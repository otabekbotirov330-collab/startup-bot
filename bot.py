from aiogram.client.session.aiohttp import AiohttpSession

# PythonAnywhere uchun proxy sozlamasi
session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot(token=TOKEN, session=session)

# Bot tokeningizni BotFather'dan olib bu yerga yozing
TOKEN = "8701141271:AAEceh-hNzPiE4QiXZgC-4fwLs7U_Y3HtTI"

session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

# --- MENU TUGMALARI ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="📝 Ro'yxatdan o'tish"))
    builder.add(types.KeyboardButton(text="🚀 STEM Yo'riqnomalar"))
    builder.add(types.KeyboardButton(text="🧠 Test yechish"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# --- START BUYRUG'I ---
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!\n"
        "**StartUp Maktab** botiga xush kelibsiz. Bu yerda siz o'z loyihalaringizni boshlashingiz mumkin.",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# --- STEM YO'RIQNOMALAR (Inline Tugmalar) ---
@dp.message(F.text == "🚀 STEM Yo'riqnomalar")
async def stem_info(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="🤖 Robototexnika", callback_data="stem_robot"))
    builder.add(types.InlineKeyboardButton(text="🧪 Kimyo/Biologiya", callback_data="stem_lab"))
    builder.adjust(1)
    
    await message.answer("Qaysi yo'nalish bo'yicha yo'riqnoma kerak?", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("stem_"))
async def callback_stem(callback: types.CallbackQuery):
    if callback.data == "stem_robot":
        await callback.message.answer("1. Arduino platformasini o'rganing.\n2. Sensorlarni ulang.\n3. Kodni yuklang.")
    elif callback.data == "stem_lab":
        await callback.message.answer("1. Xavfsizlik qoidalarini o'qing.\n2. Reaktivlarni tayyorlang.\n3. Tajribani kuzating.")
    await callback.answer()

# --- RO'YXATDAN O'TISH (Sodda ko'rinishi) ---
@dp.message(F.text == "📝 Ro'yxatdan o'tish")
async def register(message: types.Message):
    await message.answer("Loyihangiz nomi va ismingizni yozib yuboring.\n\n*Masalan: Smart-Sug'orish, Islomov Ali*", parse_mode="Markdown")

# --- TEST QISMI ---
@dp.message(F.text == "🧠 Test yechish")
async def start_test(message: types.Message):
    await message.answer_poll(
        question="STEM nima degani?",
        options=["Science, Tech, Engineering, Math", "Sport, Team, Energy, Music", "Faqat Matematika"],
        type="quiz",
        correct_option_id=0,
        is_anonymous=False
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
