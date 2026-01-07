from src.account import Account

class AccountRegistry:
    def __init__(self):
        self.accounts: list[Account] = []
    
    def add_account(self, account: Account):
        for existing_account in self.accounts:
            if existing_account.pesel == account.pesel:
                return False 
    
        self.accounts.append(account)
        return self.accounts
    
    def find_accounts_with_pesel(self,pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return []
    
    def show_all_accounts(self):
        return self.accounts
    
    def show_quantity(self):
        return len(self.accounts)
    
    def delete_account(self,account):
        if account:
            return self.accounts.remove(account)
        return 404

    