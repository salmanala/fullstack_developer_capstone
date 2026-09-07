from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('get_cars', views.get_cars, name='get_cars'),
    path('dealers/<str:state>', views.get_dealers_by_state, name='dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_by_id, name='dealer_by_id'),
    path('get_dealers', views.get_dealers, name='get_dealers'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
