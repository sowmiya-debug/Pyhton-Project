from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from employee.models import EmployeeUpdateRequest,Employee
from .serializers import EmployeeSerializer, EmployeeUpdateRequestSerializer

# Employee can view his details
from rest_framework import generics, permissions
from employee.models import Employee
from .serializers import EmployeeSerializer

# Get details of one employee
class EmployeeDetailView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]  # require JWT login



# Employee requests changes to basic details
class EmployeeUpdateRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        employee = request.user.employee
        data = request.data.copy()
        data["employee"] = employee.id

        serializer = EmployeeUpdateRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Update request submitted. Awaiting admin approval.", "request": serializer.data})
        return Response(serializer.errors, status=400)


# Admin approves/rejects requests
class AdminUpdateApprovalView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            update_request = EmployeeUpdateRequest.objects.get(id=pk, status="PENDING")
        except EmployeeUpdateRequest.DoesNotExist:
            return Response({"error": "Request not found or already processed."}, status=404)

        action = request.data.get("action")  # APPROVE or REJECT
        if action == "APPROVE":
            emp = update_request.employee
            if update_request.name:
                emp.name = update_request.name
            if update_request.age:
                emp.age = update_request.age
            if update_request.gender:
                emp.gender = update_request.gender
            if update_request.contact_number:
                emp.contact_number = update_request.contact_number
            emp.save()
            update_request.status = "APPROVED"
            update_request.save()
            return Response({"message": "Update request approved and employee details updated."})

        elif action == "REJECT":
            update_request.status = "REJECTED"
            update_request.save()
            return Response({"message": "Update request rejected."})

        return Response({"error": "Invalid action."}, status=400)

