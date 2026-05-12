import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- SOZLAMALAR ---
TOKEN = "7919823792:AAEUnwzBf-J2h1a-EfSWijv3T_syrOxvZiM" 
ADMIN_ID = 8323916383

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="AI-Maslahatchi faol!")

# --- TUGMALAR ---
def main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🎯 Kasb tanlash", callback_data="info_career")
    builder.button(text="🧠 Ruhiy ko'mak", callback_data="info_psycho")
    builder.button(text="📚 Foydali linklar", callback_data="info_links")
    builder.adjust(1)
    return builder.as_markup()

# --- AI JAVOBLAR MANTIQI ---
def get_ai_answer(user_message: str):
    msg = user_message.lower()
    
    # 1. Kasbga oid savollar
    if any(word in msg for word in ["kasb", "universitet", "yo'nalish", "qayerga o'qish", "imtihon"]):
        return ("🎯 **AI Maslahati:** Kelajakda IT, muhandislik va biotexnologiya sohalari juda muhim. "
                "Sizga matematika yoqsa — dasturlashni, ijod yoqsa — dizaynni tavsiya qilaman. "
                "Aniqroq ma'lumot uchun qiziqishlaringizni ayting.")

    # 2. Psixologik savollar
    elif any(word in msg for word in ["stress", "hayajon", "qo'rqinch", "uyqu", "charchadim", "tushkunlik"]):
        return ("🧠 **AI Ruhiy ko'mak:** Imtihon oldidan hayajonlanish normal holat. "
                "Har kuni kamida 8 soat uxlashga harakat qiling va darslar orasida 10 daqiqa toza havoda yuring. "
                "O'zingizga ishonish muvaffaqiyatning yarmi!")

    # 3. Salomlashish
    elif any(word in msg for word in ["salom", "assalom", "qalaysiz"]):
        return "Vaalaykum assalom! Men AI-Maslahatchiman. Sizga qanday yordam bera olaman?"

    # 4. Agar javob topilmasa
    return None

# --- BOT HANDLERLARI ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(f"🌟 Salom {message.from_user.first_name}! Men AI-Maslahatchiman. "
                         "Menga savolingizni yozing yoki tugmalardan foydalaning.", 
                         reply_markup=main_menu())

@dp.callback_query(F.data.startswith("info_"))
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "info_career":
        text = "Kasb tanlash bo'yicha savolingizni yozib yuboring (masalan: 'qaysi kasb yaxshi?')."
    elif callback.data == "info_psycho":
        text = "Ruhiy holatingiz haqida yozing (masalan: 'imtihondan qo'rqyapman')."
    else:
        text = "Foydali saytlar: my.uzbmb.uz, khanacademy.org"
    await callback.message.answer(text)
    await callback.answer()

@dp.message()
async def ai_message_handler(message: types.Message):
    answer = get_ai_answer(message.text)
    
    if answer:
        # Bot mustaqil javob beradi
        await message.answer(f"🤖 **AI Javobi:**\n\n{answer}", parse_mode="Markdown")
        
        # Adminga hisobot
        report = (f"👤 **O'quvchi:** {message.from_user.full_name}\n"
                  f"💬 **Savol:** {message.text}\n"
                  f"✅ **Bot javob berdi.**")
        await bot.send_message(ADMIN_ID, report)
    else:
        # Bot javob topa olmasa, sizga yo'naltiradi
        await message.answer("🤔 Bu savolga aniq javob bera olmayman. Xabaringizni Otabek Botirovga yubordim.")
        await bot.send_message(ADMIN_ID, f"📩 **YANGI MUROJAAT (Bot javob topolmadi):**\n\n"
                                         f"👤 Kimdan: {message.from_user.full_name}\n"
                                         f"📝 Matn: {message.text}")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
