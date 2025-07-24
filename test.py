import telegram
import asyncio

# --- 설정 (사용자 환경에 맞게 수정) ---
TELEGRAM_BOT_TOKEN = "8087893994:AAHNutdMob-8HI4yVY6HTBNUCXPDrpVK_t0" 
TELEGRAM_CHAT_ID = "1338893598"


bot = telegram.Bot(TELEGRAM_BOT_TOKEN)

async def main():
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Hello, Bot!")

if __name__ == "__main__":
    asyncio.run(main())