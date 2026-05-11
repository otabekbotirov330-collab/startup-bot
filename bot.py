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
TOKEN = "7919823792:AAE8aj_ch76G0PT7tmS4grEprbWUlRc1bo0"
ADMIN_ID = 8323916383

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

class AdvisorForm(StatesGroup):
    yonalish = State()
    ism = State()
    savol = State()

# --- WEB SERVER ---
async def handle(request):
    return web.Response(text="Maslahatchi boti faol!")

# --- TUGMALAR ---
def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🎯 Kasbga yo'naltirish")
    builder.button(text="🧠 Psixologik maslahat")
    builder.button(text="⚡ Tezkor javoblar")
    builder.button(text="💡 Taklif yuborish")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_faq_buttons():
    builder = InlineKeyboardBuilder()
    builder.button(text="❓ Maslahatchi kim?", callback_data="faq_who")
    builder.button(text="🛠 Vazifalari nima?", callback_data="faq_tasks")
    builder.button(text="👤 6-maktab maslahatchisi", callback_data="faq_otabek")
    builder.button(text="📤 Tashabbus yuborish tartibi", callback_data="faq_how_to")
    builder.button(text="🔙 Orqaga", callback_data="faq_back")
    builder.adjust(1)
    return builder.as_markup()

# --- BOT LOGIKASI ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!\n"
        "Men — 6-maktab maslahatchisi botiman. Sizga qanday yordam bera olaman?",
        reply_markup=get_main_menu()
    )

# Tezkor javoblar bo'limi
@dp.message(F.text == "⚡ Tezkor javoblar")
async def show_faq(message: types.Message):
    await message.answer("Sizni qiziqtirgan savolni tanlang:", reply_markup=get_faq_buttons())

@dp.callback_query(F.data.startswith("faq_"))
async def faq_answer(callback: types.CallbackQuery):
    if callback.data == "faq_who":
        text = ("**Maktab maslahatchisi kim?**\n\n"
                "Bu o'quvchilarning maktabga moslashishi, to'g'ri kasb tanlashi va "
                "shaxsiy rivojlanishiga yordam beruvchi professional mutaxassisdir.")
    elif callback.data == "faq_tasks":
        text = ("**Maslahatchi qanday ishlarni bajaradi?**\n\n"
                "✅ Kasbga yo'naltirish\n"
                "✅ Psixologik ko'mak\n"
                "✅ Nizolarni hal qilish\n"
                "✅ O'quvchilar tashabbuslarini qo'llab-quvvatlash.")
    elif callback.data == "faq_otabek":
        text = ("**6-maktab maslahatchisi:**\n\n"
                "Otabek Bakhtiyorovich Botirov — tajribali pedagog-psixolog. "
                "U o'quvchilarning STEM va texnologiyalarga qiziqishlarini qo'llab-quvvatlaydi.")
    elif callback.data == "faq_how_to":
        text = ("**Tashabbuslarni qanday joylasam bo'ladi?**\n\n"
                "1️⃣ Asosiy menyudan '💡 Taklif yuborish' tugmasini bosing.\n"
                "2️⃣ Ism-familiyangiz va sinfingizni yozing.\n"
                "3️⃣ G'oya yoki taklifingizni batafsil bayon qiling.\n"
                "Sizning xabaringiz shaxsan maslahatchiga yetkaziladi.")
    elif callback.data == "faq_back":
        await callback.message.delete()
        await callback.message.answer("Asosiy menyu:", reply_markup=get_main_menu())
        return

    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_faq_buttons())
    await callback.answer()

# Murojaat yuborish logikasi
@dp.message(F.text.in_(["🎯 Kasbga yo'naltirish", "🧠 Psixologik maslahat", "💡 Taklif yuborish"]))
async def select_category(message: types.Message, state: FSMContext):
    await state.update_data(yonalish=message.text)
    await message.answer("Ism-familiyangiz va sinfingizni yozing:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AdvisorForm.ism)

@dp.message(AdvisorForm.ism)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    data = await state.get_data()
    await message.answer(f"Tushunarli. Endi '{data['yonalish']}' bo'yicha savolingizni yozing:")
    await state.set_state(AdvisorForm.savol)

@dp.message(AdvisorForm.savol)
async def get_question(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    report = (f"📩 **YANGI MUROJAAT!**\n\n"
              f"📂 **Yo'nalish:** {user_data['yonalish']}\n"
              f"👤 **Kimdan:** {user_data['ism']}\n"
              f"📝 **Murojaat:** {message.text}\n"
              f"🔗 **Username:** @{message.from_user.username or 'yo'q'}")
    await bot.send_message(ADMIN_ID, report, parse_mode="Markdown")
    await message.answer("Rahmat! Murojaatingiz yuborildi. Tez orada javob beramiz.", reply_markup=get_main_menu())
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
