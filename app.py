from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


class BankSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, username, password):
        if username in self.accounts:
            return False, "Username already exists. Please choose another one."
        self.accounts[username] = {'password': password, 'balance': 0}
        return True, "Account created successfully."

    def login(self, username, password):
        if username not in self.accounts or self.accounts[username]['password'] != password:
            return False, "Invalid username or password. Please try again."
        return True, "Login successful."

    
    def transfer(self, sender, receiver, amount, password):
        if sender not in self.accounts or receiver not in self.accounts:
            return False, "Invalid sender or receiver."
        if self.accounts[sender]['password'] != password:
            return False, "Invalid password."
        balance = int(self.accounts[sender]['balance'])
        amount = int(amount)  # 将金额转换为整数类型
        if balance < amount:
            return False, "Insufficient balance."
        self.accounts[sender]['balance'] = str(balance - amount)  # 更新账户余额
        self.accounts[receiver]['balance'] = str(int(self.accounts[receiver]['balance']) + amount)  # 更新接收者账户余额
        return True, "Transfer successful."
    
    def deposit(self, username, amount, password):
        if username not in self.accounts:
            return False, "Invalid username."
        if self.accounts[username]['password'] != password:
            return False, "Invalid password."
        amount = int(amount)  # 将金额转换为整数类型
        self.accounts[username]['balance'] = str(int(self.accounts[username]['balance']) + amount)  # 更新账户余额
        return True, "Deposit successful."

    def check_balance(self, username, password):
        if username not in self.accounts or self.accounts[username]['password'] != password:
            return False, "Invalid username or password."
        return True, self.accounts[username]['balance']

bank = BankSystem()

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    username = data['username']
    password = data['password']
    print('----47receive')
    success, message = bank.create_account(username, password)
    print('----48\n',success)
    print('----49\n',message)
    return jsonify({'success': success, 'message': message})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    success, message = bank.login(username, password)
    return jsonify({'success': success, 'message': message})

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.json
    sender = data['sender']
    receiver = data['receiver']
    amount = data['amount']
    password = data['password']
    success, message = bank.transfer(sender, receiver, amount, password)
    return jsonify({'success': success, 'message': message})

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    username = data['username']
    amount = data['amount']
    password = data['password']
    success, message = bank.deposit(username, amount, password)
    return jsonify({'success': success, 'message': message})

@app.route('/check_balance', methods=['POST'])
def check_balance():
    data = request.json
    username = data['username']
    password = data['password']
    success, balance = bank.check_balance(username, password)
    if success:
        return jsonify({'success': True, 'balance': balance})
    else:
        return jsonify({'success': False, 'error': balance})

if __name__ == '__main__':
    app.run(debug=True)
