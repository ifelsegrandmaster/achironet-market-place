from django import template
import decimal

register = template.Library()

# register this tag that determines if an order has been
# dropped at the depot by the user
@register.simple_tag
def is_dropped_at_depot(order, seller):
    # get all the items of the order
    items = order.items.all().filter(seller=seller)
    # check if all the items have been received
    received_all = True
    for item in items:
        if item.received == False:
            received_all = False
            break
    # now check if the received all is still true
    if received_all:
        return '<span class="badge badge-success">Dropped at the depot</span>'

    return '<span class="badge badge-light">You haven\'t dropped the items at the depot</span>'

@register.simple_tag
def get_order_sales(order, seller):
    items = order.items.all().filter(seller=seller)
    total = sum(item.get_cost() for item in items)
    total = decimal.Decimal(decimal.Decimal(total) / decimal.Decimal(1.3)).quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_UP)
    return total