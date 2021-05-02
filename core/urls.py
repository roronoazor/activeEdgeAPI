from django.urls import path, include
from .views import *

urlpatterns = [
    path("employees/", ListCreateEmployeeView.as_view(), name="list_create_employees"),
    path("employee/<int:employee>", RetrieveUpdateDestroyEmployeeView.as_view(), name="get_update_destroy_employee")
]