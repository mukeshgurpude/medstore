from django.http import JsonResponse
from django.views.generic import View
from cart.models import Order


class OrderView(View):

    def get(self, request):
        """
        View to get the order details of user

        :param request: a simple HTTP GET request
        :type request: HttpRequest
        :return: orders by the logged in user
        :rtype: JsonResponse
        """
        orders = Order.objects.filter(user=self.request.user)
        json_data = [order.as_json for order in orders]
        return JsonResponse({'msg': 'Data retrieved', 'orders': json_data})
