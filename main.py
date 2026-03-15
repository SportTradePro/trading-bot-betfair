from flask import Flask, jsonify
import os
import time
from datetime import datetime

app = Flask(__name__)

# SIMULAZIONE BETFAIR (dati reali formato)
MERCATI_SIMULATI = [
    {"marketId": "1.123456", "marketName": "Juventus vs Inter", "totalMatched": "€2.5M", "back": "1.95", "lay": "1.98"},
    {"marketId": "1.123457", "marketName": "Milan vs Napoli", "totalMatched": "€1.8M", "back": "2.10", "lay": "2.15"},
    {"marketId": "1.123458", "marketName": "Roma vs Lazio", "totalMatched": "€1.2M", "back": "1.85", "lay": "1.88"}
]

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return f'''
    🚀 Trading Bot Betfair LIVE ✅<br>
    TG_TOKEN: {"OK" if os.getenv('TG_TOKEN') else "MANCANTE"}<br>
    BF_SIMULATO: OK (3 mercati live)<br>
    PORT: {os.environ.get("PORT", "5000")}
    <br><a href="/markets">📊 Mercati LIVE</a> | 
    <a href="/trade">🤖 Auto Trade</a> | 
    <a href="/status">📈 Status</a>
    '''

@app.route('/markets')
def markets():
    return jsonify({"mercati": MERCATI_SIMULATI, "timestamp": str(datetime.now())})

@app.route('/trade')
def trade():
    return jsonify({
        "strategia": "Scalping 2%",
        "trade_eseguito": True,
        "profitto": "+€12.50",
        "tempo": str(datetime.now())
    })

@app.route('/status')
def status():
    return f"✅ Bot trading attivo - Prossimo trade: {time.strftime('%H:%M:%S', time.localtime(time.time() + 60))}"

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Trading Bot SIMULATO START!")
    app.run(host='0.0.0.0', port=port)
