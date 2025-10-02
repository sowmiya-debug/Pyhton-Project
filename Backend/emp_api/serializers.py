from rest_framework import serializers
from employee.models import Employee, EmployeeUpdateRequest

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeUpdateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeUpdateRequest
        fields = ["id", "employee", "name", "age", "gender", "contact_number", "status", "created_at"]
        read_only_fields = ["status", "created_at"]
