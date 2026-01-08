import requests

PASSPORT_ID = "BC1501"
FIRST_NAME = "Shauna_2"
LAST_NAME_ID = "Davila_2"

def test_update_passenger_valid(api, flight_id, passport_id_correct, first_name_correct, last_name_correct):
    passport_id = passport_id_correct
    first_name = first_name_correct
    last_name = last_name_correct
    payload = {
        "passport_id": passport_id, 
        "first_name": first_name, 
        "last_name": last_name
    }

    _res = requests.post(f"{api}/flights/{flight_id}/passengers", json=payload)
    res = requests.get(f"{api}/flights/{flight_id}/passengers")
    body= res.json()
    print(":hehe")
    print(res.json())

    customer_id = None
    for p in body["passengers"]:
        if p["passport_id"] == passport_id_correct:
            customer_id = p["customer_id"]
            break

    assert customer_id is not None

    update_res = requests.put(f"{api}/flights/{flight_id}/passengers/{customer_id}", json=payload)
    assert update_res.status_code == 200
    

def test_update_passenger_mismatch(api, flight_id, passport_id_correct, first_name_correct, last_name_correct):
    passport_id = passport_id_correct
    first_name = first_name_correct
    last_name = last_name_correct
    payload = {
        "passport_id": passport_id, 
        "first_name": first_name, 
        "last_name": last_name
    }

    _res = requests.post(f"{api}/flights/{flight_id}/passengers", json=payload)
    res = requests.get(f"{api}/flights/{flight_id}/passengers")
    body= res.json()
    print(":hehe")
    print(res.json())

    customer_id = None
    for p in body["passengers"]:
        if p["passport_id"] == passport_id_correct:
            customer_id = p["customer_id"]
            break

    assert customer_id is not None

    update_payload = {
        "passport_id": passport_id, 
        "first_name": FIRST_NAME, 
        "last_name": LAST_NAME_ID
    }
    update_res = requests.put(f"{api}/flights/{flight_id}/passengers/{customer_id}", json=update_payload)
    assert update_res.status_code == 400
    assert update_res.json()["detail"] == "Firstname or Lastname is mismatch."
    
