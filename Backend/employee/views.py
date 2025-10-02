from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from employee.models import Employee
from .forms import EmployeeRegisterForm

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:  # only allow admins
            login(request, user)
            return redirect("dashboard")  # redirect to admin dashboard
       

    return render(request, "login.html")

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import Employee, EmployeeUpdateRequest

def is_admin(user):
    return user.is_staff  # or customize if you have admin flag
@login_required
@user_passes_test(is_admin)
def dashboard(request):
    total_employees = Employee.objects.count()
    # Pending = those not approved and not deleted
    pending_requests = EmployeeUpdateRequest.objects.filter(
        is_approved=False, is_deleted=False
    ).count()

    return render(request, "dashboard.html", {
        "total_employees": total_employees,
        "pending_requests": pending_requests,
    })



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import EmployeeRegisterForm
from .models import Employee

def employee_register(request):
    if request.method == "POST":
        form = EmployeeRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            else:
                # Create User for login
                user = User.objects.create_user(username=username, password=password)

                # Save employee details
                employee = form.save(commit=False)
                employee.user = user
                employee.save()

                messages.success(request, "Employee registered successfully!")
                return redirect("manage_employee")  # change to your list page
    else:
        form = EmployeeRegisterForm()
    return render(request, "employee_register.html", {"form": form})


# from django.contrib.auth.models import User
# from .models import Employee

# def create_employee(request):
#     if request.method == "POST":
#         form = EmployeeForm(request.POST)
#         if form.is_valid():
#             # Create Django user
#             user = User.objects.create_user(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password']
#             )
            
#             # Create employee record (link to user if needed)
#             Employee.objects.create(
#                 user=user,
#                 name=form.cleaned_data['name'],
#                 department=form.cleaned_data['department'],
#                 designation=form.cleaned_data['designation'],
#                 contact_number=form.cleaned_data['contact_number'],
#                 emergency_contact=form.cleaned_data['emergency_contact'],
#                 salary_allowance=form.cleaned_data['salary_allowance'],
#             )
#             # redirect somewhere


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Employee, EmployeeUpdateRequest
from .forms import EmployeeUpdateForm

# ✅ Employee submits update request
@login_required
def request_update(request):
    employee = get_object_or_404(Employee, user=request.user)

    if request.method == "POST":
        form = EmployeeUpdateForm(request.POST)
        if form.is_valid():
            update_request = form.save(commit=False)
            update_request.employee = employee
            update_request.save()
            return redirect('dashboard')  # back to employee dashboard
    else:
        form = EmployeeUpdateForm()

    return render(request, "employee_request_update.html", {"form": form})


# ✅ Admin views all requests
@login_required
@user_passes_test(is_admin)
def approvals(request):
    # Only show requests that are pending
    requests = EmployeeUpdateRequest.objects.filter(
        is_approved=False, is_deleted=False
    )
    return render(request, "approvals.html", {"requests": requests})


# ✅ Admin approves request
@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_request(request, request_id):
    update_request = get_object_or_404(EmployeeUpdateRequest, id=request_id)

    # Apply changes to employee
    emp = update_request.employee
    if update_request.new_name:
        emp.name = update_request.new_name
    if update_request.new_phone:
        emp.phone = update_request.new_phone
    if update_request.new_address:
        emp.address = update_request.new_address
    emp.save()

    update_request.status = "Approved"
    update_request.save()

    return redirect("approvals")


# ✅ Admin rejects request
@login_required
@user_passes_test(lambda u: u.is_superuser)
def reject_request(request, request_id):
    update_request = get_object_or_404(EmployeeUpdateRequest, id=request_id)
    update_request.status = "Rejected"
    update_request.save()
    return redirect("approvals")


from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Employee
from django.contrib import messages

def manage_employees(request):
    # Get search and department filter values
    search_query = request.GET.get('search', '')
    dept_filter = request.GET.get('department', '')

    # Filter employees
    employees = Employee.objects.all()
    if search_query:
        employees = employees.filter(name__icontains=search_query)
    if dept_filter:
        employees = employees.filter(department=dept_filter)

    # Get distinct departments for filter dropdown
    departments = Employee.objects.values_list('department', flat=True).distinct()

    # Pagination (10 per page)
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'employees': page_obj,
        'departments': departments,
        'request': request,  # to keep GET params in form
        'page_obj': page_obj,
    }
    return render(request, 'manage_employees.html', context)

# Edit employee
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.name = request.POST.get('name')
        employee.contact_number = request.POST.get('contact_number')
        employee.department = request.POST.get('department')
        employee.save()
        messages.success(request, 'Employee details updated successfully.')
        return redirect('manage_employees')
    return render(request, 'employee_edit.html', {'employee': employee})

# Delete employee
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    messages.success(request, 'Employee deleted successfully.')
    return redirect('manage_employees')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, "manage_employee.html", {"employees": employees})

def employee_delete(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        emp.delete()
        return redirect("manage_employees")
    return redirect("manage_employees")

def employee_edit(request, pk):
    # your edit logic goes here
    return redirect("manage_employees")

from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)  # clears the session
    return redirect("adminlogin")  # redirect to login page after logout







