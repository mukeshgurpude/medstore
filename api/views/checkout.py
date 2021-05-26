from typing import Dict, Any, Optional, Tuple
from django.views.generic import View
from django.http import HttpRequest, JsonResponse
from checkout.forms import BillingForm
from checkout.models import BillingAddress

"""
1. `configuration` view at [conf/](../../checkout/views.py)
2. `checkout session` view at [new/](../../checkout/views.py)
"""


class APIBillingAddress(View):

    @classmethod
    def get_address(cls, user) -> Tuple[Dict[Any, Optional[str]], Any]:
        instance = BillingAddress.objects.filter(user=user).first()
        if instance:
            return instance.as_json, instance
        return dict(address='', landmark='', city='', pincode=None), instance

    def get(self, request):
        """
        send the billing address details

        :param request: Request to get the billing address details
        :type request: HttpRequest
        """
        (b_json, b_address) = self.get_address(self.request.user)
        return JsonResponse({'fields': b_json})

    def post(self, request):
        """
        request to modify the bill

        :param request: Modify address
        :type request: HttpRequest
        """
        (b_json, b_address) = self.get_address(user=self.request.user)
        form = BillingForm(request.POST, instance=b_address)
        if form.is_valid():
            address: BillingAddress = form.save(commit=False)
            address.user = self.request.user
            address.save()
        (b_json, b_address) = self.get_address(self.request.user)
        return JsonResponse({'msg': 'Error returned', 'fields': b_json, 
                            'errors': form.errors or None},
                            status=400 if form.errors else 200)


# Alternative to `hook/` in `checkout/views.py`
def order_success(request):
    """
    Callback url from stripe

    :param request: Callback request from stripe
    :type request: HttpRequest
    """
    print(request.POST)
