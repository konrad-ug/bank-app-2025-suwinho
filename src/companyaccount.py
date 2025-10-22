

class CompanyAccount:
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.balance = 0
    
    def is_nip_valid(self, nip):
        if len(nip) == 10 and nip.isdigit():
            return True
        else:
            return False
    
    def send_balance(self,money_to_send):
        if self.balance >= money_to_send and money_to_send > 0:
            self.balance -= money_to_send
        else:
            print("Not enough balance")
    
    def receive_balance(self,money_to_receive):
        if money_to_receive > 0:
            self.balance += money_to_receive
        
    def send_company_express_transfer(self, money_to_send, additional_fee = 5.0):
        if self.balance >= money_to_send and money_to_send > 0:
            self.balance -= money_to_send
            self.balance -= additional_fee
        else:
            print("Not enough balance")
    