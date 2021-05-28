from django.urls import path
from django.views.generic import TemplateView
from.views import HomeView

app_name = 'home'

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path(r'service-worker.js', (TemplateView.as_view(
        template_name="sw.js",
        content_type='application/javascript',
    )), name='service-worker.js')
]
