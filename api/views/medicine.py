from django.http import JsonResponse
from medicines.models import Medicine
from django.core.serializers.json import Serializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from medicines.forms import CreateForm
from medicines.views import MedCreateView
# Create your views here.

# API Version 1
# Without rest framework, {#SASTA}


class CreateView(MedCreateView):
    # Inherited from MedCreateView, as to incorporate the Login required and Permission required Mixin

    def get(self, request, pk=None):
        form = CreateForm()
        fields = form.base_fields
        form_details = [field for field in fields.keys()]
        return JsonResponse({'fields': form_details}, status=200)

    def post(self, request, pk=None):
        # Same process as the MedCreateView, but with customization for the JSON response
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            fields = form.base_fields
            form_details = [field for field in fields.keys()]
            return JsonResponse({'fields': form_details}, status=200)
        med = form.save(commit=False)
        med.owner = self.request.user
        med.save()
        return JsonResponse({'msg': 'created', 'newID': med.id}, status=201)


class MedicineView(CreateView):
    # As this is inherited from { CreateView }, POST requests on this
    # view will also be able to add a new medicine
    def get_queryset(self, *args, **kwargs):
        # It's better to use this method separately, as we might want to do another queries,
        # or may need to order the data, or may need to sort the data, all of this will be
        # handled in this method

        # TODO: Handle the filters
        return Medicine.objects.all()

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serialized = Serializer().serialize(qs, fields=('name', 'price'))
        return JsonResponse(serialized, safe=False)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Just to turn off the csrf verification for this view only...
        # In future, another ( process | algorithm | method ) must be incorporated without blocking
        # the CSRF
        return super().dispatch(request, *args, **kwargs)
