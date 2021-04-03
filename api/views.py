from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from medicines.models import Medicine, MedCat
from . import serializers
from django.core.serializers.json import Serializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from medicines.forms import CreateForm
from medicines.views import MedCreateView
# Create your views here.

# API Version 1
# Without rest framework, #SASTA


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


class CreateView(MedCreateView):

    def get(self, request, pk=None):
        form = CreateForm()
        fields = form.base_fields
        form_details = [field for field in fields.keys()]
        return JsonResponse({'fields': form_details}, status=200)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            print(form)
            fields = form.base_fields
            form_details = [field for field in fields.keys()]
            return JsonResponse({'fields': form_details}, status=200)
        med = form.save(commit=False)
        med.owner = self.request.user
        med.save()
        return JsonResponse({'msg': 'created', 'newID': med.id}, status=201)


# INFO: This function will return current user details in json format
def get_current_user(request):
    """
    TODO: Add DocString
    """
    if request.method != 'GET':
        return JsonResponse({'msg': 'Invalid request'}, status=400)

    user = request.user

    if user.is_anonymous:
        return JsonResponse({'name': 'Anonymous', 'loggedIn': not user.is_anonymous}, status=200)
    else:
        return JsonResponse({'full_name': request.user.get_full_name(),
                             'short_name': request.user.get_short_name(),
                             'email': request.user.email,
                             'loggedIn': not user.is_anonymous
                             }, status=200)
