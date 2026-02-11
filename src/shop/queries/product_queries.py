import sqlalchemy as sa

from sqlalchemy import func, or_
from sqlalchemy.sql import Select

from src.shop.models.order_item import OrderItem
from src.shop.models.order import Order
from src.shop.models.product_discount import ProductDiscount
from src.shop.models.product import Product
from src.shop.models.category import Category
from src.shop.models.store import Store

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

def product_price_and_rank():

    return (
        sa.select(
            Product.product_name,
            Product.current_price,
            func.rank().over(order_by=Product.current_price).label('price_rank'),
            func.dense_rank().over(order_by=Product.current_price).label('dense_price_rank')
        )
    )

def select_top_5_products_info():

    item_total_sell = func.sum(OrderItem.quantity).label('item_total_sell')

    subq1 = (
        sa.select(
            Product.product_id,
            item_total_sell
        ).select_from(Product)
        .join(OrderItem, Product.product_id==OrderItem.product_id)
        .join(Order, OrderItem.order_id == Order.order_id)
        .where(sa.extract('year', Order.order_date) == 2022)
        .group_by(Product.product_id)
        .order_by(item_total_sell.desc())
        .limit(5)
        .subquery('filtered_products')

    )

    subq2 = (
        sa.select(
            Product.product_id,
            Product.product_name,
            Store.store_id,
            Store.store_name,
            Product.current_price,
            OrderItem.quantity
        ).select_from(Store)
        .join(Order, Store.store_id==Order.store_id)
        .join(OrderItem, Order.order_id == OrderItem.order_id)
        .join(Product, OrderItem.product_id==Product.product_id)
        .where(sa.extract('year', Order.order_date) == 2022)
        .subquery('stores_and_products')
    )

    total_sell_per_store = func.sum(subq2.c.quantity).label("total_sell_per_store")

    full_query = (
        sa.select(
            subq1.c.product_id,
            subq2.c.product_name,
            subq2.c.store_name,
            subq2.c.current_price,
            total_sell_per_store
        ).select_from(subq2)
        .join(subq1, subq2.c.product_id==subq1.c.product_id)
        .group_by(
            subq1.c.product_id,
            subq2.c.product_name,
            subq2.c.store_name,
            subq2.c.current_price
        ).order_by(total_sell_per_store.desc())
    )

    return full_query


def count_products_within_category(product_cost: float = 1500.0):

    categories_and_products = (
        sa.select(
            Category.category_id,
            Category.category_name,
            Product.product_id,
            Product.current_price
        ).select_from(Product)
        .join(Category, Product.category_id==Category.category_id)
        .cte('categories_and_products')
    )

    counted_products = (
        sa.select(
            categories_and_products.c.category_id,
            categories_and_products.c.category_name,
            func.count(categories_and_products.c.product_id).label('product_count')
        ).where(categories_and_products.c.current_price > product_cost)
        .group_by(categories_and_products.c.category_id,
            categories_and_products.c.category_name)
        .cte('counted_products')
    )

    query = (
        sa.select(
            Category.category_name,
            sa.case((counted_products.c.product_count.is_(None), 0),
            else_=counted_products.c.product_count).label('count_of_products_greater_1500')
        ).select_from(Category)
        .join(counted_products, Category.category_id==counted_products.c.category_id, full=True)
    )

    return query