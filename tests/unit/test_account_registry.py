import pytest
from src.registry import AccountRegistry
from src.account import Account

class TestAccountRegistry:
    
    @pytest.fixture
    def account_registry(self):
        return AccountRegistry()
    
    def test_add_duplicate_account(self, account_registry):
        acc1 = Account("John", "Doe", "12345678901")
        acc2 = Account("Jane", "Doe", "12345678901") 
        
        account_registry.add_account(acc1)
        result = account_registry.add_account(acc2) 
        
        assert result == False
        assert account_registry.show_quantity() == 1
        

    @pytest.mark.parametrize("account_data, pesel_to_find, expected_found", [
        (("John", "Doe", "12345678901"), "12345678901", True),
        (("John", "Doe", "12345678901"), "00000000000", False),
    ])
    def test_finding_accounts_with_pesel(self, account_registry, account_data, pesel_to_find, expected_found):

        first_name, last_name, pesel = account_data
        new_account = Account(first_name, last_name, pesel)
        account_registry.add_account(new_account)
        result = account_registry.find_accounts_with_pesel(pesel_to_find)
        if expected_found:
            assert result == new_account
            assert result.pesel == pesel_to_find
        else:
            assert result == []


    @pytest.fixture
    def account1(self):
        return Account("Jan", "Kowalski", "12345678901")

    @pytest.fixture
    def account2(self):
        return Account("Anna", "Nowak", "98765432109")
    
    def test_add_account_increases_quantity(self, account_registry, account1):
        account_registry.add_account(account1)
        assert account_registry.show_quantity() == 1
        
    def test_add_account_returns_current_list(self, account_registry, account1):
        returned_list = account_registry.add_account(account1)
        
        assert isinstance(returned_list, list)
        assert len(returned_list) == 1
        assert returned_list[0] == account1

    def test_show_all_accounts(self, account_registry, account1, account2):
        account_registry.add_account(account1)
        account_registry.add_account(account2)
        all_accounts = account_registry.show_all_accounts()
        assert len(all_accounts) == 2
        assert account1 in all_accounts
        assert account2 in all_accounts

    def test_show_quantity_updates_dynamically(self, account_registry, account1, account2):
        assert account_registry.show_quantity() == 0
        
        account_registry.add_account(account1)
        assert account_registry.show_quantity() == 1
        
        account_registry.add_account(account2)
        assert account_registry.show_quantity() == 2
        
    def test_delete_account_success(self, account_registry, account1):
        account_registry.add_account(account1)
        assert account_registry.show_quantity() == 1       
        result = account_registry.delete_account(account1)
        assert account_registry.show_quantity() == 0
        assert account1 not in account_registry.show_all_accounts()

    def test_delete_account_not_found(self, account_registry):
        result = account_registry.delete_account(None)
        
        assert result == 404
        assert account_registry.show_quantity() == 0