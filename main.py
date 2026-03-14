import os
import time
import betfairlightweight
from telegram import Bot

# -------------------------
# ENV VARIABLES (Railway)
# -------------------------

BF_USERNAME = os.getenv("BF_USERNAME")
BF_PASSWORD = os.getenv("BF_PASSWORD")
BF_APP_KEY = os.getenv("BF_APP_KEY")

TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

BANKROLL = float(os.getenv("BANKROLL", "1000"))

bot = Bot(token=TG_TOKEN)

# -------------------------
# BETFAIR LOGIN
# -------------------------

client = betfairlightweight.APIClient(
    BF_USERNAME,
    BF_PASSWORD,
    app_key=BF_APP_KEY
)

client.login()

# -------------------------
# TELEGRAM
# -------------------------

def send(msg):
    try:
        bot.send_message(chat_id=TG_CHAT_ID, text=msg)
    except:
        pass

# -------------------------
# KELLY
# -------------------------

def kelly(prob, odds):

    edge = prob - (1/odds)

    if edge <= 0:
        return 0

    fraction = edge / (odds - 1)

    if fraction > 0.05:
        fraction = 0.05

    return BANKROLL * fraction

# -------------------------
# EDGE MODEL (SIMPLE)
# -------------------------

def probability(book):

    prices = []

    for r in book.runners:
        if r.ex.available_to_back:
            prices.append(r.ex.available_to_back[0].price)

    if not prices:
        return 0

    avg = sum(prices) / len(prices)

    return max(0.01, min(0.9, 1/avg))

# -------------------------
# LIVE MARKETS
# -------------------------

def get_markets():

    market_filter = {
        "eventTypeIds": ["1"],
        "inPlayOnly": True,
        "marketTypeCodes": ["OVER_UNDER_25"]
    }

    markets = client.betting.list_market_catalogue(
        filter=market_filter,
        max_results=20,
        market_projection=["EVENT"]
    )

    return markets

# -------------------------
# MARKET BOOK
# -------------------------

def get_book(market_id):

    books = client.betting.list_market_book(
        market_ids=[market_id],
        price_projection={"priceData": ["EX_BEST_OFFERS"]}
    )

    if books:
        return books[0]

    return None

# -------------------------
# TRADE CHECK
# -------------------------

def check_trade(book):

    prob = probability(book)

    for r in book.runners:

        if not r.ex.available_to_back:
            continue

        odds = r.ex.available_to_back[0].price

        stake = kelly(prob, odds)

        if stake < 2:
            continue

        return r.selection_id, odds, round(stake,2), prob

    return None

# -------------------------
# EXECUTE
# -------------------------

def trade(market_id, data):

    selection, odds, stake, prob = data

    instruction = {
        "selectionId": selection,
        "side": "BACK",
        "orderType": "LIMIT",
        "limitOrder": {
            "size": stake,
            "price": odds,
            "persistenceType": "LAPSE"
        }
    }

    try:

        client.betting.place_orders(
            market_id=market_id,
            instructions=[instruction]
        )

        send(f"""
TRADE

Odds: {odds}
Stake: {stake}
Prob: {round(prob,2)}
""")

    except Exception as e:
        send(f"Errore trade {e}")

# -------------------------
# MAIN LOOP
# -------------------------

def run():

    send("Bot avviato")

    while True:

        try:

            markets = get_markets()

            for m in markets:

                book = get_book(m.market_id)

                if not book:
                    continue

                t = check_trade(book)

                if t:
                    trade(m.market_id, t)

                time.sleep(1)

        except Exception as e:
            send(f"Errore {e}")

        time.sleep(10)

if __name__ == "__main__":
    run()
