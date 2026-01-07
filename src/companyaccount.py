import requests
from datetime import datetime
from smtp.smtp import SMTPClient

class CompanyAccount:
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.balance = 0
        self.history = []

    def check_nip_in_db(self,nip):
        BANK_APP_MF_URL = "https://wl-api.mf.gov.pl/api/search/nip/"
        date = "2025-12-10"
        response = requests.get(f"{BANK_APP_MF_URL}{nip}/{date}")
        data = response.json()
        if data['result']['subject']['statusVat'] != "Czynny":
            print("nie ma takiego nipu")
            return False
        return True

    def is_nip_valid(self, nip):
        if self.check_nip_in_db(nip) == False:
            raise ValueError("COMPANY NOT REGISTERED!!!")

        if len(nip) == 10 and nip.isdigit():
            return True
        return False

    def send_balance(self, money_to_send):
        if self.balance >= money_to_send and money_to_send > 0:
            self.balance -= money_to_send
            self.history.append(-money_to_send)
        else:
            print("Not enough balance")

    def receive_balance(self, money_to_receive):
        if money_to_receive > 0:
            self.balance += money_to_receive
            self.history.append(money_to_receive)

    def send_company_express_transfer(self, money_to_send, additional_fee=5.0):
        if self.balance >= money_to_send and money_to_send > 0:
            self.balance -= money_to_send
            self.balance -= additional_fee
            self.history.append(-money_to_send)
            self.history.append(-additional_fee)
        else:
            print("Not enough balance")

    def submit_for_company_loan(self,money_to_loan):
        if self.balance < money_to_loan*2:
            return False
        if any(outcoming_money == -1775 for outcoming_money in self.history):
            self.balance += money_to_loan
            return True
        return False
    
    def send_history_via_email(self, email_address: str) -> bool:
        today = datetime.now().strftime('%Y-%m-%d')
        subject = f"Account Transfer History {today}"
        body = self._prepare_content()

        smtp_client = SMTPClient()
        return smtp_client.send(subject, body, email_address)
    
    def _prepare_content(self) -> str:
        return f"Company account history: {self.history}"