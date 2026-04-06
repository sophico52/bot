import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# ВСТАВЬ СВОЙ ТОКЕН:
TOKEN = "kkritinfbot"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_scores = {}
user_results = {}

# Главное меню
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📘 Что это за специальность")],
        [KeyboardButton(text="💼 Где работать")],
        [KeyboardButton(text="🧠 Пройти тест")],
        [KeyboardButton(text="📚 Специальности колледжа")]
    ],
    resize_keyboard=True
)

# Меню после теста
menu_with_result = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📘 Что это за специальность")],
        [KeyboardButton(text="💼 Где работать")],
        [KeyboardButton(text="🧠 Пройти тест")],
        [KeyboardButton(text="📚 Специальности колледжа")],
        [KeyboardButton(text="📊 Мои результаты")]
    ],
    resize_keyboard=True
)

questions = [
    ("Ты нашел флешку в коридоре колледжа. Твои действия?", [
        "Вставлю в свой комп — вдруг там что-то интересное",
        "Отнесу преподавателю/потеряшку",
        "Выброшу, мало ли вирусы"
    ]),
    
    ("Придумай пароль для почты. Что выберешь?", [
        "qwerty123 — легко запомнить",
        "Имя кота + год рождения мамы",
        "Случайную фразу: Красный_чайник_скачет_в_19:43"
    ]),
    
    ("Друг говорит: «Мой аккаунт взломали!» Твой первый совет?", [
        "Срочно поменяй пароль на новый!",
        "Включи двухфакторную авторизацию",
        "Напиши хакеру в ответ, пусть вернет"
    ]),
    
    ("Как думаешь, зачем хакеры вообще взламывают системы?", [
        "Чтобы украсть деньги или данные",
        "Ради спортивного интереса и славы",
        "Чтобы показать, где дыра в защите"
    ]),
    
    ("Ты замечаешь, что компьютер стал тормозить. Что заподозришь первым делом?", [
        "Слишком много программ открыто",
        "Может, вирус или майнер",
        "Пора покупать новый комп"
    ]),
    
    ("Представь: ты — супергерой кибербезопасности. Какая у тебя суперсила?", [
        "Вижу все уязвимости с первого взгляда",
        "Могу зашифровать что угодно",
        "Нахожу хакеров по их следам в сети"
    ])
]

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет!\n"
        "Я помогу тебе узнать о специальности\n"
        "«Основы информационной безопасности автоматизированных систем»\n\n"
        "🔐 Выбирай, что интересно 👇",
        reply_markup=menu
    )

@dp.message(lambda message: message.text == "📘 Что это за специальность")
async def info(message: types.Message):
    await message.answer_photo(
        photo="https://cdn.pixabay.com/photo/2016/12/24/23/04/coding-1930337_1280.jpg",
        caption=(
            "🔐 **Основы информационной безопасности АС**\n\n"
            "Ты научишься:\n"
            "• Защищать сайты и базы данных\n"
            "• Шифровать информацию\n"
            "• Находить уязвимости\n"
            "• Работать с криптографией\n\n"
            "🔥 Одна из самых востребованных профессий!"
        ),
        reply_markup=menu
    )

@dp.message(lambda message: message.text == "💼 Где работать")
async def job(message: types.Message):
    await message.answer_photo(
        photo="https://cdn.pixabay.com/photo/2014/05/28/18/15/study-356137_1280.jpg",
        caption=(
            "💼 **Где работать:**\n\n"
            "• Специалист по ИБ\n"
            "• Системный администратор\n"
            "• Аналитик безопасности\n"
            "• Этичный хакер\n"
            "• IT-специалист\n\n"
            "💰 Зарплата: от 80 000 ₽"
        ),
        reply_markup=menu
    )

@dp.message(lambda message: message.text == "📚 Специальности колледжа")
async def all_specialties(message: types.Message):
    text = (
        "📚 **Специальности нашего колледжа:**\n\n"
        "🔐 Основы информационной безопасности АС\n"
        "💻 Программирование\n"
        "🎨 Веб-дизайн\n"
        "🗄️ Администрирование баз данных\n""🖧 Системный администратор\n\n"
        "📍 Ждём тебя на дне открытых дверей!"
    )
    await message.answer(text, reply_markup=menu)

@dp.message(lambda message: message.text == "🧠 Пройти тест")
async def start_test(message: types.Message):
    await message.answer_photo(
        photo="https://cdn.pixabay.com/photo/2019/03/19/13/15/monkey-4065723_1280.jpg",
        caption=(
            "🎯 **Проверим, подходит ли тебе ОИБ?**\n\n"
            "Отвечай честно — всего 6 вопросов. Поехали! 🚀"
        )
    )
    user_scores[message.from_user.id] = {"score": 0, "q": 0}
    await ask_question(message)

@dp.message(lambda message: message.text == "📊 Мои результаты")
async def show_results(message: types.Message):
    user_id = message.from_user.id
    
    if user_id in user_results:
        score = user_results[user_id]
        
        if score <= 5:
            result = "🫣 Пока не очень подходит. Присмотрись к другим специальностям колледжа!"
        elif score <= 10:
            result = "👍 Стоит попробовать! У тебя есть задатки."
        else:
            result = "🔥 Отлично подходит! ОИБ — твоё направление!"
        
        await message.answer(
            f"📊 Твой результат: {score} из 18\n\n{result}",
            reply_markup=menu_with_result
        )
    else:
        await message.answer(
            "🤔 Ты ещё не проходил тест!\nНажми «🧠 Пройти тест»",
            reply_markup=menu
        )

async def ask_question(message):
    user = user_scores[message.from_user.id]
    q = user["q"]

    if q < len(questions):
        question, answers = questions[q]
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=a)] for a in answers],
            resize_keyboard=True
        )
        await message.answer(f"{q+1}️⃣ {question}", reply_markup=keyboard)
    else:
        score = user["score"]
        user_results[message.from_user.id] = score
        
        if score <= 5:
            result = "🫣 Пока не очень подходит. Присмотрись к другим специальностям колледжа!"
        elif score <= 10:
            result = "👍 Стоит попробовать! У тебя есть задатки."
        else:
            result = "🔥 Отлично подходит! ОИБ — твоё направление!"
        
        await message.answer(
            f"🎯 Результат: {score} из 18\n\n{result}\n\n📊 Нажми «Мои результаты», чтобы посмотреть их позже",
            reply_markup=menu_with_result
        )

@dp.message()
async def answers(message: types.Message):
    user_id = message.from_user.id

    if user_id in user_scores:
        user = user_scores[user_id]

        if message.text in [
            "Отнесу преподавателю/потеряшку",
            "Случайную фразу: Красный_чайник_скачет_в_19:43",
            "Включи двухфакторную авторизацию",
            "Чтобы показать, где дыра в защите",
            "Может, вирус или майнер",
            "Вижу все уязвимости с первого взгляда"
        ]:
            user["score"] += 3
        
        elif message.text in [
            "Вставлю в свой комп — вдруг там что-то интересное",
            "Имя кота + год рождения мамы",
            "Срочно поменяй пароль на новый!",
            "Чтобы украсть деньги или данные",
            "Слишком много программ открыто",
            "Могу зашифровать что угодно"
        ]:
            user["score"] += 1
        
        user["q"] += 1
        await ask_question(message)

async def main():
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())