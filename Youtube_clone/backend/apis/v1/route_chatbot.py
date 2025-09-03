import random
import json
import os
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from fastapi import Depends
import numpy as np

from backend.core.config import Settings
from backend.schemas.chatbot import Conversations
from backend.db.models.videos import Video
from backend.db.session import get_db

cohere_llm = ChatCohere(
    cohere_api_key=Settings.COHERE_APIKEY,
    model="command-r",
    temperature=0.7
)

cohere_embeddings = CohereEmbeddings(
    cohere_api_key=Settings.COHERE_APIKEY,
    model="embed-english-v3.0"
)

conversation_strg: Dict[str, Conversations] = {}

class SemanticVideoSearch:
    def __init__(self, db_session: Session = Depends(get_db)):
        self.db = db_session
        self.vector_store = None
        self.processed_videos = set()  # Track processed video IDs
        self.vector_store_path = "./backend/db/faissdb"
        self._initialize_vector_store()

    def _generate_semantic_keyword(self, video: Video) -> str:
        """Generate a semantic keyword for a video using LLM"""
        keyword_prompt = PromptTemplate(
            input_variables=["title"],
            template="""
            Analyze this video content and generate a single, concise semantic keyword that best represents its core theme or topic.
            
            Video Title: {title}
            
            Return ONLY the keyword without any additional text, explanations, or formatting.
            The keyword should be 1-3 words maximum and capture the essence of the video.
            
            Semantic Keyword:
            """
        )
        
        try:
            chain = keyword_prompt | cohere_llm
            response = chain.invoke({
                "title": video.title or ""
            })
            return response.content.strip()
        except Exception as e:
            print(f"Error generating keyword for video {video.id}: {e}")
            # Fallback: use first tag or title
            if video.tags:
                return video.tags.split(",")[0].strip()
            return video.title or "unknown"

    def _initialize_vector_store(self):
        """Initialize or load the vector store, processing new videos"""
        try:
            # Load existing processed video IDs if they exist
            processed_file = f"{self.vector_store_path}_processed.json"
            if os.path.exists(processed_file):
                with open(processed_file, 'r') as f:
                    self.processed_videos = set(json.load(f))
            
            # Get all videos from database
            all_videos = self.db.query(Video).all()
            new_videos = [v for v in all_videos if str(v.id) not in self.processed_videos]
            
            if new_videos:
                print(f"Found {len(new_videos)} new videos to process")
                new_docs = []
                
                for video in new_videos:
                    # Generate semantic keyword
                    semantic_keyword = self._generate_semantic_keyword(video)
                    
                    # Create document with semantic keyword as main content
                    doc = Document(
                        page_content=semantic_keyword,
                        metadata={
                            'id': str(video.id),
                            'title': video.title,
                            'desc': video.desc,
                            'tags': video.tags,
                            'semantic_keyword': semantic_keyword
                        }
                    )
                    new_docs.append(doc)
                    self.processed_videos.add(str(video.id))
                
                # Load existing vector store or create new one
                if os.path.exists(self.vector_store_path):
                    self.vector_store = FAISS.load_local(
                        self.vector_store_path, 
                        cohere_embeddings, 
                        allow_dangerous_deserialization=True
                    )
                    # Add new documents
                    self.vector_store.add_documents(new_docs)
                else:
                    # Create new vector store
                    self.vector_store = FAISS.from_documents(
                        new_docs,
                        cohere_embeddings
                    )
                
                # Save updated vector store and processed videos list
                self.vector_store.save_local(self.vector_store_path)
                with open(processed_file, 'w') as f:
                    json.dump(list(self.processed_videos), f)
                
                print(f"Processed {len(new_docs)} new videos. Total videos in store: {len(self.processed_videos)}")
            
            elif os.path.exists(self.vector_store_path):
                # Load existing vector store
                self.vector_store = FAISS.load_local(
                    self.vector_store_path, 
                    cohere_embeddings, 
                    allow_dangerous_deserialization=True
                )
                print(f"Loaded existing vector store with {len(self.processed_videos)} videos")
            else:
                print("No videos found and no existing vector store")
                self.vector_store = None
                
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            self.vector_store = None

    def desc_based_vids(self, desc: str, k: int = 10) -> List[Video]:
        """Find videos based on semantic similarity to description"""
        if not self.vector_store:
            return []
        try:
            # Similarity search using the semantic keywords
            docs = self.vector_store.similarity_search(desc, k=k)
            
            # Extract video IDs and get videos from database
            video_ids = [doc.metadata['id'] for doc in docs]
            videos = self.db.query(Video).filter(Video.id.in_(video_ids)).all()
            
            # Sort videos based on search result order
            vid_dict = {str(video.id): video for video in videos}
            sorted_vids = [vid_dict[vid_id] for vid_id in video_ids if vid_id in vid_dict]
            
            return sorted_vids
            
        except Exception as e:
            print(f"Error in semantic search: {e}")
            return []
        
    def refresh_vector_store(self):
        """Force refresh of vector store to include any new videos"""
        self.processed_videos = set()
        self._initialize_vector_store()
