from django.contrib import admin
from pcapp.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class UserModelAdmin(BaseUserAdmin):
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'name', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()

class DepartmentModelAdmin(admin.ModelAdmin):
	list_display = ["department_id","department_name","updated","Created_on"]
	list_display_link=["department_name"]
	list_filter=["department_name","updated"]
	search_fields=["department_name"]
	class Meta:
		model=Department
		

class EmployeeModelAdmin(admin.ModelAdmin):
	list_display = ["employee_id","employee_name","employee_phone","employee_email","updated","Created_on"]
	list_display_link=["employee_name"]
	list_filter=["employee_name","updated"]
	search_fields=["employee_name"]
	class Meta:
		model=Employee
		

class TimesheetModelAdmin(admin.ModelAdmin):
	list_display = ["department_id","employee_id","date","working_hours","start_time","end_time","updated","Created_on"]
	list_display_link=["department_id","employee_id","date"]
	list_filter=["department_id","employee_id","date"]
	search_fields=["department_id","employee_id","date"]
	class Meta:
		model=Timesheet
		

# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)
admin.site.register(Department, DepartmentModelAdmin)
admin.site.register(Employee, EmployeeModelAdmin)
admin.site.register(Timesheet, TimesheetModelAdmin)
