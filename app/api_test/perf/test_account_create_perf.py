import requests

BASE_URL = "http://127.0.0.1:5000/api/accounts"

class TestAccountPerformance:
    
    def test_create_delete_loop_perf(self):
        for i in range(100):
           
            pesel = f"55010100{i:03d}" 
            data = {
                "name": "Perf",
                "surname": "Test",
                "pesel": pesel
            }

            response_create = requests.post(BASE_URL, json=data, timeout=0.5)
            assert response_create.status_code == 201, f"Błąd tworzenia w iteracji {i}"

            
    def test_transfer_perf_and_balance(self):

        pesel = "99010112345"
        create_data = {
            "name": "Mati",
            "surname": "Suwak",
            "pesel": pesel
        }

        requests.post(BASE_URL, json=create_data)

        transfer_amount = 100
        loops = 100
        expected_balance = transfer_amount * loops

        payload = {"amount": transfer_amount, "type": "incoming"}

        for i in range(loops):
            response = requests.post(
                f"{BASE_URL}/{pesel}/transfer", 
                json=payload, 
                timeout=0.5
            )
            assert response.status_code == 200, f"Błąd przelewu w iteracji {i}"

        get_response = requests.get(f"{BASE_URL}/{pesel}", timeout=0.5)
        assert get_response.status_code == 200
        
        account_data = get_response.json()
        assert account_data['balance'] == expected_balance
        
        requests.delete(f"{BASE_URL}/{pesel}")

