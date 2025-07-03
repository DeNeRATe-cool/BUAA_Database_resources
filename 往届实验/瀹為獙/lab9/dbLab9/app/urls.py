from django.urls import path
from app.views import *

urlpatterns = [
    path('add', add),
    path('delete', delete),
    path('alter', alter),
    path('search', search),
]