def test_get_empty_patients(client):
    resp = client.get("/patients")
    assert resp.status_code == 200
    assert resp.json() == []

def test_create_and_get_patient(client):
    payload = {
        "name": "Alice Smith",
        "age": 29,
        "sex": "F"
    }
    # Create
    resp = client.post("/patients", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Alice Smith"
    assert data["age"] == 29
    assert data["sex"] == "F"
    assert "id" in data

    patient_id = data["id"]

    # Read back
    resp2 = client.get(f"/patients/{patient_id}")
    assert resp2.status_code == 200
    assert resp2.json() == data

def test_update_patient(client):
    # First create one
    resp = client.post("/patients", json={"name":"Bob","age":40,"sex":"M"})
    pid = resp.json()["id"]

    # Update
    update_payload = {"name": "Bobby", "age": 41, "sex": "M"}
    resp2 = client.put(f"/patients/{pid}", json=update_payload)
    assert resp2.status_code == 200
    updated = resp2.json()
    assert updated["name"] == "Bobby"
    assert updated["age"] == 41

def test_delete_patient(client):
    # Create then delete
    resp = client.post("/patients", json={"name":"Carol","age":35,"sex":"F"})
    pid = resp.json()["id"]

    resp2 = client.delete(f"/patients/{pid}")
    assert resp2.status_code == 204

    # Now 404 on GET
    resp3 = client.get(f"/patients/{pid}")
    assert resp3.status_code == 404
