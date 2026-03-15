from flask import Flask
import os
from betfairlightweight import APIClient, filters

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    status = f'''
    🚀 Trading Bot Betfair LIVE ✅<br>
    TG_TOKEN: {"OK" if os.getenv('TG_TOKEN') else "MANCANTE"}<br>
    BF_USERNAME: {"OK" if os.getenv('BF_USERNAME') else "MANCANTE"}<br>
    BF_PASSWORD: {"OK" if os.getenv('BF_PASSWORD') else "MANCANTE"}<br>
    BF_APP_KEY: {"OK" if os.getenv('BF_APP_KEY') else "MANCANTE"}<br>
    PORT: {os.environ.get("PORT", "5000")}
    '''
    return status

@app.route('/test-betfair')
def test_betfair():
    try:
        if not all([os.getenv('BF_USERNAME'), os.getenv('BF_PASSWORD'), os.getenv('BF_APP_KEY')]):
            return "❌ Betfair credentials mancanti"
        
        trading = APIClient(
            username=os.getenv('BF_USERNAME'),
            password=os.getenv('BF_PASSWORD'),
            app_key=os.getenv('BF_APP_KEY')
        )
        trading.login()
        markets = trading.betting.list_market_catalogue(
            filter=filters.market_filter(event_type_ids=['1']),  # Soccer
            max_results='3'
        )
        trading.logout()
        return f"✅ Betfair OK! {len(markets)} mercati caricati"
    except Exception as e:
        return f"❌ Betfair errore: {str(e)}"

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Trading Bot Betfair START!")
    app.run(host='0.0.0.0', port=port)
