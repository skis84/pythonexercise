from django.urls import path
from . import views

urlpatterns = [
    path('<company_id>', views.company, name='company')
]
