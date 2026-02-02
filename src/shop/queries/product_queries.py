import sqlalchemy as sa

from sqlalchemy import func, or_
from sqlalchemy.sql import Select

from src.shop.models.order_item import OrderItem
from src.shop.models.product_discount import ProductDiscount
from src.shop.models.product import Product

def find_product_names_longer_than_50_characters() -> Select:
    return (
        sa.select(Product.product_name).where(func.length(Product.product_name) > 50)
    )

def calculate_ratio_discounted_to_non_discounted_products():

    # orders_with_discount_info =
    subq = (
        sa.select(
            OrderItem.order_item_id.label("order_item_id"),
            ProductDiscount.active.label("active_discount")
            )
        .select_from(OrderItem)
        .join(ProductDiscount, OrderItem.discount_id == ProductDiscount.discount_id)
        .subquery("oi_discounts")
        )


    return     (
        sa.select(
            func.sum(sa.case((subq.c.active_discount == True, 1), else_=0)).label("discounted"),
            func.sum(sa.case((subq.c.active_discount == False, 1), else_=0)).label("non_discounted")
        )
        .select_from(subq)
    )

def show_products_cheaper_than_300_and_more_expensive_than_2000():

    return (sa.select(
        Product.product_id,
        Product.product_name,
        Product.brand,
        Product.category_id,
        Product.current_price
    ).filter(or_(Product.current_price < 300, Product.current_price > 2000)))

