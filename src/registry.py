from src.account import Account

class AccountRegistry:
    def __init__(self):
        self.accounts: list[Account] = []
    
    def add_account(self,account: Account):
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
    

    