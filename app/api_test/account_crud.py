import requests
import pytest

URL = "http://127.0.0.1:5000/api/accounts"

class TestAccountApi:
    
   
    @pytest.fixture(scope="function", autouse=True)
    def clean_environment(self):
        yield 
        response = requests.get(URL)
        if response.status_code == 200:
            for account in response.json():
                pesel = account.get("pesel")
                if pesel:
                    requests.delete(f"{URL}/{pesel}")
    @pytest.fixture(scope="function")
    def existing_account(self):
        pesel = "88010155555"
        account_data = {"name": "Test", "surname": "User", "pesel": pesel}
        requests.delete(f"{URL}/{pesel}") 
        response = requests.post(URL, json=account_data)
        assert response.status_code == 201
        yield pesel   
        requests.delete(f"{URL}/{pesel}")
    @pytest.fixture(scope="function")
    def rich_account(self, existing_account):
        pesel = existing_account
        requests.post(f"{URL}/{pesel}/transfer", json={"amount": 1000, "type": "incoming"})
        return pesel

    def test_create_account(self):
        pesel = "99010100001"
        data = {
            "name": "Mati",
            "surname": "Suwak",  
            "pesel": pesel
        }

        response = requests.post(URL, json=data)
        
        assert response.status_code == 201
        assert response.json().get("message") == "Account created"

    def test_api_create_duplicate_account(self):
        payload = {"name": "Jan", "surname": "Nowak", "pesel": "11111111111"}
        
        requests.post(URL, json=payload) 
        response = requests.post(URL, json=payload) 
    
        assert response.status_code == 409

    def test_get_accounts(self):
        requests.post(URL, json={"name": "Jan", "surname": "Kowalski", "pesel": "99010100002"})
        
        response = requests.get(URL)
        data = response.json()
        
        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_accounts_count(self):
        requests.post(URL, json={"name": "Jan", "surname": "Kowalski", "pesel": "99010100003"})
        
        response = requests.get(f"{URL}/count")
        data = response.json()
        
        assert "count" in data
        assert data["count"] >= 1

    def test_get_account_by_pesel(self):
        pesel = "99010100004"
        requests.post(URL, json={"name": "Jan", "surname": "Kowalski", "pesel": pesel})
        
        response = requests.get(f"{URL}/{pesel}")
        data = response.json()
        
        assert response.status_code == 200
        assert str(data["pesel"]) == pesel

    def test_update_account(self):
        pesel = "99010100005"
        requests.post(URL, json={"name": "Jan", "surname": "OldName", "pesel": pesel})
        
        update_data = {"name": "Jan", "surname": "NewName", "pesel": pesel}
        response = requests.patch(f"{URL}/{pesel}", json=update_data)
        get_response = requests.get(f"{URL}/{pesel}")
        data = get_response.json()
        
        assert data["surname"] == "NewName"
        

    def test_delete_account(self):
        pesel = "99010100006"
        requests.post(URL, json={"name": "Jan", "surname": "Kowalski", "pesel": pesel})
        
        response = requests.delete(f"{URL}/{pesel}")
        assert response.status_code == 200
        check_response = requests.get(f"{URL}/{pesel}")
        assert check_response.status_code == 404
    
    def test_incoming_transfer(self, existing_account):
        pesel = existing_account
        payload = {"amount": 100, "type": "incoming"}
        
        response = requests.post(f"{URL}/{pesel}/transfer", json=payload)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Zlecenie przyjęto do realizacji"
        assert response_data["balance"] == 100

    def test_outgoing_transfer_success(self,rich_account):
        pesel = rich_account
        payload = {"amount":100, "type": "outgoing"}
        response = requests.post(f"{URL}/{pesel}/transfer",json = payload)
        assert response.status_code == 200
        assert response.json()["balance"] == 900

    def test_outgoing_transfer_fail(self,existing_account):
        pesel = existing_account
        payload = {"amount":100, "type":"outgoing"} 
        response = requests.post(f"{URL}/{pesel}/transfer",json = payload)
        assert response.status_code == 422
        assert "Insufficient funds" in response.json()["error"]

    def test_express_transfer_success(self,rich_account):
        pesel = rich_account
        payload = {"amount":100, "type":"express"} 
        response = requests.post(f"{URL}/{pesel}/transfer",json = payload)
        assert response.status_code == 200
        assert response.json()["balance"] == 899 

    def test_express_transfer_fail(self,existing_account):
        pesel = existing_account
        payload = {"amount":100, "type":"express"}
        response = requests.post(f"{URL}/{pesel}/transfer",json = payload)
        assert response.status_code == 422

    def test_transfer_to_non_existent_account(self):
        pesel = "00000000000"
        payload = {"amount": 100, "type": "incoming"}
        
        response = requests.post(f"{URL}/{pesel}/transfer", json=payload)
        
        assert response.status_code == 404
        assert "Account not found" in response.json()["error"]