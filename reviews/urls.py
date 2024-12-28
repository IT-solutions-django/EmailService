from django.urls import path
from .views import *


app_name = 'reviews' 


urlpatterns = [
    path('two_gis/<str:organization_id>/', Fetch2GISReviews.as_view(), name='fetch_two_gis_reviews'),
    path('vl/<str:organization_slug>/<str:organization_id>/', FetchVLReviews.as_view(), name='fetch_vl_reviews'),
    path('yandex/<str:organization_slug>/<str:organization_id>/', FetchYandexReviews.as_view(), name='fetch_yandex_reviews'),
]