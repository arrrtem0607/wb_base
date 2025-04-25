import asyncio
import aiohttp
import re
from typing import List, Dict

from utils.logger import logger


class SellerParserAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")  # Удаляем / на всякий случай
        self.session: aiohttp.ClientSession | None = None

    async def init_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def get_inns_by_links(self, links: List[str]) -> List[Dict]:
        await self.init_session()
        url = f"{self.base_url}/api/inn/by-seller-links"

        try:
            async with self.session.post(url, json={"links": links}) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data.get("results", [])
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error: {e.status} - {e.message}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return []

    async def get_seller_summary(self, seller_id: int) -> Dict:
        await self.init_session()
        url = f"{self.base_url}/api/seller/summary"
        params = {"seller_id": seller_id}

        try:
            async with self.session.get(url, params=params) as resp:
                text = await resp.text()
                if resp.status != 200:
                    print(f"❌ Ошибка MPStats [{resp.status}] для seller_id={seller_id}\nОтвет: {text}")
                    return {}
                try:
                    return await resp.json()
                except Exception as e:
                    print(f"❌ Ошибка парсинга JSON seller_id={seller_id}: {e}\nТело ответа: {text}")
                    return {}
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error: {e.status} - {e.message}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return {}

    async def get_seller_summary_safe(self, seller_id: int) -> dict:
        await self.init_session()
        url = f"{self.base_url}/api/seller/summary"
        params = {"seller_id": seller_id}

        for attempt in range(3):
            try:
                async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    text = await resp.text()

                    if resp.status == 204:
                        logger.warning(f"⛔ Нет данных по seller_id={seller_id}")
                        return {}

                    if resp.status in (202, 400) and (
                        "Ожидание очереди" in text or "один отчет" in text
                    ):
                        logger.warning(f"⏳ MPStats ограничение seller_id={seller_id}: {text.strip()}")
                        await asyncio.sleep(120)  # 🔁 ждём минуту
                        continue

                    resp.raise_for_status()
                    return await resp.json()

            except asyncio.CancelledError:
                logger.error(f"❌ CancelledError: Запрос отменён для seller_id={seller_id}")
                break
            except Exception as e:
                logger.warning(f"⚠️ Ошибка при получении summary seller_id={seller_id}: {e}")
                await asyncio.sleep(60)

        logger.error(f"❌ Не удалось получить выручку для seller_id={seller_id} после 3 попыток")
        return {}

    async def get_seller_list(self, date: str, limit: int = 500, offset: int = 0) -> List[Dict]:
        await self.init_session()
        url = f"{self.base_url}/api/seller/list?date={date}"
        results = []

        payload = {
            "startRow": offset,
            "endRow": offset + limit,
            "rowGroupCols": [],
            "valueCols": [],
            "pivotCols": [],
            "pivotMode": False,
            "groupKeys": [],
            "filterModel": {},
            "sortModel": []
        }

        try:
            async with self.session.post(url, json=payload) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    logger.warning(f"⚠️ Ошибка {resp.status} при загрузке продавцов {offset}-{offset + limit}: {text}")
                    return []

                data = await resp.json()
                items = data.get("sellers") or data.get("data") or []
                results.extend(items)

        except Exception as e:
            logger.error(f"❌ Ошибка при загрузке продавцов: {e}")
            await asyncio.sleep(2)

        logger.info(f"✅ Загружено продавцов: {len(results)}")
        return results

    async def get_all_sellers_paginated(self, date: str, max_total: int = 900000, page_size: int = 500) -> List[Dict]:
        await self.init_session()
        all_sellers = []
        offset = 0

        while offset < max_total:
            logger.info(f"📦 Загружаем продавцов {offset}–{offset + page_size}")
            url = f"{self.base_url}/api/seller/list?date={date}"

            payload = {
                "startRow": offset,
                "endRow": offset + page_size,
                "rowGroupCols": [],
                "valueCols": [],
                "pivotCols": [],
                "pivotMode": False,
                "groupKeys": [],
                "filterModel": {},
                "sortModel": []
            }

            try:
                async with self.session.post(url, json=payload) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        logger.warning(f"⚠️ Ошибка {resp.status}: {text}")
                        break

                    data = await resp.json()
                    sellers = data.get("sellers") or data.get("data") or []

                    if not sellers:
                        logger.info("📭 Продавцы закончились.")
                        break

                    all_sellers.extend(sellers)
                    offset += page_size

            except Exception as e:
                logger.error(f"❌ Ошибка при получении продавцов: {e}")
                break

        logger.info(f"✅ Всего загружено продавцов: {len(all_sellers)}")
        return all_sellers

    @staticmethod
    def extract_seller_id(link: str) -> int:
        """
        Извлекает seller_id из ссылки на продавца WB.
        Пример: https://www.wildberries.ru/seller/476021 -> 476021
        """
        match = re.search(r"/seller/(\d+)", link)
        if not match:
            raise ValueError(f"❌ Не удалось извлечь seller_id из ссылки: {link}")
        return int(match.group(1))

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
