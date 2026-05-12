import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# --- SOZLAMALAR ---
TOKEN = "7919823792:AAE0i-8p4A777M9zq70IxhTl2DE4-8VzV8Y"
ADMIN_ID = 8323916383

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

class AdvisorForm(StatesGroup):
    yonalish = State()
    ism = State()
    savol = State()

async def handle(request):
    return web.Response(text="Maslahatchi boti faol!")

# --- TUGMALAR ---
def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🎯 Kasbga yo'naltirish")
    builder.button(text="🧠 Psixologik maslahat")
    builder.button(text="👨‍👩‍👧 Ota-onalar uchun") # Yangi
    builder.button(text="⚡ Tezkor javoblar")
    builder.button(text="📚 Foydali resurslar") # Yangi
    builder.button(text="💡 Taklif yuborish")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_faq_buttons():
    builder = InlineKeyboardBuilder()
    builder.button(text="❓ Maslahatchi kim?", callback_data="faq_who")
    builder.button(text="👤 6-maktab maslahatchisi", callback_data="faq_otabek")
    builder.button(text="📝 Murojaat namunasi", callback_data="faq_sample")
    builder.button(text="🔙 Orqaga", callback_data="faq_back")
    builder.adjust(1)
    return builder.as_markup()

# --- BOT LOGIKASI ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!\n"
        "Men — 6-maktab maslahatchisi Otabek Botirovning raqamli yordamchisiman.",
        reply_markup=get_main_menu()
    )

# Foydali resurslar bo'limi
@dp.message(F.text == "📚 Foydali resurslar")
async def show_links(message: types.Message):
    links_text = (
        "🌐 **Foydali saytlar ro'yxati:**\n\n"
        "1. [My.uzbmb.uz](https://my.uzbmb.uz) — OTMga hujjat topshirish.\n"
        "2. [Khan Academy](https://uz.khanacademy.org) — Bepul onlayn darslar.\n"
        "3. [Edu.uz](https://t.me/eduuz) — Oliy ta'lim vazirligi kanali.\n"
        "4. [Kasbim.uz](https://kasbim.uz) — Kasb tanlash bo'yicha platforma."
    )
    await message.answer(links_text, parse_mode="Markdown", disable_web_page_preview=True)

# Ota-onalar bo'limi
@dp.message(F.text == "👨‍👩‍👧 Ota-onalar uchun")
async def parents_section(message: types.Message):
    text = (
        "👨‍👩‍👧 **Hurmatli ota-onalar!**\n\n"
        "Farzandingiz ta'limi va psixologiyasi bo'yicha maslahatlarimiz:\n"
        "• Farzand bilan do'stona muloqot o'rnatish sirlari.\n"
        "• Kasb tanlashda ularga qanday bosim o'tkazmaslik kerak?\n"
        "• Imtihon davridagi stressni birgalikda yengish.\n\n"
        "Savollaringiz bo'lsa, 'Psixologik maslahat' bo'limi orqali yozishingiz mumkin."
    )
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text == "⚡ Tezkor javoblar")
async def show_faq(message: types.Message):
    await message.answer("Sizni qiziqtirgan savolni tanlang:", reply_markup=get_faq_buttons())

@dp.callback_query(F.data.startswith("faq_"))
async def faq_answer(callback: types.CallbackQuery):
    if callback.data == "faq_who":
        text = "Maslahatchi — o'quvchilarning maktab hayotiga moslashishi va to'g'ri kasb tanlashiga ko'maklashuvchi mutaxassisdir."
    elif callback.data == "faq_otabek":
        text = "6-maktab maslahatchisi: Otabek Bakhtiyorovich Botirov. STEM va zamonaviy ta'lim bo'yicha mutaxassis."
    elif callback.data == "faq_sample":
        text = ("📝 **Murojaat namunasi:**\n\n"
                "\"Ismim Ali, 11-sinfman. Matematikaga qiziqaman, lekin qaysi universitetga topshirishni bilmayapman. Shu bo'yicha maslahat bera olasizmi?\"")
    elif callback.data == "faq_back":
        await callback.message.delete()
        await callback.message.answer("Asosiy menyu:", reply_markup=get_main_menu())
        return
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_faq_buttons())
    await callback.answer()

# Murojaat yuborish (oldingidek)
@dp.message(F.text.in_(["🎯 Kasbga yo'naltirish", "🧠 Psixologik maslahat", "💡 Taklif yuborish"]))
async def select_category(message: types.Message, state: FSMContext):
    await state.update_data(yonalish=message.text)
    await message.answer("Ism-familiyangizni yozing:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AdvisorForm.ism)

@dp.message(AdvisorForm.ism)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer("Murojaatingizni batafsil yozib yuboring:")
    await state.set_state(AdvisorForm.savol)

@dp.message(AdvisorForm.savol)
async def get_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    report = (f"📩 **YANGI MUROJAAT!**\n\n"
              f"📂 **Yo'nalish:** {data['yonalish']}\n"
              f"👤 **Kimdan:** {data['ism']}\n"
              f"📝 **Matn:** {message.text}\n"
              f"🔗 **User:** @{message.from_user.username or 'yo-q'}")
    try:
        await bot.send_message(ADMIN_ID, report, parse_mode="Markdown")
        await message.answer("Rahmat! Murojaatingiz Otabek Botirovga yetkazildi.", reply_markup=get_main_menu())
    except:
        await message.answer("Xatolik! Adminga xabar yuborishda muammo bo'ldi.", reply_markup=get_main_menu())
    await state.clear()

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
