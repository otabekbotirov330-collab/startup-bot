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
    return web.Response(text="Bot faol!")

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
    builder.button(text="👤 6-maktab maslahatchisi", callback_data="faq_otabek")
    builder.button(text="🔙 Orqaga", callback_data="faq_back")
    builder.adjust(1)
    return builder.as_markup()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Men 6-maktab maslahatchisi botiman.", reply_markup=get_main_menu())

@dp.message(F.text == "⚡ Tezkor javoblar")
async def show_faq(message: types.Message):
    await message.answer("Savolni tanlang:", reply_markup=get_faq_buttons())

@dp.callback_query(F.data.startswith("faq_"))
async def faq_answer(callback: types.CallbackQuery):
    if callback.data == "faq_who":
        text = "Maslahatchi — o'quvchilarga yo'l ko'rsatuvchi mutaxassisdir."
    elif callback.data == "faq_otabek":
        text = "6-maktab maslahatchisi: Otabek Bakhtiyorovich Botirov."
    elif callback.data == "faq_back":
        await callback.message.delete()
        await callback.message.answer("Asosiy menyu:", reply_markup=get_main_menu())
        return
    await callback.message.edit_text(text, reply_markup=get_faq_buttons())
    await callback.answer()

@dp.message(F.text.in_(["🎯 Kasbga yo'naltirish", "🧠 Psixologik maslahat", "💡 Taklif yuborish"]))
async def select_category(message: types.Message, state: FSMContext):
    await state.update_data(yonalish=message.text)
    await message.answer("Ism-familiyangizni yozing:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AdvisorForm.ism)

@dp.message(AdvisorForm.ism)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer("Murojaatingizni yozing:")
    await state.set_state(AdvisorForm.savol)

@dp.message(AdvisorForm.savol)
async def get_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    rep = f"📩 MUROJAAT!\nYo'nalish: {data['yonalish']}\nKimdan: {data['ism']}\nMatn: {message.text}"
    try:
        await bot.send_message(ADMIN_ID, rep)
        await message.answer("Rahmat! Yuborildi.", reply_markup=get_main_menu())
    except:
        await message.answer("Xatolik! Adminga bormadi.", reply_markup=get_main_menu())
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
