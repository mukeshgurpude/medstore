from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.http import JsonResponse, HttpRequest
from medicines.models import Medicine
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from medicines.forms import CreateForm

# API Version 1

class MedicineView(View):
    @classmethod
    def get_queryset(cls, filters=None):
        # It's better to use this method separately, as we might want to do another queries,
        # or may need to order the data, or may need to sort the data, all of this will be
        # handled in this method
        """
        Expected keys:
            owner | category | price__lt | price__gt | quantity__gt | quantity__lt
        """
        m = Medicine.objects.all()
        for key, value in filters.items():
            try:
                if key == 'owner':
                    m = m.filter(owner__sellerprofile__store_name=value)
                elif key == 'category':
                    m = m.filter(category__name=value)
                else:
                    m = m.filter(key=value)
            except (FieldError, ValueError):
                pass
        return m

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """
        GET the medicines list
        :param request: request to get the list as json
        :type request: HttpRequest
        :return: List containing basic medicine data
        :rtype: JsonResponse
        """
        qs = self.get_queryset(request.GET)

        json = {med.id: {'name': med.name,
                         'price': med.price,
                         'category': med.category.name
                         } for med in qs}

        return JsonResponse(json)

    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Create a medicine using formData

        :param request: request with the new medicine data
        :type request: HttpRequest
        :return: Respond if the query was successful
        :rtype: JsonResponse
        """

        if not self.request.user.has_perm('medicines.add_medicine'):
            return JsonResponse({'msg': "You don't have permission to update medicines"}, status=400)
        # Same process as the MedCreateView, but with customization for the JSON response
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            return JsonResponse({'msg': 'This form has invalid data', 'errors': form.errors}, status=200)

        # Check if this request is duplicated

        temp = Medicine.objects.filter(name=form.data['name'], owner=self.request.user)

        if temp:
            return JsonResponse({'msg': 'No two medicines by the same owner can have the same'
                                        'name'}, status=400)

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


class APIDetailView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    @classmethod
    def get_med(cls, pk=None, slug=None):
        if pk is not None:
            med: Medicine = Medicine.objects.get(id=pk)
        else:
            med: Medicine = Medicine.objects.get(slug__exact=slug)
        return med

    def get(self, request, pk=None, slug=None):
        try:
            med = self.get_med(pk=pk, slug=slug)
            return JsonResponse(med.as_json)
        except ObjectDoesNotExist:
            return JsonResponse({'msg': 'Medicine not found'}, status=404)

    def post(self, request, pk=None, slug=None):
        try:
            med: Medicine = self.get_med(pk=pk, slug=slug)
            f = CreateForm(request.POST or None, request.FILES or None, instance=med)
            if f.is_valid():
                f.save()
                return JsonResponse({'msg': 'Got it', 'name': med.name})
            else:
                return JsonResponse({'msg': "No, you can't fool me", 'errors': f.errors})
        except ObjectDoesNotExist:
            return JsonResponse({'msg': "Are you kidding me?, that medicine doesn't exists at all"},
                                status=404)
