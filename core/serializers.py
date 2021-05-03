from rest_framework import serializers
from .models import *
from datetime import datetime


class GetEmployeeSerializer(serializers.ModelSerializer):

    employee_id = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    join_date = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'age', 'join_date']

    def get_employee_id(self, employee):
        return "E%s" % str(employee.id).zfill(5)

    def get_age(self, employee):
        return "%s" % (datetime.now().year - employee.date_of_birth.year)

    def get_join_date(self, employee):
        return "%s" % (employee.join_date.date())


class CreateEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "date_of_birth"]

