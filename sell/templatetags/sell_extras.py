from django import template
import decimal

register = template.Library()


@register.simple_tag
def render_item_price(item):
    return decimal.Decimal(decimal.Decimal(item.price) / decimal.Decimal(1.3)).quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_UP)
