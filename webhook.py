from flask import Flask, request
app = Flask(__name__)

@app.route('/gumroad-webhook', methods=['POST'])
def gumroad_webhook():
    data = request.json
    # burada webhook datanı emal et
    return 'OK', 200

# Lazım olsa başqa route-lar əlavə et
