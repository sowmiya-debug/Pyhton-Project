from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,User

def create_superuser(self, email, name='admin',password=None):
   user = self.create_user(email=email,name=name, password=password)
   user.is_admin = True
   user.is_superuser = True
   user.save(using=self._db)
   return user

from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # for login
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('Male','Male'), ('Female','Female'), ('Other','Other')])
    contact_number = models.CharField(max_length=15)

    # Additional Details
    address = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=15)

    # Occupation Details
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    salary_basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    salary_allowance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# from django.db import models
# from django.contrib.auth.models import User

# class Employee(models.Model):
    
#     name = models.CharField(max_length=100)
#     age = models.PositiveIntegerField()
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

#     department = models.CharField(max_length=100)
#     designation = models.CharField(max_length=100)
#     contact_number = models.CharField(max_length=15)
#     emergency_contact = models.CharField(max_length=15)
#     salary_allowance = models.DecimalField(max_digits=10, decimal_places=2)
#     address = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.name

    
class EmployeeUpdateRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    new_name = models.CharField(max_length=100)
    new_age = models.PositiveIntegerField()
    new_gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    new_contact_number = models.CharField(max_length=15)
    is_approved = models.BooleanField(null=True)  # None = pending, True = approved, False = rejected
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete flag
    

    

    def __str__(self):
        return f"Update Request for {self.employee.name}"

