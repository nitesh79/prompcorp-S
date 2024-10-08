"""
URL configuration for prompcorp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path
from pcapp.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/test/', test)
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r"^auth/", include("djoser.urls.jwt")),
    path('admin/', admin.site.urls),
    path('', pages_register_fun, name='pages-register'),
	path('index/', indexfun,name='index'), # this is main home page
    path('base/', basefun, name='base'),
    path('userprofile/', userprofilefun, name='userprofile'),

    #register, login, logout
    path('pages-register/', pages_register_fun, name='pages-register'), # this one is for home page ie resiter and login
    path('reg/', regfun, name='reg'),
    path('loginf/', loginffun, name='loginf'),
    path('logout/', logoutfun, name='logout'),

    #Contract
    path('Contract/', Contractfun, name='Contract'),
    path('addContract/', addContractfun, name='addContract'),
    path('editContract/', editContractfun, name='editContract'),
    path('delete_Contract/<str:id>/', delete_Contractfun, name='delete_Contract'),

    #Deals
    path('Deals/', Dealsfun, name='Deals'),
    path('addDeals/', addDealsfun, name='addDeals'),
    path('editDeals/', editDealsfun, name='editDeals'),
    path('delete_deals/<str:id>/', delete_dealsfun, name='delete_deals'),

    #Client Group
    path('ClientGroup/', ClientGroupfun, name='ClientGroup'),
    path('addClientGroup/', addClientGroupfun, name='addClientGroup'),
    path('editClientGroup/', editClientGroupfun, name='editClientGroup'),
    path('delete_ClientGroup/<str:id>/', delete_ClientGroupfun, name='delete_ClientGroup'),

    #Client Account
    path('Account/', Accountfun, name='Account'),
    path('addAccount/', addAccountfun, name='addAccount'),
    path('editAccount/', editAccountfun, name='editAccount'),
    path('delete_Account/<str:id>/', delete_Accountfun, name='delete_Account'),

    #Client Contact
    path('ClientContact/', ClientContactfun, name='ClientContact'),
    path('addClientContact/', addClientContactfun, name='addClientContact'),
    path('editClientContact/', editClientContactfun, name='editClientContact'),
    path('delete_ClientContact/<str:id>/', delete_ClientContactfun, name='delete_ClientContact'),

    #Employee and department domain
    path('EmployeeDepartment/', EmployeeDepartmentfun, name='EmployeeDepartment'),
    path('addemployee/', addemployeefun, name='addemployee'),
    path('editemployee/', editemployeefun, name='editemployee'),
    path('delete_employee/<str:id>/', delete_employeefun, name='delete_employee'),

    #department 
    path('Department/', Departmentfun, name='Department'),
    path('addDepartment/', addDepartmentfun, name='addDepartment'),
    path('editDepartment/', editDepartmentfun, name='editDepartment'),
    path('delete_Department/<str:id>/', delete_Departmentfun, name='delete_Department'),

    #Timesheet
    path('Timesheet/', Timesheetfun, name='Timesheet'),
    path('addTimesheet/', addTimesheetfun, name='addTimesheet'),
    path('edittimesheet/', edittimesheetfun, name='edittimesheet'),
    path('delete_timesheet/<str:id>/', delete_timesheetfun, name='delete_timesheet'),

    #Material Supplier
    path('MaterialSupplier/', MaterialSupplierfun, name='MaterialSupplier'),
    path('addMaterialSupplier/', addMaterialSupplierfun, name='addMaterialSupplier'),
    path('editMaterialSupplier/', editMaterialSupplierfun, name='editMaterialSupplier'),
    path('delete_MaterialSupplier/<str:id>/', delete_MaterialSupplierfun, name='delete_MaterialSupplier'),

    #Stores Branch Names
    path('Stores/', StoresBranchNamesfun, name='Stores'),
    path('addStoresBranchNames/', addStoresBranchNamesfun, name='addStoresBranchNames'),
    path('editStoresBranchNames/', editStoresBranchNamesfun, name='editStoresBranchNames'),
    path('delete_StoresBranchNames/<str:id>/', delete_StoresBranchNamesfun, name='delete_StoresBranchNames'),

    #Stores Branch Names
    path('MaterialInvoice/', MaterialInvoicefun, name='MaterialInvoice'),
    path('addMaterialInvoice/', addMaterialInvoicefun, name='addMaterialInvoice'),
    path('editMaterialInvoice/', editMaterialInvoicefun, name='editMaterialInvoice'),
    path('delete_MaterialInvoice/<str:id>/', delete_MaterialInvoicefun, name='delete_MaterialInvoice'),

    #registration

]

# Add this to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

LOGIN_URL = 'loginffun'
LOGOUT_URL = 'logoutfun'
LOGIN_REDIRECT_URL = 'pages-register'