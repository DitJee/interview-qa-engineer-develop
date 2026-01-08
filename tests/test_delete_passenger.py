import requests

def test_delete_passenger_valid(api, flight_id, passport_id_correct, first_name_correct, last_name_correct):
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
    # print(":hehe")
    # print(res.json())

    customer_id = None
    for p in body["passengers"]:
        if p["passport_id"] == passport_id_correct:
            customer_id = p["customer_id"]
            break

    assert customer_id is not None

    update_res = requests.delete(f"{api}/flights/{flight_id}/passengers/{customer_id}")
    assert update_res.status_code == 200
    
