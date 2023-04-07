from django.urls import path, include
from app.views import *

urlpatterns = [
    path('', index, name='index'),
    path('push/', push_marks, name='push'),
    path('get-marks/', get_marks, name='get-marks'),
]
