


    
from django.urls import path
from emp_api import views
from .views import EmployeeDetailView, EmployeeUpdateRequestView, AdminUpdateApprovalView

urlpatterns = [
    path('login/', views.login, name='login'),
    path("employee/me/", EmployeeDetailView.as_view(), name="employee-details"),
    path("employee/update-request/", EmployeeUpdateRequestView.as_view(), name="employee-update-request"),
    path("admin/update-approval/<int:pk>/", AdminUpdateApprovalView.as_view(), name="admin-update-approval"),
]

    
