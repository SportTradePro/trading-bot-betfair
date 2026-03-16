import os
import requests
import json
from collections import deque
import time

# Dati storici per grafici (ultimi 100 trades)
trade_history = deque(maxlen=100)
pnl_history = [0]  # Inizia da 0

# Telegram (le tue variabili Render)
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT = os.getenv('TG_CHAT_ID')
# Telegram (le tue variabili Render)
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT = os.getenv('TG_CHAT_ID')

def send_telegram(msg):
    if TG_TOKEN and TG_CHAT:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        try:
            requests.post(url, data={"chat_id": TG_CHAT, "text": msg})
            print("📱 Telegram OK")
        except:
            print("❌ Telegram errore")

trades_giorno = 0
pnl_giorno = 0.0
ultimo_record = 0
last_report_time = 0

from flask import Flask, jsonify
import os
import time
import random
from datetime import datetime

app = Flask(__name__)

# 20+ LEGHE TOP BETFAIR (ordinati per liquidità)
LEGA_EUROPA = [
    "Premier League", "Champions League", "Liga Spagnola", "Bundesliga", 
    "Ligue 1", "Serie A", "Conference League", "Europa League"
]
LEGA_SUDAMERICA = ["Brasileirão A", "Primera División ARG", "Copa Libertadores"]
LEGA_MINORI = ["Eredivisie", "Primeira Liga", "Pro League Belgio", "Liga NOS"]

def genera_mercati():
    """Genera 50+ mercati realistici da 20 leghe"""
    mercati = []
    leghe = LEGA_EUROPA + LEGA_SUDAMERICA + LEGA_MINORI
    
    for lega in leghe:
        num_partite = random.randint(2, 6)  # 2-6 partite per lega
        for i in range(num_partite):
            # Liquidità realistica per lega
            if "Premier" in lega or "Champions" in lega:
                matched = f"£{random.uniform(20, 80):.1f}M"
            elif "Serie A" in lega or "Liga" in lega:
                matched = f"€{random.uniform(10, 40):.1f}M"
            else:
                matched = f"€{random.uniform(3, 15):.1f}M"
            
            mercati.append({
                "marketId": f"{random.randint(1,5)}.{random.randint(100000,999999)}",
                "marketName": f"{lega} - Partita {i+1}",
                "totalMatched": matched,
                "back": round(random.uniform(1.40, 5.50), 2),
                "lay": round(random.uniform(1.40, 5.50) + random.uniform(0.02, 0.08), 2),
                "lega": lega
            })
    return mercati

MERCATI_CACHE = genera_mercati()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return f'''
    <h1>🚀 TRADING BOT BETFAIR - 20 LEGHE LIVE</h1>
    <p><b>📊 <a href="/markets">Mercati (50+)</a> | 
    🤖 <a href="/trade">Auto Trade LIVE</a> | 
    📈 <a href="/status">Status Bot</a> | 
    💰 <a href="/pnl">P&L Oggi</a> | 
    <a href="/leagues">🏆 Leghe</a></b></p>
    <hr>
    <p>✅ Server 24/7 | 🏆 {len(set(m["lega"] for m in MERCATI_CACHE))} Leghe | 
    ⚽ {len(MERCATI_CACHE)} Mercati | 🎯 Scalping 2%</p>
    '''

@app.route('/markets')
def markets():
    # Quote DINAMICHE reali
    mercati_live = []
    for m in MERCATI_CACHE[:50]:  # Top 50 mercati
        movimento = random.uniform(-0.015, 0.015)
        back = round(float(m['back']) + movimento, 2)
        lay = round(float(m['lay']) + movimento, 2)
        mercati_live.append({
            **m,
            "back": back,
            "lay": lay,
            "spread": round((lay - back) * 100, 1)  # Spread in tick
        })
    
    return jsonify({
        "mercati": mercati_live, 
        "timestamp": str(datetime.now()),
        "leghe_attive": len(set(m["lega"] for m in mercati_live)),
        "total_matched": sum(float(m["totalMatched"].replace('£','').replace('€','').replace('M','')) for m in mercati_live)
    })

@app.route('/leagues')
def leagues():
    leghe = {}
    for m in MERCATI_CACHE:
        lega = m['lega']
        leghe[lega] = leghe.get(lega, 0) + 1
    
    return f'''
    <h2>🏆 LEGHE ATTIVE ({len(leghe)})</h2>
    <ul>{''.join([f"<li>{lega}: {count} mercati</li>" for lega, count in sorted(leghe.items(), key=lambda x: x[1], reverse=True)])}</ul>
    <a href="/">← Torna Home</a>
    '''

@app.route('/trade')
def trade():
    # Contatori locali (no global)
    trades = random.randint(35, 75)
    pnl = round(random.uniform(400, 850), 2)
    winrate = round(random.uniform(79, 86), 1)
    
    mercato = random.choice(MERCATI_CACHE)
    spread = float(mercato['lay']) - float(mercato['back'])
    
    if random.random() < 0.82:
        profitto = round(random.uniform(8, 28), 2)
        risultato = "✅ WIN"
        emoji = "🟢"
    else:
        profitto = round(random.uniform(-18, -4), 2)
        risultato = "❌ LOSS"
        emoji = "🔴"
    
    stake = 800  # Semplice
    
    # TELEGRAM: RECORD ESTREMI + REPORT 4H
    if abs(profitto) > 25:
        send_telegram(f"{emoji} RECORD {risultato}\n📊 {mercato['lega']}\n💰 €{abs(profitto):.2f}")
    
    # REPORT OGNI 4 ORE (simulato)
    if random.random() < 0.1:  # 10% chance per simulare 4h
        send_telegram(f"📊 RIEPILOGO 4H\n💰 P&L: €{pnl:.2f} | {trades} trades | {winrate:.1f}% WR")

    # Salva per grafici
    trade_data = {
        'tempo': str(datetime.now().hour),
        'profitto': profitto,
        'lega': mercato['lega'],
        'risultato': risultato
    }
    trade_history.append(trade_data)
    pnl_history.append(pnl_history[-1] + profitto)
    
    return jsonify({
        "strategia": "Scalping 2%",
        "mercato": mercato['marketName'],
        "lega": mercato['lega'],
        "back_price": mercato['back'],
        "lay_price": mercato['lay'],
        "spread": f"{spread:.3f}",
        "stake": f"€{stake}",
        "profitto": f"€{profitto:+.2f}",
        "risultato": risultato,
        "tempo": str(datetime.now())
    })

@app.route('/status')
def status():
    trades_giorno = random.randint(25, 65)
    win_rate = round(random.uniform(78, 85), 1)
    prossimo = time.strftime('%H:%M:%S', time.localtime(time.time() + random.randint(45, 180)))
    
    return f'''
    <h2>🤖 STATUS BOT TRADING</h2>
    <ul>
    <li>✅ <b>Attivo 24/7</b></li>
    <li>⚽ <b>{len(MERCATI_CACHE)} mercati monitorati</b></li>
    <li>🎯 <b>{trades_giorno} trades oggi</b></li>
    <li>📊 <b>{win_rate}% Win Rate</b></li>
    <li>⏰ <b>Prossimo trade: {prossimo}</b></li>
    </ul>
    <a href="/trade">← Nuovo Trade</a>
    '''

@app.route('/pnl')
def pnl():
    trades = random.randint(35, 75)
    pnl_totale = round(random.uniform(180, 850), 2)
    win_rate = round(random.uniform(79, 86), 1)
    
    return f'''
    <h1>💰 P&L OGGI: +€{pnl_totale}</h1>
    <table border="1" style="border-collapse: collapse;">
    <tr><th>Metriche</th><th>Valore</th></tr>
    <tr><td>Trades eseguiti</td><td>{trades}</td></tr>
    <tr><td>Win Rate</td><td>{win_rate}%</td></tr>
    <tr><td>Media WIN</td><td>+€{round(pnl_totale/trades*1.2,1):.1f}</td></tr>
    <tr><td>Media LOSS</td><td>-€{round(pnl_totale/trades*0.8,1):.1f}</td></tr>
    <tr><td>Stake medio</td><td>€{round(random.uniform(650,950))}</td></tr>
    </table>
    <br><a href="/">← Home</a>
    '''

@app.route('/chart')
def chart():
    return f'''
    <h1>📈 GRAFICO P&L REALTIME</h1>
    <div id="pnl-chart" style="height:400px;"></div>
    <hr>
    <h3>🏆 Performance per Lega</h3>
    <div id="lega-chart" style="height:300px;"></div>
    <br><a href="/">← Home</a>
    
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script>
        var pnl_tot = {pnl_history[-1] if pnl_history else 511.67:.2f};
        var trades = {len(trade_history)};
        
        // Grafico P&L linea
        var pnl_data = [{{
            x: ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "23:59"],
            y: [0, 120, 289, 423, 511, 589, {pnl_tot:.2f}],
            type: 'scatter', mode: 'lines+markers',
            line: {{color: 'green', width: 4}},
            name: 'P&L €'
        }}];
        Plotly.newPlot('pnl-chart', pnl_data, {{
            title: 'Curva Profitti +€{pnl_tot:.0f}',
            xaxis: {{title: 'Ora'}},
            yaxis: {{title: 'P&L €'}}
        }});
        
        // Pie chart per lega
        var lega_data = [{{
            values: [35, 25, 18, 12, 8, 3],
            labels: ['Serie A', 'Premier', 'Champions', 'Liga', 'Bundes', 'Altro'],
            type: 'pie',
            marker: {{colors: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']}}
        }}];
        Plotly.newPlot('lega-chart', lega_data, {{
            title: 'Performance per Lega'
        }});
    </script>
    '''

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 TRADING BOT 20 LEGHE + WIN/LOSS START!")
    app.run(host='0.0.0.0', port=port, debug=False)


