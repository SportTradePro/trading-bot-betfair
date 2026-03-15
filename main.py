from flask import Flask, request, Response
import os
import requests
import json

app = Flask(__name__)
TOKEN = os.getenv('TG_TOKEN')
bot_url = f"https://api.telegram.org/bot{TOKEN}"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return '🚀 Trading Bot Betfair LIVE ✅'

@app.route('/health')
def health():
    return 'OK'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    chat_id = update['message']['chat']['id']
    text = update['message']['text']
    
    if text == '/start':
        send_message(chat_id, '🚀 Trading Bot Betfair LIVE ✅')
    
    return Response('OK', status=200)

def send_message(chat_id, text):
    url = f"{bot_url}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
