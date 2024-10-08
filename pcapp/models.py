from django.db import models
from django.contrib.auth.models import User,BaseUserManager, AbstractBaseUser

# Create your models here.

#custom user model for authenticatioin with email instead of username -----------------------------------------------------------
# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, is_admin=False, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        User = self.model(
            email=self.normalize_email(email),
            name=name,
            is_admin=is_admin
        )
        User.set_password(password)
        User.save(using=self._db)
        return User
    
    def create_superuser(self, email, name, is_admin=True, password=None):
        """
        Creates and saves a Superuser with the given email, name and password.
        """
        User = self.create_user(
            email=email,
            password=password,
            name=name,
            is_admin=is_admin
        )
        User.is_admin = True
        User.save(using=self._db)
        return User

# Custom User Model.
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    is_approved=models.BooleanField(default=False)
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    Created_on=models.DateTimeField(auto_now=False,auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['name', 'is_admin']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
# end of custom user model for authenticatioin with email instead of username ----------------------------------------------------


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)


#----------------------------------------------------------------------------------------------------- 
#Domain Department

class Department(models.Model):
    department_id = models.CharField(max_length=20, primary_key=True)
    department_name = models.CharField(max_length=255)
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    Created_on=models.DateTimeField(auto_now=False,auto_now_add=True)
    def __unicode__(self):
        return self.department_name
    def __str__(self):
        return self.department_name
    
class Employee(models.Model):
    employee_id = models.CharField(max_length=20, primary_key=True)
    employee_name = models.CharField(max_length=255, null=False)
    employee_phone = models.CharField(max_length=20, unique=True)
    employee_email = models.EmailField(unique=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    Created_on = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.employee_name

    def __str__(self):
        return self.employee_name
    
class Timesheet(models.Model):
    department_id = models.ForeignKey(Department, null=False, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, null=False, on_delete=models.CASCADE)
    date = models.DateField()
    working_hours = models.DecimalField(max_digits=5, decimal_places=2)  
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    myfile = models.FileField(upload_to='uploads/', blank=True, null=True)
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    Created_on=models.DateTimeField(auto_now=False,auto_now_add=True)
    class Meta:
        unique_together = (('date','department_id', 'employee_id' ),)

#-----------------------------------------------------------------------------------------------------
#Domain: Clients
class ClientGroup(models.Model):
    client_id=models.CharField(max_length=20, primary_key=True)
    industry=models.CharField(max_length=255)
    company_name=models.CharField(max_length=255)
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    Created_on=models.DateTimeField(auto_now=False,auto_now_add=True)
    class Meta:
        unique_together = (('client_id', 'industry'),)


class Account(models.Model):
    account_number = models.CharField(max_length=20,primary_key=True) # change this to charfield
    client_id = models.ForeignKey(ClientGroup, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=255)
    account_role = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    abn = models.BigIntegerField(max_length=11,unique=True)
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    Created_on=models.DateTimeField(auto_now=False,auto_now_add=True)

class ClientContact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15,unique=True) 
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    Created_on=models.DateTimeField(auto_now=False,auto_now_add=True)


#----------------------------------------------------------------------------------------------------- 
#Domain Contract

class Deals(models.Model):
    deal_id = models.CharField(max_length=20,primary_key=True)
    deal_name = models.CharField(max_length=255)
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    pricing = models.DecimalField(max_digits=12, decimal_places=2)
    duration =  models.CharField(max_length=255)
    SLAs = models.TextField()
    deal_status = models.CharField(max_length=255)
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    Created_on=models.DateTimeField(auto_now=False,auto_now_add=True)

class Contract(models.Model):
    contract_id = models.CharField(max_length=20,primary_key=True)
    deal_id = models.ForeignKey(Deals, on_delete=models.CASCADE)
    contract_type =  models.CharField(max_length=255)
    start_date =  models.DateField()
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    Created_on=models.DateTimeField(auto_now=False,auto_now_add=True)

#----------------------------------------------------------------------------------------------------- 
#Materials Domain

class MaterialSupplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=200)
    business_name = models.CharField(max_length=200)
    business_address = models.CharField(max_length=200)
    phone_support_queries = models.CharField(max_length=15,unique=True) 
    email_support_queries = models.EmailField(unique=True)
    material_supply_category = models.CharField(max_length=200)
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    Created_on=models.DateTimeField(auto_now=False,auto_now_add=True)

class StoresBranchNames(models.Model):
    ABN = models.CharField(max_length=20,primary_key=True)
    supplier_id = models.ForeignKey(MaterialSupplier, on_delete=models.CASCADE)
    store_id = models.CharField(max_length=200)
    branch_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    region_of_operation = models.CharField(max_length=200)
    branch_contact = models.CharField(max_length=200) 
    phone = models.CharField(max_length=15,unique=True) 
    email = models.EmailField(unique=True)
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    Created_on=models.DateTimeField(auto_now=False,auto_now_add=True)
	
class MaterialInvoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    ABN = models.ForeignKey(StoresBranchNames, on_delete=models.CASCADE)
    items = models.CharField(max_length=200)
    quantity = models.IntegerField(max_length=10)
    individual_price = models.DecimalField(max_digits=10, decimal_places=2) 
    total_price = models.DecimalField(max_digits=12, decimal_places=2) 
    approver = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    Created_on=models.DateTimeField(auto_now=False,auto_now_add=True)

	
	
	
	
	