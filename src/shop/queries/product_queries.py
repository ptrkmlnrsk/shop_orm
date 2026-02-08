import sqlalchemy as sa

from sqlalchemy import func, or_
from sqlalchemy.sql import Select

from src.shop.models.order_item import OrderItem
from src.shop.models.product_discount import ProductDiscount
from src.shop.models.product import Product
from src.shop.models.category import Category

def find_product_names_longer_than_50_characters() -> Select:
    return (
        sa.select(Product.product_name).where(func.length(Product.product_name) > 50)
    )

def calculate_ratio_discounted_to_non_discounted_products():

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


def count_products_ordered_less_than_1100():
    return (
        sa.select(
            OrderItem.product_id,
            func.count().label('count'),
        ).select_from(OrderItem)
        .group_by(OrderItem.product_id)
        .having(func.count() < 1100)
        .order_by(OrderItem.product_id)
    )


def top10_percent_products():
    return (
        sa.select(
            Product.product_name,
            Product.current_price)
        .order_by(Product.current_price.desc())
        .fetch(10, percent=True, with_ties=True)
    )

def sales_per_product_name_sales_per_category():

    query = (sa.select(
        Product.category_id,
        Product.product_name,
        Category.category_name,
        OrderItem.product_id,
        OrderItem.quantity,
        func.sum(OrderItem.quantity).over(partition_by=OrderItem.product_id).label('total_sold_products'),
        func.sum(OrderItem.quantity).over(partition_by=Product.category_id).label('total_sales_by_category'))
                .select_from(Product)
                .join(OrderItem, Product.product_id==OrderItem.product_id)
                .join(Category, Product.category_id==Category.category_id)
             .distinct()
        )

    return query