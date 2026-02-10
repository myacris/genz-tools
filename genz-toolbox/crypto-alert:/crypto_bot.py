import requests
import time
from telegram import Bot
import asyncio

# CONFIGURATION - He needs to fill these
TELEGRAM_TOKEN = 'PASTE_YOUR_BOT_TOKEN_HERE'
CHAT_ID = 'PASTE_YOUR_CHAT_ID_HERE'
CHECK_INTERVAL = 300  # 5 minutes in seconds

# Price thresholds (in USD)
BTC_HIGH = 70000  # Alert if BTC goes above
BTC_LOW = 60000   # Alert if BTC goes below
ETH_HIGH = 4000   # Alert if ETH goes above
ETH_LOW = 3000    # Alert if ETH goes below

class CryptoAlert:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_TOKEN)
        self.last_btc = 0
        self.last_eth = 0
        
    def get_prices(self):
        """Fetch current prices from CoinGecko API (Free)"""
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum',
            'vs_currencies': 'usd'
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            return {
                'btc': data['bitcoin']['usd'],
                'eth': data['ethereum']['usd']
            }
        except Exception as e:
            print(f"Error fetching prices: {e}")
            return None
    
    async def send_alert(self, message):
        """Send Telegram message"""
        try:
            await self.bot.send_message(chat_id=CHAT_ID, text=message)
            print(f"Alert sent: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")
    
    async def check_prices(self):
        """Main logic to check and alert"""
        prices = self.get_prices()
        if not prices:
            return
        
        btc_price = prices['btc']
        eth_price = prices['eth']
        
        # Check Bitcoin
        if btc_price >= BTC_HIGH and self.last_btc < BTC_HIGH:
            await self.send_alert(f"🚀 BTC ALERT: Bitcoin is up! Current price: ${btc_price:,.2f}")
        elif btc_price <= BTC_LOW and self.last_btc > BTC_LOW:
            await self.send_alert(f"📉 BTC ALERT: Bitcoin dropped! Current price: ${btc_price:,.2f}")
        
        # Check Ethereum
        if eth_price >= ETH_HIGH and self.last_eth < ETH_HIGH:
            await self.send_alert(f"🚀 ETH ALERT: Ethereum is up! Current price: ${eth_price:,.2f}")
        elif eth_price <= ETH_LOW and self.last_eth > ETH_LOW:
            await self.send_alert(f"📉 ETH ALERT: Ethereum dropped! Current price: ${eth_price:,.2f}")
        
        self.last_btc = btc_price
        self.last_eth = eth_price
        print(f"Checked prices - BTC: ${btc_price}, ETH: ${eth_price}")
    
    async def run(self):
        """Run the bot continuously"""
        print("Crypto Alert Bot started... Monitoring BTC and ETH")
        await self.send_alert("🤖 Crypto Alert Bot is now active! Monitoring your bags...")
        
        while True:
            await self.check_prices()
            await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    bot = CryptoAlert()
    asyncio.run(bot.run())