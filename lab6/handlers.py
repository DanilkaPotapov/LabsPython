from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from movie_api import get_movie_data, get_similar_movies

router = Router()

class FilmStates(StatesGroup):
    START = State()
    INPUT_TITLE = State()
    SHOW_MOVIE = State()

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Найти фильм", callback_data="find_movie")]
    ])
    await message.answer(
        "🎬 Привет! Я FilmRecommenderBot.\n"
        "Введи название фильма, и я покажу описание и похожие фильмы.",
        reply_markup=kb
    )
    await state.set_state(FilmStates.START)


@router.callback_query(F.data == "find_movie")
async def cb_find_movie(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🎥 Введи название фильма:")
    await state.set_state(FilmStates.INPUT_TITLE)
    await callback.answer()


@router.message(FilmStates.INPUT_TITLE)
async def on_movie_title(message: Message, state: FSMContext):
    title = message.text.strip()
    await message.answer("🔎 Ищу информацию...")

    data = await get_movie_data(title)
    if not data:
        await message.answer("Такого фильма я не знаю. Попробуй другое название (лучше на английском).")
        return

    await state.update_data(current_title=data["Title"])

    text = (
        f"🎬 <b>{data['Title']}</b> ({data.get('Year', '-')})\n"
        f"⭐ IMDB: {data.get('imdbRating', '—')}\n"
        f"🎭 Жанр: {data.get('Genre', '—')}\n"
        f"🎥 Режиссёр: {data.get('Director', '—')}\n\n"
        f"{data.get('Plot', 'Описание отсутствует.')}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎞 Похожие фильмы", callback_data="show_similar")],
        [InlineKeyboardButton(text="🔎 Новый поиск", callback_data="find_movie")]
    ])

    if data.get("Poster") and data["Poster"] != "N/A":
        await message.answer_photo(data["Poster"], caption=text, parse_mode="HTML", reply_markup=kb)
    else:
        await message.answer(text, parse_mode="HTML", reply_markup=kb)

    await state.set_state(FilmStates.SHOW_MOVIE)


@router.callback_query(F.data == "show_similar")
async def cb_show_similar(callback: CallbackQuery, state: FSMContext):
    st = await state.get_data()
    title = st.get("current_title")

    await callback.message.answer("🎯 Ищу похожие фильмы...")
    similar = await get_similar_movies(title)

    if not similar:
        await callback.message.answer("😕 Не удалось найти похожие фильмы.")
        return

    for name in similar[:5]:
        data = await get_movie_data(name)
        if not data:
            await callback.message.answer(f"🎬 {name}")
            continue

        text = (
            f"🎬 <b>{data['Title']}</b> ({data.get('Year', '-')})\n"
            f"⭐ IMDB: {data.get('imdbRating', '—')}\n"
            f"{data.get('Plot', '')[:350]}..."
        )

        if data.get("Poster") and data["Poster"] != "N/A":
            await callback.message.answer_photo(data["Poster"], caption=text, parse_mode="HTML")
        else:
            await callback.message.answer(text, parse_mode="HTML")

    await callback.message.answer("🔎 Хочешь поискать ещё? /start")
    await callback.answer()
