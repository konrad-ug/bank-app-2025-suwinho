from datetime import datetime
from smtp.smtp import SMTPClient

class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        
        if self.is_promo_code_valid(promo_code) and self.is_person_not_elder(pesel):
            self.balance = 50.0

        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.history = []

    def is_pesel_valid(self, pesel):
        if pesel and len(pesel) == 11:
            return True
        return False

    def is_promo_code_valid(self, promo_code):
        if promo_code and promo_code.startswith("PROM_") and len(promo_code) == 8:
            return True
        return False

    def is_person_not_elder(self, pesel):
        if not pesel:
            return False
        date_of_birth = int(pesel[:2])
        if 26 < date_of_birth < 60:
            return False
        return True

    def send_balance(self, money_to_send):
        if self.balance >= money_to_send and money_to_send > 0:
            self.balance -= money_to_send
            self.history.append(-money_to_send)
            return True
        else:
            print("Not enough balance")
            return False
    
    def receive_balance(self, money_to_receive):
        if money_to_receive > 0:
            self.balance += money_to_receive
            self.history.append(money_to_receive)
            return True
        return False
    
    def send_express_transfer(self, money_to_send, additional_fee=1.0):
        if self.balance >= money_to_send and money_to_send > 0:
            self.balance -= money_to_send
            self.balance -= additional_fee
            self.history.append(-money_to_send)
            self.history.append(-additional_fee)
            return True
        else:
            print("Not enough balance")
            return False

    def submit_for_loan(self, amount_for_loan):
        third_last_index = len(self.history)-3
        last_three_transactions = self.history[third_last_index:]
        last_five_transactions = self.history[len(self.history)-5:]
        for transaction in last_three_transactions:
            if transaction < 0:
                return False
        sum_transactions = 0
        for transaction in last_five_transactions:
            sum_transactions+=transaction
        
        if sum_transactions > amount_for_loan:
            self.balance+=amount_for_loan
            return True
        else:
            return False
        
    def send_history_via_email(self, email_address: str) -> bool:
        today = datetime.now().strftime('%Y-%m-%d')
        subject = f"Account Transfer History {today}"
        body = self._prepare_content()

        smtp_client = SMTPClient()
        return smtp_client.send(subject, body, email_address)

    def _prepare_content(self) -> str:
        return f"Personal account history: {self.history}"