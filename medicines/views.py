from django.shortcuts import render
from .owner import *
from .models import MedCat, Medicine


# for search queries
from django.db.models import Q

# Create your views here.


class MedListView(OwnerListView):
    model = Medicine
    template_name = "medicines/medicine_list.html"

    def get(self, request):
        search = request.GET.get("search", False)
        if search:
            query = Q(name__contains=search)
            query.add(Q(category__contains=search), Q.OR)
            query.add(Q(description__contains=search), Q.OR)
            medicine_list = Medicine.objects.filter(query).select_related()
        else:
            medicine_list = Medicine.objects.all()
        ctx = {'medicine_list': medicine_list, 'search': search}
        return render(request, self.template_name, ctx)
