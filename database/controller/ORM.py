# database/controller/ORM.py

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect, text, select
from dotenv import load_dotenv
import functools
import re

from utils.seller_parcer_api import SellerParserAPI
from utils.logger import setup_logger
from database.entities.core import Database, Base
from database.entities.models import MPStatSeller

load_dotenv()
logger = setup_logger(__name__)

def session_manager(method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        async with self.db.session() as session:
            async with session.begin():
                try:
                    result = await method(self, session, *args, **kwargs)
                    await session.commit()
                    logger.info(f"✅ {method.__name__} выполнена успешно")
                    return result
                except Exception as e:
                    await session.rollback()
                    logger.error(f"❌ Ошибка в {method.__name__}: {e}", exc_info=True)
                    raise e
    return wrapper

def clean_value(val, field=None):
    if pd.isna(val) or val == 'nan':
        return None
    if isinstance(val, pd.Timestamp):
        return val.to_pydatetime()
    if isinstance(val, str):
        if field and field in ("registration_date", "liquidation_date"):
            if re.search(r"[A-Za-z]{2,}", val):
                return None
            try:
                dt = pd.to_datetime(val, errors='raise')
                return dt.to_pydatetime()
            except Exception:
                return None
    return val

class SuppliersORM:
    def __init__(self, db: Database = Database()):
        self.db = db

    async def ensure_tables(self):
        async with self.db.async_engine.begin() as conn:
            def check_tables(sync_conn):
                sync_conn.execute(text("SET search_path TO public"))
                inspector = inspect(sync_conn)
                return inspector.get_table_names(schema="public")

            tables = await conn.run_sync(check_tables)

            if "suppliers" not in tables:
                logger.info("📂 Таблица 'suppliers' не найдена. Создаём...")
                await conn.run_sync(Base.metadata.create_all)
                logger.info("✅ Таблица 'suppliers' успешно создана")
            else:
                logger.info("📁 Таблица 'suppliers' уже существует — пропускаем создание")

    async def import_from_excel(self, df: pd.DataFrame, batch_size: int = 100):
        if "Профиль на сайте Wildberries" not in df.columns:
            logger.error("❌ В таблице отсутствует колонка 'Профиль на сайте Wildberries'")
            return

        profile_column = "Профиль на сайте Wildberries"
        total = len(df)
        added, skipped = 0, 0

        for i in range(0, total, batch_size):
            chunk = df.iloc[i:i + batch_size]
            async with self.db.session() as session:
                existing_profiles = await self._get_existing_profiles(session, chunk[profile_column].tolist())

                new_objects = []
                for _, row in chunk.iterrows():
                    profile = clean_value(row.get(profile_column))
                    if profile in existing_profiles:
                        skipped += 1
                        continue

                    obj = Supplier(
                        inn=clean_value(row.get("ИНН")),
                        wb_profile=profile,
                        seller_name=clean_value(row.get("Название продавца")),
                        product_section=clean_value(row.get("Раздел товаров")),
                        product_category=clean_value(row.get("Категория товаров")),
                        items_sold=clean_value(row.get("Товаров продано")),
                        review_count=clean_value(row.get("Количество отзывов")),
                        seller_rating=clean_value(row.get("Рейтинг продавца")),
                        percent_purchased=clean_value(row.get("% выкупленных товаров")),
                        registration_date=clean_value(row.get("Регистрация на Wildberries"), field="registration_date"),
                        legal_address=clean_value(row.get("Юридический адрес")),
                        phone_mobile=clean_value(row.get("Рабочие телефоны мобильные")),
                        phone_city=clean_value(row.get("Рабочие телефоны городские")),
                        email=clean_value(row.get("Рабочие Email")),
                        email_alt=clean_value(row.get("Рабочие Email дополнительный источник")),
                        website=clean_value(row.get("Сайт")),
                        whatsapp=clean_value(row.get("Whatsapp")),
                        telegram=clean_value(row.get("Telegram")),
                        vk=clean_value(row.get("VK")),
                        instagram=clean_value(row.get("Instagram")),
                        ok=clean_value(row.get("OK")),
                        avg_sales_per_day=clean_value(row.get("Среднее количество продаваемых товаров в день")),
                        company_status=clean_value(row.get("Статус компании")),
                        liquidation_date=clean_value(row.get("Дата ликвидации"), field="liquidation_date")
                    )
                    new_objects.append(obj)

                session.add_all(new_objects)
                await session.commit()
                added += len(new_objects)
                logger.info(
                    f"🔹 Пакет {i // batch_size + 1}: добавлено {len(new_objects)}, пропущено {len(chunk) - len(new_objects)}")

        logger.info(f"🎉 Импорт завершён: всего добавлено {added}, пропущено {skipped}")

    async def _get_existing_profiles(self, session: AsyncSession, profiles: list[str]) -> set:
        result = await session.execute(select(Supplier.wb_profile).where(Supplier.wb_profile.in_(profiles)))
        return set(row[0] for row in result.all())

    async def update_missing_inns_once(self, api: SellerParserAPI, batch_size: int = 100) -> bool:
        async with self.db.session() as session:
            stmt = (
                select(Supplier)
                .where(Supplier.wb_profile.is_not(None), Supplier.inn.is_(None))
                .limit(batch_size)
            )
            result = await session.execute(stmt)
            suppliers_batch = result.scalars().all()

            if not suppliers_batch:
                logger.info("🟢 Все ИНН уже заполнены.")
                return False

            links = [s.wb_profile for s in suppliers_batch if s.wb_profile]

            try:
                inns_data = await api.get_inns_by_links(links)
            except Exception as e:
                logger.error(f"❌ Ошибка при запросе ИНН: {e}")
                return False

            link_to_inn = {entry['link']: entry['inn'] for entry in inns_data if entry.get('inn')}

            updated = 0
            for supplier in suppliers_batch:
                inn = link_to_inn.get(supplier.wb_profile)
                if inn:
                    supplier.inn = inn
                    updated += 1

            await session.commit()
            logger.info(f"🔄 Обновлено {updated} ИНН из {len(suppliers_batch)}")
            return True
