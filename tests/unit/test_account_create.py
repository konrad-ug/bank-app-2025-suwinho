import pytest
from src.account import Account

class TestAccount:

    @pytest.fixture
    def account(self):
        return Account("John", "Doe", "12345678901")

    def test_account_creation(self, account):
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678901"


    @pytest.mark.parametrize("pesel, expected_pesel", [
        ("12345678901", "12345678901"),   
        ("43253532153151", "Invalid"),    
        ("12345", "Invalid"),             
        (None, "Invalid")                 
    ])
    def test_pesel_initialization(self, pesel, expected_pesel):
        account = Account("John", "Doe", pesel)
        assert account.pesel == expected_pesel


    @pytest.mark.parametrize("pesel, promo_code, expected_balance", [
        ("90345678901", "PROM_ABC", 50.0), 
        ("12345678901", "PROMX_abc", 0.0), 
        ("12345678901", "PRxM_Abc", 0.0),  
        ("12345678901", "PROM_Abcc", 0.0), 
        ("50010112345", "PROM_ABC", 0.0),  
        (None, "PROM_ABC", 0.0),          
        ("70345678901", "PROM_ABc", 50.0), 
    ])
    def test_promo_code_application(self, pesel, promo_code, expected_balance):
        account = Account("John", "Doe", pesel, promo_code)
        assert account.balance == expected_balance

    def test_to_dict_returns_correct_fields(self):
        account = Account("Jan", "Kowalski", "12345678901")
        account.balance = 150.0
        account.history = [150.0]
    
        expected_dict = {
            "first_name": "Jan",
            "last_name": "Kowalski",
            "pesel": "12345678901",
            "balance": 150.0,
            "history": [150.0]
        }

        assert account.to_dict() == expected_dict