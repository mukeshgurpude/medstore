from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from cart.models import CartItem, Order
from django.views.generic import View
from django.contrib.auth import get_user_model

User = get_user_model()


class CartView(View):

    @classmethod
    def update_item(cls, pk: int = None, action: str = None,
                    order: Order = None, user: User = None) -> dict:
        """
        Utility function to update the quantity of the cart item

        :param pk: ID of the medicine
        :type pk: int
        :param action: Action specifier (increase | decrease)
        :type action: str
        :param order: Order to store the cart items
        :type order: Order
        :param user: User to create an cart item, if not already exists
        :type user: User
        :rtype: dict
        """
        try:
            c = CartItem.objects.get(item_id=pk)
            c.quantity += 1 if action == 'increase' else -1 if action == 'decrease' else 0
            if c.quantity == 0:
                c.delete()
            else:
                c.save()

        except ObjectDoesNotExist:
            c = CartItem.objects.create(item_id=pk, user=user)
            if order:
                order.items.add()
            elif user:
                try:
                    active_order = Order.objects.get(user=user, ordered=False)
                except ObjectDoesNotExist:
                    active_order = Order.objects.create(user=user)
                active_order.items.add(c)
        return c.as_json

    def get(self, request: HttpRequest):
        try:
            active_order: Order = Order.objects.get(user=self.request.user.id, ordered=False)
            if active_order:
                return JsonResponse({'msg': active_order.__str__(), 'items': active_order.as_json})
        except ObjectDoesNotExist:
            return JsonResponse({'msg': 'No items in cart', 'items': []})

    # noinspection PyArgumentList,PyArgumentList
    def post(self, request):
        """
        Request format, {id: Medicine id, action: (increase | decrease)}

        :param request: http request
        :type request: HttpRequest
        :return: Info, if the items are updated
        :rtype: JsonResponse
        """
        if request.user.is_anonymous:
            return JsonResponse({'msg': 'User not logged in'}, status=400)
        try:
            active_order: Order = Order.objects.get(user=request.user.id, ordered=False)
        except ObjectDoesNotExist:
            active_order: Order = Order.objects.create(user=request.user)
        data = self.update_item(pk=request.POST.get(key='id'),
                                action=request.POST.get(key='action'),
                                order=active_order, user=request.user)
        return JsonResponse({'msg': 'Operation successful', 'detail': data})
