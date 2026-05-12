import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- SOZLAMALAR ---
TOKEN = "7919823792:AAE0i-8p4A777M9zq70IxhTl2DE4-8VzV8Y"
ADMIN_ID = 8323916383

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="AI-Maslahatchi boti faol!")

# --- DIZAYN: INLINE TUGMALAR ---
def main_menu_inline():
    builder = InlineKeyboardBuilder()
    builder.button(text="🚀 Kasb tanlash (AI)", callback_data="ai_career")
    builder.button(text="🧘 Psixologik ko'mak", callback_data="ai_psycho")
    builder.button(text="👨‍👩‍👧 Ota-onalar bo'limi", callback_data="parents")
    builder.button(text="📚 Foydali resurslar", callback_data="links")
    builder.button(text="💡 Taklif yuborish", callback_data="suggest")
    builder.adjust(2)
    return builder.as_markup()

# --- BOT LOGIKASI ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    welcome_text = (
        f"👋 **Assalomu alaykum, {message.from_user.first_name}!**\n\n"
        "Men 6-maktabning **Intellektual Yordamchisi**man. "
        "Sizga kasb tanlash, o'qish va psixologik masalalarda "
        "darhol javob bera olaman.\n\n"
        "👇 Kerakli bo'limni tanlang:"
    )
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=main_menu_inline())

# AI Javoblar bazasi (Sizning o'rningizga bot javob beradi)
@dp.callback_query(F.data.startswith("ai_"))
async def ai_response(callback: types.CallbackQuery):
    if callback.data == "ai_career":
        text = ("🎯 **Kasb tanlash bo'yicha tavsiya:**\n\n"
                "Hozirda IT, Robototexnika va Sun'iy intellekt sohalari eng istiqbolli hisoblanadi. "
                "Agar sizga matematika yoqsa — Dasturlashni, chizmachilik yoqsa — Dizaynni tanlang.\n\n"
                "Aniqroq maslahat uchun qiziqishlaringizni yozib qoldiring!")
    elif callback.data == "ai_psycho":
        text = ("🧠 **Ruhshunos maslahati:**\n\n"
                "Imtihon oldidan hayajonlanyapsizmi? Bu tabiiy! "
                "Kuniga 8 soat uxlashni va har 45 minut darsdan keyin dam olishni unutmang. "
                "O'zingizga ishonish — muvaffaqiyatning yarmi!")
    
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=main_menu_inline())
    await callback.answer()

@dp.callback_query(F.data == "parents")
async def parents_info(callback: types.CallbackQuery):
    text = ("👨‍👩‍👧 **Ota-onalar uchun:**\n\n"
            "Farzandingizning qobiliyatini yoshligidan kuzating. "
            "Uni o'zi yoqtirmagan kasbga majburlash kelajakda uning baxtsiz bo'lishiga sabab bo'lishi mumkin. "
            "Ko'proq muloqot qiling!")
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=main_menu_inline())

@dp.callback_query(F.data == "links")
async def links_info(callback: types.CallbackQuery):
    text = ("📚 **Foydali manbalar:**\n\n"
            "• [My.uzbmb.uz](https://my.uzbmb.uz) - Imtihonlar\n"
            "• [Khan Academy](https://uz.khanacademy.org) - Onlayn darslar\n"
            "• [Coursera](https://coursera.org) - Xalqaro kurslar")
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=main_menu_inline(), disable_web_page_preview=True)

# Taklif yuborish (Sizga keladigan qism)
@dp.callback_query(F.data == "suggest")
async def suggest_start(callback: types.CallbackQuery):
    await callback.message.answer("Sinfingiz va taklifingizni yozing. Otabek Botirov uni shaxsan ko'rib chiqadi.")
    await callback.answer()

# Umumiy xabarlarni qabul qilish va Admin'ga bildirish
@dp.message()
async def handle_all_messages(message: types.Message):
    # Bu yerda bot o'quvchi bilan muloqot qiladi
    await message.reply("Xabaringiz qabul qilindi. Men uni tahlil qilyapman...")
    
    # Adminga hisobot yuborish
    report = (f"👤 **Foydalanuvchi:** {message.from_user.full_name}\n"
              f"💬 **Xabar:** {message.text}\n"
              f"🤖 *Bot avtomatik javob rejimida.*")
    await bot.send_message(ADMIN_ID, report, parse_mode="Markdown")

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
