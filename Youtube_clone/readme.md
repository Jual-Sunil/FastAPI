# YouTube Clone (FastAPI)

This is a **YouTube clone project** built with **FastAPI** for the backend and **Jinja2 templates** for the frontend.  
It’s a learning project that shows how to combine user authentication, video browsing, and an **AI-powered chatbot** to make search easier.

---

## Features

- User login and signup system  
- Video browsing, and search  
- Description-based search using AI  
- Simple frontend using HTML, CSS, and Jinja2 templates  
- AI chatbot that helps you find videos by:  
  - Showing random suggestions or keywords 
  - Understanding text descriptions (semantic search)  

---

## How the Project Works

1. **User Authentication**  
   - Users can sign up and log in.  
   - Sessions are handled securely.  

2. **Videos**  
   - Videos have a title, description, tags, thumbnail, and creator.  
   - You can browse videos or search them manually.
   - Follows a UI similar to Youtube but not as advanced as I used AI tools to generate them.  

3. **AI Chatbot**  
   - The chatbot appears as a chat window.  
   - You can:  
     - Type descriptions based on your own preference or based on what is already shown below the text-box.  
   - Behind the scenes, the chatbot uses a **semantic search system** powered by free LLM APIs.  

4. **Limitation**  
   - Right now, only a limited number of videos can be processed because free LLM APIs have token limits.  
   - This can be expanded in the future with paid APIs or better infrastructure.  

---

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy  
- **Frontend**: Jinja2, HTML, CSS, JS  
- **Database**: PostgreSQL  
- **AI Integration**: Cohere / LLM APIs for semantic search  

---

## Setup and Run

1. Clone the repository:
   cmd
   git clone --depth 1 https://github.com/Jual-Sunil/FastAPI.git
   cd FastAPI/Youtube_clone

2. Create a virtual environment and install dependencies:
    python -m venv venv
    source venv/bin/activate   # for Linux/Mac
    venv\Scripts\activate      # for Windows
    pip install -r requirements.txt

3. Setup environment variables in a .env file (DB URL, secret keys, etc.).
    Uploaded a sample .env file to follow

4. Run database migrations
    alembic init {file name}
    alembic --autogenerate -m "changes you've made"
    alembic upgrade head

5. Start your FastAPI server
    uvicorn main:app --reload

Future improvements
    -Handle larger video datasets by using paid API plans
    -Improve chatbot intelligence with advanced LLMs
    -Add video upload & streaming features