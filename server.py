from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def handle_gumroad():
    data = request.form
    telegram_id = data.get("custom_field_telegram_id")
    price = float(data.get("price", 0))

    if not telegram_id:
        return "No Telegram ID", 400

    amount = int(price / 1)
    if amount >= 200:
        amount += 50

    try:
        with open("balance.json", "r") as f:
            balances = json.load(f)
    except:
        balances = {}

    balances[telegram_id] = balances.get(telegram_id, 0) + amount

    with open("balance.json", "w") as f:
        json.dump(balances, f)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
