from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import database
import text

router = Router()

# Состояния для FSM
class EnrollmentStates(StatesGroup):
    choosing_direction = State()
    choosing_level = State()
    choosing_course = State()

class CourseStates(StatesGroup):
    viewing_directions = State()

# Кнопки для меню
menu_buttons = [
    [KeyboardButton(text="📚 Курсы")],
    [KeyboardButton(text="⭐️ Отзывы")],
    [KeyboardButton(text="✍️ Записаться на курс")],
    [KeyboardButton(text="📋 Показать записи")],
    [KeyboardButton(text="📞 Связаться с менеджером")]
]

# Меню под строкой ввода
main_menu = ReplyKeyboardMarkup(keyboard=menu_buttons, resize_keyboard=True)

# Команда /start
@router.message(Command("start"))

async def send_welcome(message: types.Message):
    user_first_name = message.from_user.first_name
    await message.answer_sticker("CAACAgIAAxkBAAEFekpmRjGBAwshG0FXj0QvNDUgwOqcNwAC6zwAAjhUwUlVH2A7hkIIGjUE")
    await message.reply(
        text.welcome_message(user_first_name),
        reply_markup=main_menu
    )

# Информация о курсах
@router.message(lambda message: message.text == "📚 Курсы")
async def course_info(message: types.Message, state: FSMContext):
    await state.update_data(direction_index=0)
    await show_direction(message, state)

async def show_direction(message_or_callback, state: FSMContext):
    data = await state.get_data()
    direction_index = data.get("direction_index", 0)

    text_message = text.courses_message(direction_index)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️", callback_data="prev_direction"), InlineKeyboardButton(text="➡️", callback_data="next_direction")]
    ])

    if isinstance(message_or_callback, types.Message):
        await message_or_callback.reply(text_message, reply_markup=keyboard)
    else:
        await message_or_callback.message.edit_text(text_message, reply_markup=keyboard)

@router.callback_query(lambda callback_query: callback_query.data in ["prev_direction", "next_direction"])
async def navigate_directions(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    direction_index = data.get("direction_index", 0)

    if callback_query.data == "prev_direction":
        direction_index = (direction_index - 1) % len(text.directions)
    elif callback_query.data == "next_direction":
        direction_index = (direction_index + 1) % len(text.directions)

    await state.update_data(direction_index=direction_index)
    await show_direction(callback_query, state)

# Отзывы студентов
@router.message(lambda message: message.text == "⭐️ Отзывы")
async def show_reviews(message: types.Message, state: FSMContext):
    await state.update_data(review_index=0)
    review_text = text.review_message(0)
    await message.reply(
        review_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️", callback_data="prev_review"), InlineKeyboardButton(text="➡️", callback_data="next_review")]
        ])
    )

# Навигация по отзывам
@router.callback_query(lambda callback_query: callback_query.data in ["prev_review", "next_review"])
async def navigate_reviews(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    review_index = data.get("review_index", 0)

    if callback_query.data == "prev_review":
        review_index = (review_index - 1) % len(text.reviews)
    elif callback_query.data == "next_review":
        review_index = (review_index + 1) % len(text.reviews)

    await state.update_data(review_index=review_index)
    review_text = text.review_message(review_index)
    await callback_query.message.edit_text(
        review_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️", callback_data="prev_review"), InlineKeyboardButton(text="➡️", callback_data="next_review")]
        ])
    )

# Запись на курс
@router.message(lambda message: message.text == "✍️ Записаться на курс")
async def enroll(message: types.Message, state: FSMContext):
    await message.reply(
        "Пожалуйста, выберите направление, которое вас интересует:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🖥️ Веб-разработка", callback_data="direction_1")],
            [InlineKeyboardButton(text="📊 Анализ данных", callback_data="direction_2")],
            [InlineKeyboardButton(text="🤖 Машинное обучение", callback_data="direction_3")]
        ])
    )
    await state.set_state(EnrollmentStates.choosing_direction)

# Выбор направления
@router.callback_query(lambda callback_query: callback_query.data.startswith("direction_"))
async def choose_direction(callback_query: types.CallbackQuery, state: FSMContext):
    direction = int(callback_query.data.split("_")[1])
    await state.update_data(direction=direction)
    await callback_query.message.edit_text(
        text.choose_level_message(direction),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👶 Для начинающих", callback_data=f"level_1_direction_{direction}")],
            [InlineKeyboardButton(text="📈 Для продвинутых", callback_data=f"level_2_direction_{direction}")],
            [InlineKeyboardButton(text="🏆 Для экспертов", callback_data=f"level_3_direction_{direction}")]
        ])
    )
    await state.set_state(EnrollmentStates.choosing_level)

# Выбор уровня
@router.callback_query(lambda callback_query: callback_query.data.startswith("level_"))
async def choose_level(callback_query: types.CallbackQuery, state: FSMContext):
    level, direction = map(int, callback_query.data.split("_")[1::2])
    await state.update_data(level=level, direction=direction)

    text_message = text.choose_course_message(direction, level)

    await callback_query.message.edit_text(
        text_message,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=course, callback_data=f"course_{i}_direction_{direction}_level_{level}") for i, course in enumerate(text.courses_data[direction][level])],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"back_to_levels_direction_{direction}")]
        ])
    )
    await state.set_state(EnrollmentStates.choosing_course)

# Возврат к уровням
@router.callback_query(lambda callback_query: callback_query.data.startswith("back_to_levels_direction_"))
async def back_to_levels(callback_query: types.CallbackQuery, state: FSMContext):
    direction = int(callback_query.data.split("_")[-1])
    await callback_query.message.edit_text(
        text.choose_level_message(direction),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👶 Для начинающих", callback_data=f"level_1_direction_{direction}")],
            [InlineKeyboardButton(text="📈 Для продвинутых", callback_data=f"level_2_direction_{direction}")],
            [InlineKeyboardButton(text="🏆 Для экспертов", callback_data=f"level_3_direction_{direction}")]
        ])
    )
    await state.set_state(EnrollmentStates.choosing_level)

# Выбор курса
@router.callback_query(lambda callback_query: callback_query.data.startswith("course_"))
async def choose_course(callback_query: types.CallbackQuery, state: FSMContext):
    course_index, direction, level = map(int, callback_query.data.split("_")[1::2])
    selected_course = text.courses_data[direction][level][course_index]
    user_id = callback_query.from_user.id

    database.add_enrollment(user_id, direction, level, selected_course)
    await callback_query.message.answer_sticker("CAACAgIAAxkBAAEFekxmRjGcRQF9QDmnqPfS3Hnm7oGokgAC6k4AAkuraUvzfpyX0S3CCzUE")
    await callback_query.message.edit_text(
        text.course_selected_message(selected_course)
    )
    await state.clear()

# Связаться с менеджером
@router.message(lambda message: message.text == "📞 Связаться с менеджером")
async def contact_manager(message: types.Message):
    await message.reply("Чтобы связаться с менеджером, напишите @edusmartmanager")

# Показать записи
@router.message(lambda message: message.text == "📋 Показать записи")
async def show_enrollments(message: types.Message):
    enrollments = database.get_enrollments()
    if not enrollments:
        await message.reply("Записей не найдено.")
        return

    response = "Курсы на которые вы записались:\n"
    for enrollment in enrollments:
        user_id, direction, level, course = enrollment
        response += f"Курс: {course}\n"

    await message.reply(response)