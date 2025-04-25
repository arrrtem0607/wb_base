from sqlalchemy import String, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database.entities.core import Base

class Supplier(Base):
    __tablename__ = "suppliers"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inn: Mapped[str] = mapped_column(String, nullable=True)
    wb_profile: Mapped[str] = mapped_column("Профиль на сайте Wildberries", String, nullable=True)
    seller_name: Mapped[str] = mapped_column("Название продавца", String, nullable=True)
    product_section: Mapped[str] = mapped_column("Раздел товаров", String, nullable=True)
    product_category: Mapped[str] = mapped_column("Категория товаров", String, nullable=True)
    items_sold: Mapped[int] = mapped_column("Товаров продано", Integer, nullable=True)
    review_count: Mapped[int] = mapped_column("Количество отзывов", Integer, nullable=True)
    seller_rating: Mapped[float] = mapped_column("Рейтинг продавца", Float, nullable=True)
    percent_purchased: Mapped[float] = mapped_column("% выкупленных товаров", Float, nullable=True)
    registration_date: Mapped[DateTime] = mapped_column("Регистрация на Wildberries", DateTime, nullable=True)
    legal_address: Mapped[str] = mapped_column("Юридический адрес", String, nullable=True)
    phone_mobile: Mapped[str] = mapped_column("Рабочие телефоны мобильные", String, nullable=True)
    phone_city: Mapped[str] = mapped_column("Рабочие телефоны городские", String, nullable=True)
    email: Mapped[str] = mapped_column("Рабочие Email", String, nullable=True)
    email_alt: Mapped[str] = mapped_column("Рабочие Email дополнительный источник", String, nullable=True)
    website: Mapped[str] = mapped_column("Сайт", String, nullable=True)
    whatsapp: Mapped[str] = mapped_column("Whatsapp", String, nullable=True)
    telegram: Mapped[str] = mapped_column("Telegram", String, nullable=True)
    vk: Mapped[str] = mapped_column("VK", String, nullable=True)
    instagram: Mapped[str] = mapped_column("Instagram", String, nullable=True)
    ok: Mapped[str] = mapped_column("OK", String, nullable=True)
    avg_sales_per_day: Mapped[float] = mapped_column("Среднее количество продаваемых товаров в день", Float, nullable=True)
    company_status: Mapped[str] = mapped_column("Статус компании", String, nullable=True)
    liquidation_date: Mapped[DateTime] = mapped_column("Дата ликвидации", DateTime, nullable=True)
