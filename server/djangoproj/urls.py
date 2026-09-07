from pathlib import Path
"""djangoproj URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent

urlpatterns = [
    path('static/<path:path>', serve, {'document_root': BASE_DIR / 'frontend' / 'build' / 'static'}),
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    path('about', TemplateView.as_view(template_name="About.html"), name='about'),
    path('contact', TemplateView.as_view(template_name="Contact.html"), name='contact'),

    path('dealer/<int:id>', TemplateView.as_view(template_name='index.html'), name='dealer_frontend'),
    path('postreview/<int:id>', TemplateView.as_view(template_name='index.html'), name='postreview_frontend'),
    path(
        'dealers',
        TemplateView.as_view(
            template_name='index.html'
        ),
        name='dealers'
    ),

    path('', TemplateView.as_view(template_name="Home.html"), name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve React production build assets during development
urlpatterns += static(
    '/static/',
    document_root=BASE_DIR / 'frontend' / 'build' / 'static'
)
