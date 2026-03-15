from flask import Flask
import os

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return f'''
    🚀 Trading Bot Betfair LIVE ✅<br>
    TG_TOKEN: {"OK" if os.getenv('TG_TOKEN') else "MANCANTE"}<br>
    PORT: {os.environ.get("PORT", "5000")}
    '''

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Bot server avviato!")
    app.run(host='0.0.0.0', port=port)

