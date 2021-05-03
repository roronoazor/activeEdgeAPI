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

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = self.get_serializer_class()
            filtered_queryset = self.filter_queryset(self.get_queryset())
            paginated_queryset = self.paginate_queryset(filtered_queryset)
            serializer = serializer(paginated_queryset, many=True)

            response_message = dict()
            response_message["message"] = "success"
            response_message["employees"] = serializer.data
            response_message["next"] = self.paginator.get_next_link()
            response_message["previous"] = self.paginator.get_previous_link()
            response_message["count"] = filtered_queryset.count()

            return Response(response_message, status=status.HTTP_200_OK)
        return Response({"message": "authentication required"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            response_message = dict()
            serializer = self.get_serializer_class()
            serializer = serializer(data=request.data)

            try:
                date_of_birth = datetime.strptime(request.data.get("date_of_birth"), "%Y-%m-%d")
                if date_of_birth.date() > datetime.now().date():
                    return Response({"message": "date of birth cannot be in the future"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"message": "a valid date with format YYYY-MM-DD is required"}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid(raise_exception=True):
                employee_instance = serializer.save(created_by="%s" % (request.user,))
                response_message["message"] = "success"
                return Response(response_message, status=status.HTTP_200_OK)
            response_message["message"] = "failed"
            return Response(response_message, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "authentication required"}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateEmployeeSerializer
        return GetEmployeeSerializer

    def get_queryset(self):
        return Employee.objects.all()


class RetrieveUpdateDestroyEmployeeView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            employee_instance = get_object_or_404(Employee, pk=self.kwargs["employee"])
            response_message = dict()

            response_message["message"] = "success"
            serializer = self.get_serializer_class()
            serializer = serializer(employee_instance)
            response_message["employee"] = serializer.data
            return Response(response_message, status=status.HTTP_200_OK)
        return Response({"message": "authentication required"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            employee_instance = get_object_or_404(Employee, pk=self.kwargs["employee"])
            response_message = dict()

            response_message["message"] = "success"

            # updates the employee
            employee_instance.first_name = request.data.get("first_name", employee_instance.first_name)
            employee_instance.last_name = request.data.get("last_name", employee_instance.last_name)
            date_of_birth = None
            if request.data.get("date_of_birth"):
                date_of_birth = datetime.strptime(request.data.get("date_of_birth"), "%Y-%m-%d")
                if date_of_birth.date() > datetime.now().date():
                    return Response({"message": "date of birth cannot be in the future"}, status=status.HTTP_400_BAD_REQUEST)
                date_of_birth = date_of_birth.date()
            employee_instance.date_of_birth = date_of_birth if date_of_birth else employee_instance.date_of_birth
            employee_instance.last_updated_by = "%s" % (request.user,)
            employee_instance.save()

            serializer = self.get_serializer_class()
            serializer = serializer(employee_instance)
            response_message["employee"] = serializer.data
            return Response(response_message, status=status.HTTP_200_OK)
        return Response({"message": "authentication required"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            employee_instance = get_object_or_404(Employee, pk=self.kwargs["employee"])
            response_message = dict()

            response_message["message"] = "success"
            # delete this employee
            employee_instance.delete()
            return Response(response_message, status=status.HTTP_200_OK)
        return Response({"message": "authentication required"}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return CreateEmployeeSerializer
        return GetEmployeeSerializer
