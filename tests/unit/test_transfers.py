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
    
    
    