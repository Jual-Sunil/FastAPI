def test_create_user(client):
    data = {"email" : "Something@fastapitut.com",
            "password" : "something_gets_the_other"}
    response = client.post("/users/", json=data)
    assert response.status_code == 201
    assert response.json()["email"] == "Something@fastapitut.com"