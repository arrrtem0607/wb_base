from sqlalchemy import (
    Integer, String, Float, Date, Boolean
)
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from database.entities.core import Base

class MPStatSeller(Base):
    __tablename__ = "mp_sellers"
    __table_args__ = {"schema": "public"}

    # PK — supplier_id
    supplier_id: Mapped[int] = mapped_column("supplier_id", Integer, primary_key=True)

    # базовые поля из списка
    name: Mapped[str] = mapped_column("name", String, nullable=True)
    inn: Mapped[str] = mapped_column("inn", String, nullable=True)
    first_date: Mapped[Date] = mapped_column("first_date", Date, nullable=True)
    position: Mapped[int] = mapped_column("position", Integer, nullable=True)

    subjects: Mapped[int] = mapped_column("subjects", Integer, nullable=True)
    subjects_with_sells: Mapped[int] = mapped_column("subjects_with_sells", Integer, nullable=True)
    subjects_with_sells_percent: Mapped[float] = mapped_column("subjects_with_sells_percent", Float, nullable=True)

    items: Mapped[int] = mapped_column("items", Integer, nullable=True)
    items_with_count: Mapped[int] = mapped_column("items_with_count", Integer, nullable=True)
    items_with_sells: Mapped[int] = mapped_column("items_with_sells", Integer, nullable=True)
    items_with_sells_percent: Mapped[float] = mapped_column("items_with_sells_percent", Float, nullable=True)

    live_items: Mapped[int] = mapped_column("live_items", Integer, nullable=True)
    items_new: Mapped[int] = mapped_column("items_new", Integer, nullable=True)
    items_new_percent: Mapped[float] = mapped_column("items_new_percent", Float, nullable=True)
    items_new_with_sells: Mapped[int] = mapped_column("items_new_with_sells", Integer, nullable=True)
    items_new_with_sells_percent: Mapped[float] = mapped_column("items_new_with_sells_percent", Float, nullable=True)

    brands: Mapped[int] = mapped_column("brands", Integer, nullable=True)
    brands_with_sells: Mapped[int] = mapped_column("brands_with_sells", Integer, nullable=True)
    brands_with_sells_percent: Mapped[float] = mapped_column("brands_with_sells_percent", Float, nullable=True)

    most_frequent_country: Mapped[str] = mapped_column("most_frequent_country", String, nullable=True)

    sales: Mapped[int] = mapped_column("sales", BIGINT, nullable=True)
    balance: Mapped[float] = mapped_column("balance", Float, nullable=True)
    revenue: Mapped[float] = mapped_column("revenue", Float, nullable=True)
    revenue_potential: Mapped[float] = mapped_column("revenue_potential", Float, nullable=True)
    lost_profit: Mapped[float] = mapped_column("lost_profit", Float, nullable=True)
    lost_profit_percent: Mapped[float] = mapped_column("lost_profit_percent", Float, nullable=True)

    min_price: Mapped[float] = mapped_column("min_price", Float, nullable=True)
    min_price_with_sells: Mapped[float] = mapped_column("min_price_with_sells", Float, nullable=True)
    max_price: Mapped[float] = mapped_column("max_price", Float, nullable=True)
    max_price_with_sells: Mapped[float] = mapped_column("max_price_with_sells", Float, nullable=True)

    avg_price: Mapped[float] = mapped_column("avg_price", Float, nullable=True)
    avg_price_with_sells: Mapped[float] = mapped_column("avg_price_with_sells", Float, nullable=True)
    median_price: Mapped[float] = mapped_column("median_price", Float, nullable=True)
    median_price_with_sells: Mapped[float] = mapped_column("median_price_with_sells", Float, nullable=True)

    avg_rating: Mapped[float] = mapped_column("avg_rating", Float, nullable=True)
    avg_rating_with_sells: Mapped[float] = mapped_column("avg_rating_with_sells", Float, nullable=True)

    turnover_in_days: Mapped[int] = mapped_column("turnover_in_days", Integer, nullable=True)
    frozen_stocks: Mapped[int] = mapped_column("frozen_stocks", BIGINT, nullable=True)
    frozen_stocks_cost: Mapped[float] = mapped_column("frozen_stocks_cost", Float, nullable=True)
    frozen_stocks_percent: Mapped[float] = mapped_column("frozen_stocks_percent", Float, nullable=True)

    purchase: Mapped[float] = mapped_column("purchase", Float, nullable=True)
    purchase_after_return: Mapped[float] = mapped_column("purchase_after_return", Float, nullable=True)

    sells_on_ozon: Mapped[int] = mapped_column("sells_on_ozon", Integer, nullable=True)
    wb_rating: Mapped[float] = mapped_column("wb_rating", Float, nullable=True)
    wb_user_valuation: Mapped[float] = mapped_column("wb_user_valuation", Float, nullable=True)

    feedback_count: Mapped[int] = mapped_column("feedback_count", Integer, nullable=True)
    delivery_duration: Mapped[float] = mapped_column("delivery_duration", Float, nullable=True)
    ratio_mark_supp: Mapped[float] = mapped_column("ratio_mark_supp", Float, nullable=True)

    is_premium: Mapped[bool] = mapped_column("is_premium", Boolean, nullable=True)
    supplier_loyalty_program_level: Mapped[int] = mapped_column(
        "supplier_loyalty_program_level", Integer, nullable=True
    )

    # ваши дополнительные поля
    phone: Mapped[str] = mapped_column("Телефон", String, nullable=True)
    status: Mapped[str] = mapped_column("Статус", String, nullable=True)
    comment: Mapped[str] = mapped_column("Комментарий", String, nullable=True)
    manager: Mapped[str] = mapped_column("Менеджер", String, nullable=True)
