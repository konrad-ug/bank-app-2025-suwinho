from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", '12345678901')
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678901"        

    def test_pesel_to_long(self):
        account = Account("John","Dheere","43253532153151")
        assert account.pesel == "Invalid"
    
    def test_promo_valid(self):
        account = Account("John", "Johnson","12345678901")
        account.add_promo_code("Prom_XYZ")
        assert account.balance == 50
    
    def test_promo_invalid_prefix(self):
        account = Account("John", "Johnson","12345678901", "PRxM_Abc")
        assert account.balance == 50

    def test_promo_invalid_suffix(self):
        account = Account("John", "Johnson","12345678901", "PRxM_Abc")
        assert account.balance == 50