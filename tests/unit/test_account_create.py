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
        account = Account("John", "Johnson","12345678901","PROMX_abc")
        
        assert account.balance == 0.0
    
    def test_promo_invalid_prefix(self):
        account = Account("John", "Johnson","12345678901", "PRxM_Abc")
        assert account.balance == 0.0

    def test_promo_invalid_suffix(self):
        account = Account("John", "Johnson","12345678901", "PRxM_Abc")
        assert account.balance == 0.0

    def test_reduce_balance(self):
        account = Account("John", "Johnson","12345678901", "PROM_Abc")
        assert account.balance == 0.0

    def test_balance_not_changed(self):
        account = Account("John","Beverly","70345678901","PROM_ABc")
        assert account.balance == 0.0

