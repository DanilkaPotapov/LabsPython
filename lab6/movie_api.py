import aiohttp
import ssl
import certifi
from config import OMDB_API_KEY, TASTEDIVE_KEY, OMDB_URL, TASTEDIVE_URL

ssl_context = ssl.create_default_context(cafile=certifi.where())

async def get_movie_data(title: str):
    params = {"t": title, "apikey": OMDB_API_KEY}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(OMDB_URL, params=params, ssl=ssl_context) as resp:
                if resp.status != 200:
                    print(f"⚠️ Ошибка OMDb HTTP: {resp.status}")
                    return None
                data = await resp.json()
                if data.get("Response") == "True":
                    return data
                else:
                    print(f"OMDb не нашёл: {title}")
                    return None
    except Exception as e:
        print("Ошибка при запросе OMDb:", e)
        return None


async def get_similar_movies(title: str, limit: int = 6):
    """Ищет похожие фильмы через TasteDive API"""
    params = {
        "q": f"movie:{title}",
        "type": "movie",
        "limit": limit,
        "info": 1,
        "k": TASTEDIVE_KEY
    }

    print("\n --- TasteDive запрос ---")
    print(f"URL: {TASTEDIVE_URL}")
    print(f"Параметры: {params}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(TASTEDIVE_URL, params=params, ssl=ssl_context) as resp:
                print(f"HTTP статус TasteDive: {resp.status}")

                if resp.status != 200:
                    print(f"Ошибка TasteDive HTTP: {resp.status}")
                    return []

                data = await resp.json()
                print(f"TasteDive ответ (первые 500 символов): {str(data)[:500]}")

                similar_data = data.get("Similar") or data.get("similar") or {}
                results = similar_data.get("Results") or similar_data.get("results") or []

                if not results:
                    print("TasteDive не вернул похожих фильмов.")
                else:
                    print(f"Найдено {len(results)} похожих фильмов.")

                return [r["Name"] if "Name" in r else r.get("name") for r in results]
    except Exception as e:
        print("Ошибка TasteDive:", e)
        return []
