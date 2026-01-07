import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from src.registry import AccountRegistry
from src.account import Account

app = Flask(__name__)
registry = AccountRegistry()


@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    account = Account(data["name"], data["surname"], data["pesel"])
    
    result = registry.add_account(account)
    
    if result != False:
        return jsonify({"message": "Account created"}), 201
    else:
        return jsonify({"error": "Account with this pesel already exists"}), 409

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.show_all_accounts()
    if not accounts:
        return 404
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel":
    acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count = registry.show_quantity()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    finded = registry.find_accounts_with_pesel(pesel)
    if not finded:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"name": finded.first_name, "surname": finded.last_name, "pesel": finded.pesel}), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    print("got request!", data)
    account = registry.find_accounts_with_pesel(pesel)
    if not account:
        return 404
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
    if "balance" in data: 
        account.balance = data["balance"]
    return jsonify({"message": "Account updated"}), 200
    
@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.find_accounts_with_pesel(pesel)
    if not account:
        return jsonify({"error": "Account not found"}), 404 
    registry.delete_account(account)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def make_outgoing_transfer(pesel):
    data = request.get_json()
    amount = data["amount"]
    transfer_type = data["type"]
    if not amount or not transfer_type:
        return jsonify({"error": "Missing amount or type"}), 400
    account = registry.find_accounts_with_pesel(pesel)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    try:
        if transfer_type == "outgoing":
            success = account.send_balance(amount)
            if success:
                return jsonify({"message": "Zlecenie przyjęto do realizacji", "balance": account.balance}), 200
            else:
                return jsonify({"error": "Insufficient funds"}),422
        if transfer_type == "incoming":
            success = account.receive_balance(amount)
            if success:
                return jsonify({"message": "Zlecenie przyjęto do realizacji", "balance": account.balance}), 200
            else:
                return jsonify({"error": "Insufficient funds"}),422
        if transfer_type == "express":
            success = account.send_express_transfer(amount)
            if success:
                return jsonify({"message": "Zlecenie przyjęto do realizacji", "balance": account.balance}), 200
            else:
                return jsonify({"error": "Insufficient funds"}),422
    except ValueError:
        return jsonify({"error": "Invalid transfer type"}),400

if __name__ == "__main__":
    app.run(debug=True)