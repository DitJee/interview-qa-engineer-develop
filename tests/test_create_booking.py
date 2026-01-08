import requests

def test_create_booking_valid(api, flight_id, passport_id_correct, first_name_correct, last_name_correct):
    passport_id = passport_id_correct
    first_name = first_name_correct
    last_name = last_name_correct

    payload = {
        "passport_id": passport_id, 
        "first_name": first_name, 
        "last_name": last_name
    }

    res = requests.post(f"{api}/flights/{flight_id}/passengers", json=payload)

    assert res.status_code == 200

    body = res.json()

    assert body["flight_id"] == flight_id
    assert body["passport_id"] == passport_id
    assert body["first_name"] == first_name
    assert body["last_name"] == last_name

def test_create_booking_already_exist(api, flight_id, passport_id_correct, first_name_correct, last_name_correct):
    passport_id = passport_id_correct
    first_name = first_name_correct
    last_name = last_name_correct

    payload = {
        "passport_id": passport_id, 
        "first_name": first_name, 
        "last_name": last_name
    }

    res = requests.post(f"{api}/flights/{flight_id}/passengers", json=payload)

    assert res.status_code == 500

def test_create_booking_passport_mismatch(api, flight_id, passport_id_correct):
    payload = {
        "passport_id": passport_id_correct,
        "first_name": "Hehe",
        "last_name": "hoho"
    }

    res = requests.post(f"{api}/flights/{flight_id}/passengers", json=payload)
    assert res.status_code == 400
    assert res.json()["detail"] == "Firstname or Lastname is mismatch."