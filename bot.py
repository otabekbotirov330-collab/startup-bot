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
TOKEN = "7919823792:AAFLA1PPeR0SBVYoxI2EGFcU6LfQ__x6Tls" 
ADMIN_ID = 8323916383

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- SAVOLLAR BAZASI (20 TA) ---
QUESTIONS = [
    "1. Texnik qurilmalarni ta'mirlash sizga yoqadimi?",
    "2. Insonlarga maslahat berishni yoqtirasizmi?",
    "3. Kompyuter dasturlarini o'rganish qiziqarli-mi?",
    "4. Tadbirlar tashkil qilishni yoqtirasizmi?",
    "5. Matematik masalalarni yechish sizga zavq beradimi?",
    "6. Yangi insonlar bilan tanishish siz uchun osonmi?",
    "7. Chizmachilik yoki dizayn bilan shug'ullanasizmi?",
    "8. Laboratoriyada tajribalar o'tkazishni xohlaysizmi?",
    "9. Jamoani boshqarish sizga yoqadimi?",
    "10. Kitob o'qish va tahlil qilishni yoqtirasizmi?",
    "11. Avtomobillar mexanizmiga qiziqasizmi?",
    "12. Kasallarga yordam berish sizni quvontiradimi?",
    "13. Iqtisodiy hisob-kitoblar bilan shug'ullanish-chi?",
    "14. Sahnada chiqish qilishdan qo'rqmaysizmi?",
    "15. Tabiat va hayvonlarni o'rganish yoqadimi?",
    "16. Chet tillarini o'rganishga moyilligingiz bormi?",
    "17. Qurilish yoki arxitektura loyihalari qiziqmi?",
    "18. Psixologik kitoblar o'qiysizmi?",
    "19. Sotuv yoki marketing sohasiga qanday qaraysiz?",
    "20. Sport bilan muntazam shug'ullanasizmi?"
]

class QuizState(StatesGroup):
    answering = State()

async def handle(request):
    return web.Response(text="Maktab maslahatchisi faol!")

# --- MENYULAR ---
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

def quiz_inline():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Ha (Yoqadi)", callback_data="score_1")
    builder.button(text="❌ Yo'q (Yoqmaydi)", callback_data="score_0")
    builder.adjust(2)
    return builder.as_markup()

# --- BOT LOGIKASI ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(f"🌟 Salom {message.from_user.first_name}!\nMen 6-maktab **Maktab maslahatchisi**man.", reply_markup=main_menu())

@dp.message(F.text == "📝 Testlar va so'rovnomalar")
async def start_quiz(message: types.Message, state: FSMContext):
    await state.update_data(current_q=0, total_score=0)
    await message.answer("🚀 **Kasbiy moyillik testi boshlandi!** (20 ta savol)\n\n" + QUESTIONS[0], reply_markup=quiz_inline())
    await state.set_state(QuizState.answering)

@dp.callback_query(QuizState.answering)
async def process_quiz(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_q = data.get('current_q')
    total_score = data.get('total_score') + int(callback.data.split("_")[1])
    
    current_q += 1
    
    if current_q < len(QUESTIONS):
        await state.update_data(current_q=current_q, total_score=total_score)
        await callback.message.edit_text(f"Savol {current_q+1}/{len(QUESTIONS)}:\n\n{QUESTIONS[current_q]}", reply_markup=quiz_inline())
    else:
        # Test yakunlandi
        await state.clear()
        result_text = ""
        if total_score >= 15:
            result_text = "🔥 **Siz faol va harakatchan yetakchisiz!** Sizga boshqaruv, IT yoki muhandislik sohalari mos keladi."
        elif total_score >= 10:
            result_text = "🎓 **Sizda intellektual salohiyat kuchli.** Ilm-fan, pedagogika yoki tibbiyot yo'nalishlarini ko'rib chiqing."
        else:
            result_text = "🎨 **Siz ijodkor va ijtimoiy insonsiz.** San'at, psixologiya yoki xizmat ko'rsatish sohalari siz uchun."
        
        await callback.message.edit_text(f"🏁 **Test yakunlandi!**\n\nTo'plangan ball: {total_score}\n\n**Xulosa:** {result_text}")
    
    await callback.answer()

@dp.message()
async def school_ai_handler(message: types.Message):
    msg = message.text.lower()
    if "salom" in msg:
        await message.answer("Assalomu alaykum! Men maktab maslahatchisiman. Sizga qanday yordam bera olaman?")
    else:
        await message.answer("🤖 *Maktab maslahatchisi tahlili:* Xabaringiz qabul qilindi. Otabek Botirovga yubordim.")
        await bot.send_message(ADMIN_ID, f"📩 {message.from_user.full_name}: {message.text}")

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
