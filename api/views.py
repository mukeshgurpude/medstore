from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from medicines.models import Medicine, MedCat
from . import serializers
from django.core.serializers.json import Serializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.

# API Version 1
# Without rest framework


class MedicineView(View):

    def get_queryset(self, *args, **kwargs):
        return Medicine.objects.all()

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serialized = Serializer().serialize(qs, fields=('name', 'price'))
        return JsonResponse(serialized, safe=False)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        s = serializers.MedicineSerializer(data=request.POST)
        print(s.is_valid())
        return HttpResponse('yes')

