from django.http import JsonResponse, HttpRequest
from medicines.models import Medicine
from django.core.serializers.json import Serializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from medicines.forms import CreateForm
from medicines.views import MedCreateView

# API Version 1
# Without rest framework, {#SASTA}


class CreateView(MedCreateView):
    # Inherited from MedCreateView, as to incorporate the Login required and Permission required Mixin

    def get(self, request, pk=None):
        """
        Get the medicine details

        :param request: Request to get the current detail for medicine
        :type request: HttpRequest
        :param pk: ID of the medicine
        :return: Data of the current medicine detail
        :rtype: JsonResponse
        """
        form = CreateForm()
        fields = form.base_fields
        form_details = [field for field in fields.keys()]
        return JsonResponse({'fields': form_details}, status=200)

    def post(self, request: HttpRequest, pk=None) -> JsonResponse:
        """
        Create a medicine using formData

        :param request: request with the new medicine data
        :type request: HttpRequest
        :param pk: ID of the medicine whose, data is to be altered
        :return: Respond if the query was successful
        :rtype: JsonResponse
        """
        # TODO: handle updating of med
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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Just to turn off the csrf verification for this view only...
        # In future, another ( process | algorithm | method ) must be incorporated without blocking
        # the CSRF
        return super().dispatch(request, *args, **kwargs)


class MedicineView(View):
    # As this is inherited from { CreateView }, POST requests on this
    # view will also be able to add a new medicine
    def get_queryset(self, *args, **kwargs):
        # It's better to use this method separately, as we might want to do another queries,
        # or may need to order the data, or may need to sort the data, all of this will be
        # handled in this method

        # TODO: Handle the filters
        return Medicine.objects.all()

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """
        GET the medicines list
        :param request: request to get the list as json
        :type request: HttpRequest
        :return: List containing basic medicine data
        :rtype: JsonResponse
        """
        qs = self.get_queryset()
        serialized = Serializer().serialize(qs, fields=('name', 'price'))
        return JsonResponse(serialized, safe=False)
