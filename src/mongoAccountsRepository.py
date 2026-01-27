from pymongo import MongoClient
from src.account import Account

class MongoAccountsRepository:
    def __init__(self, host="localhost", port=27017):
        self.client = MongoClient(host, port)
        self.db = self.client['bank_db']
        self._collection = self.db['accounts']

    def save_all(self, accounts):
        self._collection.delete_many({})  
        for account in accounts:
            self._collection.update_one(
                {"pesel": account.pesel},
                {"$set": account.to_dict()},
                upsert=True 
            )

    def load_all(self):
        db_data = list(self._collection.find({}))
        accounts = []
        for data in db_data:
            acc = Account(data['first_name'], data['last_name'], data['pesel'])
            acc.balance = data['balance']
            acc.history = data['history']
            accounts.append(acc)
        return accounts