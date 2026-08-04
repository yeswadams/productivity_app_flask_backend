def test_react_auth_contract(client):
    signup = client.post("/signup", json={
        "username": "alex",
        "password": "secure-password",
        "password_confirmation": "secure-password",
    })
    assert signup.status_code == 201
    assert signup.get_json()["token"]

    login = client.post("/login", json={"username": "alex", "password": "secure-password"})
    assert login.status_code == 200
    me = client.get("/me", headers={"Authorization": f"Bearer {login.get_json()['token']}"})
    assert me.status_code == 200
    assert me.get_json()["username"] == "alex"


def test_expense_crud_pagination_and_ownership(client, auth_header):
    for index in range(3):
        response = client.post(
            "/api/v1/expenses",
            headers=auth_header,
            json={"title": f"Expense {index}", "amount": index + 1},
        )
        assert response.status_code == 201

    page = client.get("/api/v1/expenses?page=1&per_page=2", headers=auth_header)
    assert page.status_code == 200
    assert len(page.get_json()["expenses"]) == 2
    assert page.get_json()["pagination"]["total"] == 3

    expense_id = page.get_json()["expenses"][0]["id"]
    updated = client.patch(
        f"/api/v1/expenses/{expense_id}",
        headers=auth_header,
        json={"description": None},
    )
    assert updated.status_code == 200
    assert updated.get_json()["expense"]["description"] is None

    client.post("/signup", json={
        "username": "other_user",
        "password": "secure-password",
        "password_confirmation": "secure-password",
    })
    other_login = client.post("/login", json={"username": "other_user", "password": "secure-password"})
    other_headers = {"Authorization": f"Bearer {other_login.get_json()['token']}"}
    assert client.get(f"/api/v1/expenses/{expense_id}", headers=other_headers).status_code == 404
    assert client.delete(f"/api/v1/expenses/{expense_id}", headers=other_headers).status_code == 404

    assert client.delete(f"/api/v1/expenses/{expense_id}", headers=auth_header).status_code == 200


def test_expense_routes_require_a_valid_token(client):
    assert client.get("/api/v1/expenses").status_code == 401
    assert client.get("/api/v1/expenses", headers={"Authorization": "Bearer invalid"}).status_code == 422
