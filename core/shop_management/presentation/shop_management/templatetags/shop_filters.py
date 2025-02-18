from django import template

from core.shop_management.presentation.shop_management.models import Product

from datetime import datetime, timedelta

register = template.Library()

@register.filter
def int_to_range(value: int) -> range:
    return range(int(value))
    
@register.filter
def subtract(value1: int, value2: int) -> int:
    return value1 - value2

@register.simple_tag
def get_price_with_discount(full_price: int, discount: float):
    try:
        full_price = int(full_price)
        discount = float(discount)
        return "{:.2f}".format(full_price - (full_price / 100) * discount)
    except ValueError:
        return "Invalid data"
    
@register.filter
def get_status_of_new(item: Product) -> bool:
    if isinstance(item, Product):
        yesterday = datetime.today() - timedelta(weeks=1)
            
        if item.time_created.timestamp() >= yesterday.timestamp():
            return True
        else:
            return False
    return ''
    