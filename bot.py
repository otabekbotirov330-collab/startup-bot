import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- SOZLAMALAR ---
TOKEN = "7919823792:AAEUnwzBf-J2h1a-EfSWijv3T_syrOxvZiM" 
ADMIN_ID = 8323916383

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="Maktab maslahatchisi faol!")

# --- DOIMIY MENYU (1-USUL) ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🎯 Kasb tanlash")
    builder.button(text="🧠 Ruhiy ko'mak")
    builder.button(text="👨‍👩‍👧 Ota-onalar uchun")
    builder.button(text="👨‍🏫 O'qituvchilar uchun")
    builder.button(text="📝 Testlar va so'rovnomalar")
    builder.button(text="📚 Foydali linklar")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# --- AI JAVOBLAR MANTIQI ---
def get_school_ai_answer(user_message: str):
    msg = user_message.lower()
    
    if any(word in msg for word in ["kasb", "universitet", "yo'nalish", "o'qish"]):
        return ("🎯 **Maktab maslahatchisi:** Kelajak kasblari IT va muhandislik bilan bog'liq. "
                "Qaysi fanlarga qiziqishingizni aytsangiz, aniqroq universitet tavsiya qilaman.")

    elif any(word in msg for word in ["stress", "qo'rqinch", "hayajon", "charchadim"]):
        return ("🧠 **Maktab maslahatchisi:** Imtihon stressini yengish uchun nafas mashqlarini bajaring. "
                "O'zingizga bo'lgan ishonchni aslo yo'qotmang, biz sizga ishonamiz!")

    elif any(word in msg for word in ["salom", "assalom", "qalaysiz"]):
        return "Vaalaykum assalom! Men maktab maslahatchisining raqamli yordamchisiman. Sizga qanday yordam bera olaman?"

    return None

# --- BOT HANDLERLARI ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        f"🌟 Salom {message.from_user.first_name}!\nMen 6-maktabning **Maslahatchi Boti**man. "
        "Sizga o'qishingiz va kelajagingizda yordam berishga tayyorman.", 
        reply_markup=main_menu()
    )

# Bo'limlar uchun maxsus javoblar
@dp.message(F.text == "👨‍👩‍👧 Ota-onalar uchun")
async def parents_info(message: types.Message):
    await message.answer("👨‍👩‍👧 **Ota-onalar uchun maslahatlar:**\n\nFarzandingizning qobiliyatini yoshligidan kuzating. "
                         "Unga kasb tanlashda do'stona maslahat bering, majburlamang.")

@dp.message(F.text == "👨‍🏫 O'qituvchilar uchun")
async def teachers_info(message: types.Message):
    await message.answer("👨‍🏫 **O'qituvchilar uchun metodik yordam:**\n\nDars jarayonida STEM va zamonaviy texnologiyalardan foydalanish "
                         "bo'yicha tavsiyalarni tez orada shu bo'limga yuklaymiz.")

@dp.message(F.text == "📝 Testlar va so'rovnomalar")
async def quiz_section(message: types.Message):
    await message.answer("📝 **Testlar bo'limi:**\n\n1. Kasbiy moyillik testi (tez kunda)\n"
                         "2. Psixologik holat testi (tez kunda)\n"
                         "3. Maktab hayoti haqida so'rovnoma")

@dp.message(F.text == "📚 Foydali linklar")
async def links_info(message: types.Message):
    await message.answer("📚 **Foydali manbalar:**\n\n• [My.uzbmb.uz](https://my.uzbmb.uz)\n• [Khan Academy](https://uz.khanacademy.org)", 
                         disable_web_page_preview=True)

# Maktab maslahatchisi nomidan AI javobi
@dp.message()
async def school_ai_handler(message: types.Message):
    answer = get_school_ai_answer(message.text)
    
    if answer:
        await message.answer(answer)
        # Adminga bildirish
        await bot.send_message(ADMIN_ID, f"👤 {message.from_user.full_name}: {message.text}\n✅ Bot javob berdi.")
    else:
        await message.answer("🤔 Bu savolga aniq javobim yo'q, lekin xabaringizni Otabek Botirovga yubordim.")
        await bot.send_message(ADMIN_ID, f"📩 **Yangi murojaat:**\n👤 {message.from_user.full_name}\n📝 {message.text}")

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
