from django import template
from cart.models import Order

register = template.Library()


@register.filter
def cart_total(user):
    order = Order.objects.filter(user=user, ordered=False)
    return order[0].items.count() if order.exists() else 0
