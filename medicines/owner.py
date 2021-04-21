from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerListView(generic.ListView):
    """"""


class OwnerCreateView(LoginRequiredMixin, generic.CreateView):

    def form_valid(self, form):
        form_object = form.save(commit=False)
        form_object.owner = self.request.user
        form_object.save()
        return super(OwnerCreateView, self).form_valid(form)


class OwnerDetailView(generic.DetailView):
    """"""


class OwnerUpdateView(LoginRequiredMixin, generic.UpdateView):

    def get_queryset(self):
        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerDeleteView(LoginRequiredMixin, generic.DeleteView):

    def get_queryset(self):
        return super(OwnerDeleteView, self).get_queryset().filter(owner=self.request.user)
