from src.account import Account
from src.companyaccount import CompanyAccount

class TestAccountLab2:

    def test_sending_balance(self):
        account = Account("John","Beverly","70345678901")
        account.balance = 100.0
        account.send_balance(100)
        assert account.balance == 0.0

    def test_receive_balance(self):
        account = Account("John","Beverly","70345678901")
        account.receive_balance(100)
        assert account.balance == 100.0
    
    def test_not_enough_balance(self):
        account = Account("John","Beverly","70345678901")
        account.balance = 50.0
        account.send_balance(100)
        assert account.balance == 50.0

    def test_express_transfer_valid(self):
        account = Account("John","Beverly","70345678901")
        account.balance = 50.0
        account.send_express_transfer(50)
        assert account.balance == -1.0
    
    def test_company_transfer_valid(self):
        account = CompanyAccount("Marek","1234567890")
        account.balance = 50.0
        account.send_company_express_transfer(50)
        assert account.balance == -5.0

    def test_too_low_balance(self):
        account = Account("John","Beverly","90345678901")
        account.balance = 40
        account.send_express_transfer(50)
        assert account.balance == 40.0

    def test_company_too_low_balance(self):
        account = CompanyAccount("Marek","1234567890")
        account.balance = 40.0
        account.send_company_express_transfer(50)
        assert account.balance == 40.0
    def test_receive_balance_adds_money(self):
        account = CompanyAccount("MAREK", "1234567890")
        account.receive_balance(100)
        assert account.balance == 100
    
    def test_receive_balance_negative_amount(self, capsys):
        account = CompanyAccount("MAREK", "1234567890")
        account.receive_balance(-50)
        assert account.balance == 0

    def test_send_balance_reduces_money(self):
        account = CompanyAccount("MAREK", "1234567890")
        account.receive_balance(200)
        account.send_balance(100)
        assert account.balance == 100
    
    def test_express_transfer_with_fee(self):
        account = CompanyAccount("MAREK", "1234567890")
        account.receive_balance(200)
        account.send_company_express_transfer(100)
        assert account.balance == 95
    
    def test_express_transfer_not_enough_balance(self, capsys):
        account = CompanyAccount("MAREK", "1234567890")
        account.receive_balance(50)
        account.send_company_express_transfer(100)
        assert account.balance == 50

    def test_nip_with_special_characters(self):
        account = CompanyAccount("MAREK", "12345-6789")
        assert account.nip == "Invalid"

    def test_adding_history_with_succesfull_company_transfer(self):
        account = CompanyAccount("MAREK", "1234567890")
        account.balance = 50
        account.send_balance(30)
        assert account.history[0] == -30

    def test_adding_history_with_succesfull_transfer(self):
        account = Account("John","Beverly","70345678901")
        account.balance = 50
        account.send_balance(30)
        assert account.history[0] == -30
    
    def test_not_adding_history_while_company_low_balance(self):
        account = CompanyAccount("MAREK", "1234567890")
        account.send_balance(30)
        assert len(account.history) == 0
    
    def test_not_adding_history_while_low_balance(self):
        account = Account("John","Beverly","70345678901")
        account.send_balance(30)
        assert len(account.history) == 0

    def test_loan_application_success(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_balance(1000)
        account.receive_balance(1000)
        account.receive_balance(1000)
        account.receive_balance(1000)
        account.receive_balance(1000)
        result = account.submit_for_loan(3000)
        
        assert account.balance == 5000 + 3000 

    def test_loan_application_rejected_due_to_negative_history(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_balance(2000) 
        account.receive_balance(2000)
        account.receive_balance(2000)
        account.receive_balance(2000)
        account.send_balance(500) 
        result = account.submit_for_loan(500)
        assert result is False
        assert account.balance == 7500 

    def test_loan_application_rejected_due_to_low_sum(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_balance(100)
        account.receive_balance(100)
        account.receive_balance(100)
        account.receive_balance(100)
        account.receive_balance(100)
        result = account.submit_for_loan(2000)       
        assert account.balance == 500 