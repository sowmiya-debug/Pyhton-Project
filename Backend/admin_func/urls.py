from django.urls import path,include
from employee import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    
    path('', views.admin_login,name='adminlogin'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('register/',views.employee_register,name='employee_register'),
    path('manage-employees/', views.manage_employees, name='manage_employee'),
    path("request-update/", views.request_update, name="request_update"),
    path("approvals/", views.approvals, name="approvals"),
    path("approve/<int:request_id>/", views.approve_request, name="approve_request"),
    path("reject/<int:request_id>/", views.reject_request, name="reject_request"),
    path('employees/', views.manage_employees, name='manage_employees'),
    path('employees/edit/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('employees/delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('employeelist/', views.employee_list, name='employeelist'),
    path("logout/", views.user_logout, name="logout"),
    path('api/', include('emp_api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
