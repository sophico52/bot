import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# ВСТАВЬ СВОЙ ТОКЕН:
TOKEN = "8693867728:AAG9hCdey_BqRehGmBrJLonG0C-yxkAyb6Y"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_scores = {}
user_results = {}
user_states = {}  # Для отслеживания состояния пользователя

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

# Правильные ответы и баллы
correct_answers = {
    0: ("Отнесу преподавателю/потеряшку", 3),
    1: ("Случайную фразу: Красный_чайник_скачет_в_19:43", 3),
    2: ("Включи двухфакторную авторизацию", 3),
    3: ("Чтобы показать, где дыра в защите", 3),
    4: ("Может, вирус или майнер", 3),
    5: ("Вижу все уязвимости с первого взгляда", 3)
}

def get_result_text(score: int) -> str:
    """Возвращает текст результата по количеству баллов"""
    if score <= 5:
        return "🫣 Пока не очень подходит. Присмотрись к другим специальностям колледжа!"
    elif score <= 10:
        return "👍 Стоит попробовать! У тебя есть задатки."
    else:
        return "🔥 Отлично подходит! ОИБ — твоё направление!"

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
        "🗄️ Администрирование баз данных\n"
        "🖧 Системный администратор\n\n"
        "📍 Ждём тебя на дне открытых дверей!"
    )
    await message.answer(text, reply_markup=menu)

@dp.message(lambda message: message.text == "🧠 Пройти тест")
async def start_test(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = "taking
