from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .filters import EmployeeFilter
from django_filters import rest_framework as filters
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class ListCreateEmployeeView(ListCreateAPIView):

    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        qs = self.filter_queryset(self.get_queryset())
        serializer = serializer(qs, many=True)

        response_message = dict()
        response_message["message"] = "success"
        response_message["employees"] = serializer.data

        return Response(response_message, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        response_message = dict()
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            employee_instance = serializer.save()
            response_message["message"] = "success"
            return Response(response_message, status=status.HTTP_200_OK)
        response_message["message"] = "failed"
        return Response(response_message, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateEmployeeSerializer
        return GetEmployeeSerializer

    def get_queryset(self):
        return Employee.objects.all().order_by("last_name")


class RetrieveUpdateDestroyEmployeeView(RetrieveUpdateDestroyAPIView):

    def get(self, request, *args, **kwargs):
        employee_instance = get_object_or_404(Employee, pk=self.kwargs["employee"])
        response_message = dict()

        response_message["message"] = "success"
        serializer = self.get_serializer_class()
        serializer = serializer(employee_instance)
        response_message["employee"] = serializer.data
        return Response(response_message, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        employee_instance = get_object_or_404(Employee, pk=self.kwargs["employee"])
        response_message = dict()

        response_message["message"] = "success"

        # updates the employee
        employee_instance.first_name = request.data.get("first_name", employee_instance.first_name)
        employee_instance.last_name = request.data.get("last_name", employee_instance.last_name)
        date_of_birth = None
        if request.data.get("date_of_birth"):
            date_of_birth = datetime.strptime(request.data.get("date_of_birth"), "%Y-%m-%d")
        employee_instance.date_of_birth = date_of_birth if date_of_birth else employee_instance.date_of_birth
        employee_instance.save()

        serializer = self.get_serializer_class()
        serializer = serializer(employee_instance)
        response_message["employee"] = serializer.data
        return Response(response_message, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        employee_instance = get_object_or_404(Employee, pk=self.kwargs["employee"])
        response_message = dict()

        response_message["message"] = "success"
        # delete this employee
        employee_instance.delete()
        return Response(response_message, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        return GetEmployeeSerializer
