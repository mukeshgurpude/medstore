from django.urls import path, reverse_lazy
from . import views


app_name = "medicines"

urlpatterns = [
    path("", views.MedListView.as_view(), name="all"),
    path("medicine/<int:pk>/", views.MedDetailView.as_view(), name="detail"),
    path("add/", views.MedCreateView.as_view(success_url=reverse_lazy("medicines:all")), name="create"),
    path("update/<int:pk>/", views.MedUpdateView.as_view(success_url=reverse_lazy("medicines:all")), name="update"),
    path("delete/<int:pk>/", views.MedDeleteView.as_view(success_url=reverse_lazy("medicines:all")), name="delete"),
    path("medicine/<int:pk>/thumbnail/", views.stream_file, name="picture"),
]
