import pytest
from unittest.mock import patch 
from src.account import Account
from src.companyaccount import CompanyAccount

class TestAccountRefactored:

    @pytest.fixture(autouse=True)
    def mock_api(self):
        with patch('src.companyaccount.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "result": {"subject": {"statusVat": "Czynny"}}
            }
            yield mock_get

    @pytest.fixture
    def account(self):
        return Account("John", "Doe", "12345678901")

    @pytest.fixture
    def company_account(self):
        return CompanyAccount("MarekCorp", "1234567890")

    @pytest.mark.parametrize("initial_balance, amount, expected_balance", [
        (100.0, 100.0, 0.0),    
        (100.0, 50.0, 50.0),    
        (50.0, 100.0, 50.0),    
        (40.0, 50.0, 40.0)     
    ])
    def test_send_balance(self, account, initial_balance, amount, expected_balance):
        account.balance = initial_balance
        account.send_balance(amount)
        assert account.balance == expected_balance

    @pytest.mark.parametrize("initial_balance, amount, expected_balance", [
        (0.0, 100.0, 100.0),    
        (50.0, 50.0, 100.0),    
        (0.0, -50.0, 0.0)      
    ])
    def test_receive_balance(self, account, initial_balance, amount, expected_balance):
        account.balance = initial_balance
        account.receive_balance(amount)
        assert account.balance == expected_balance

    @pytest.mark.parametrize("initial_balance, amount, expected_balance", [
        (50.0, 50.0, -1.0),     
        (40.0, 50.0, 40.0)      
    ])
    def test_express_transfer_individual(self, account, initial_balance, amount, expected_balance):
        account.balance = initial_balance
        account.send_express_transfer(amount)
        assert account.balance == expected_balance

    @pytest.mark.parametrize("initial_balance, amount, expected_balance", [
        (50.0, 50.0, -5.0),    
        (200.0, 100.0, 95.0),   
        (50.0, 100.0, 50.0),    
        (40.0, 50.0, 40.0)      
    ])
    def test_express_transfer_company(self, company_account, initial_balance, amount, expected_balance):
        company_account.balance = initial_balance
        company_account.send_company_express_transfer(amount)
        assert company_account.balance == expected_balance

    def test_history_updated_after_transfer(self, account):
        account.balance = 100
        account.send_balance(30)
        assert account.history[-1] == -30 
        assert len(account.history) == 1

    def test_history_not_updated_on_fail(self, account):
        account.balance = 10
        account.send_balance(100) 
        assert len(account.history) == 0

    @pytest.mark.parametrize("history, loan_amount, expected_result, balance_change", [
        ([1000, 1000, 1000, 1000, 1000], 3000, True, 3000),
        ([2000, 2000, 2000, -500, 2000], 500, False, 0),
        ([100, 100, 100, 100, 100], 2000, False, 0),
        ([1000, 1000], 500, True, 500) 
    ])
    def test_loan_application(self, account, history, loan_amount, expected_result, balance_change):
        account.history = history
        initial_balance = 0
        account.balance = initial_balance
        result = account.submit_for_loan(loan_amount)
        
        assert result == expected_result
        assert account.balance == initial_balance + balance_change

    @pytest.mark.parametrize("history, initial_balance, loan_amount, expected_result, balance_change", [
        #uda sie 
        ([1000, 1000, 1000, 1000, -1775], 7000 , 3000, True, 3000),
        # nie ma opłaty ZUS
        ([2000, 2000, 2000, -500, 2000], 2000 , 500, False, 0),
        # za mało salda na portfelu
        ([100, 100, 100, 100, 100], 1000 ,2000, False, 0),
    ])
    def test_company_loan_application(self, company_account, history, initial_balance, loan_amount, expected_result, balance_change):
        company_account.history = history
        company_account.balance = initial_balance
        result = company_account.submit_for_company_loan(loan_amount)

        assert result == expected_result
        assert company_account.balance == initial_balance + balance_change
    
    @pytest.fixture
    def company_account(self, mock_api):
        return CompanyAccount("MarekCorp", "1234567890")

    @pytest.mark.parametrize("initial_balance, amount, expected_balance, expected_history_len", [
        (100.0, 50.0, 50.0, 1),   # Sukces
        (100.0, 150.0, 100.0, 0),  # Za mało środków
        (100.0, -10.0, 100.0, 0),  # Ujemna kwota
    ])
    def test_company_send_balance(self, company_account, initial_balance, amount, expected_balance, expected_history_len):
        company_account.balance = initial_balance
        company_account.send_balance(amount)
        assert company_account.balance == expected_balance
        assert len(company_account.history) == expected_history_len

    @pytest.mark.parametrize("initial_balance, amount, expected_balance, expected_history_len", [
        (0.0, 100.0, 100.0, 1),   # Sukces
        (50.0, 0.0, 50.0, 0),     # przelewamy 0 złoycyh
        (50.0, -20.0, 50.0, 0),   # przelewamy ujemną kwotę
    ])
    def test_company_receive_balance(self, company_account, initial_balance, amount, expected_balance, expected_history_len):
        company_account.balance = initial_balance
        company_account.receive_balance(amount)
        assert company_account.balance == expected_balance
        assert len(company_account.history) == expected_history_len

    

    def test_company_express_transfer_insufficient_funds(self, company_account):
        company_account.send_company_express_transfer(50) 
        assert company_account.balance == 0
        assert len(company_account.history) == 0