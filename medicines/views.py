from django.views.decorators.http import require_safe
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from .owner import *
from .models import Medicine
from .forms import CreateForm
from django.views import View
from .filters import ProductFilter
from cart.models import Order
from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.
class MedListView(OwnerListView):
    model = Medicine
    template_name = "medicines/medicine_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        if self.request.user.is_authenticated:
            orders = Order.objects.filter(user=self.request.user, ordered=False)
            if orders.exists():
                cart_items = orders[0].items.all()
                a = [item.item for item in cart_items]
                context["items"] = a
        return context


class MedDetailView(OwnerDetailView):
    model = Medicine
    template_name = "medicines/medicine_detail.html"


class MedCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = Medicine
    permission_required = 'medicines.add_medicine'
    permission_denied_message = "No Access"
    success_url = reverse_lazy("medicines:all")
    template_name = "medicines/medicine_add.html"

    def get(self, request):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        med = form.save(commit=False)
        med.owner = self.request.user
        med.save()
        return redirect(self.success_url)


class MedUpdateView(LoginRequiredMixin, View):
    model = Medicine
    success_url = "medicines:all"
    template_name = "medicines/medicine_add.html"

    def get(self, request, pk):
        med = get_object_or_404(Medicine, id=pk, owner=self.request.user)
        form = CreateForm(instance=med)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        med = get_object_or_404(Medicine, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=med)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        med = form.save(commit=False)
        med.save()
        return redirect(self.success_url)


class MedDeleteView(OwnerDeleteView):
    model = Medicine
    template_name = "medicines/medicine_delete.html"


@require_safe
def stream_file(request, pk):
    med = get_object_or_404(Medicine, id=pk)
    response = HttpResponse()
    if not med.thumbnail:
        return HttpResponse("No Thumbnail")
    response['Content-Type'] = med.thumb_content_type
    response['Content-Length'] = len(med.thumbnail)
    response.write(med.thumbnail)
    return response
