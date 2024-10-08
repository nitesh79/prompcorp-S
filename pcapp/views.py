from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect,Http404, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import *
from pcapp.models import *
from django.contrib import messages
from pcapp.models import *
from django.db.models import Q
from django.db import transaction
from django.db import IntegrityError
from datetime import datetime
from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from pcapp.serializers import CustomTokenObtainPairSerializer
from django.http import JsonResponse
from django.core import serializers
# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def test(request):
    return JsonResponse({'name' : request.GET.get("name")})
    # employeedata = Employee.objects.all()
    # return JsonResponse({'data' : list(employeedata.values()),
    #                      'status' : 200 }, safe=False)



 
def pages_register_fun(request):
	return render(request,"pcapp/pages-register.html")

# =-------- need to work on this -----
def custom_page_not_found_view(request, exception):
    return render(request, "error-404.html", status=404)

def basefun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        return render(request, 'pcapp/base.html')
    else:
        return render(request,"pcapp/pages-register.html")
    return render(request, 'pcapp/base.html')

def userprofilefun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        userdata = get_object_or_404(User, email=request.user.email)
        userdata.email = request.user.email
    context = {
        "userdata": userdata,
    }
    return render(request, 'pcapp/userprofile.html', context)

@login_required(login_url='/pages-register/')
def indexfun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        clientgroupdata = ClientGroup.objects.all()
        accountdata = Account.objects.all()
        clientcontactdata = ClientContact.objects.all()
        dealdata = Deals.objects.all()
        contractdata = Contract.objects.all()
        clientgroupdata = ClientGroup.objects.all()
        timesheetdata = Timesheet.objects.all()
        empdata = Employee.objects.all()
        deptdata = Department.objects.all()
        materialdata = MaterialSupplier.objects.all()
        storebranchdata = StoresBranchNames.objects.all()
        matinvoicedata = MaterialInvoice.objects.all()
        context = {
            "accountdata": accountdata,
            "clientgroupdata": clientgroupdata,
            "clientcontactdata": clientcontactdata,
            "dealdata": dealdata,
            "contractdata": contractdata,
            "clientgroupdata": clientgroupdata,
            "timesheetdata": timesheetdata,
            "empdata": empdata,
            "deptdata": deptdata,
            "materialdata": materialdata,
            "storebranchdata": storebranchdata,
            "matinvoicedata": matinvoicedata,
        }    
        return render(request, 'pcapp/index.html', context)
    else:
        return render(request,"pcapp/pages-register.html")
    return render(request, 'pcapp/index.html')

#-------------------------------------------------------------------------------------------------------
#Client and Contract domain
#Client Account
def Accountfun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        query = request.GET.get('q')
        clientgroupdata = ClientGroup.objects.all()
        if query:
            accountdata = Account.objects.filter(
                Q(account_number__icontains=query) | 
                Q(client_id__company_name__icontains=query) |
                Q(account_name__icontains=query) |
                Q(account_role__icontains=query) |
                Q(location__icontains=query) |
                Q(abn__icontains=query)
            )
        else:
            accountdata = Account.objects.all()
            
        
        context = {
            "accountdata": accountdata,
            "clientgroupdata": clientgroupdata,
        }
        return render(request, 'pcapp/Account.html', context)
    else:
        return render(request, "pcapp/pages-register.html")

def addAccountfun(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        client_id = request.POST.get('client_id')
        account_name = request.POST.get('account_name')
        account_role = request.POST.get('account_role')
        locationdata = request.POST.get('locationdata')
        abn = request.POST.get('abn')
        try:
            clgrp = ClientGroup.objects.get(client_id=client_id)
            if Account.objects.filter(account_number=account_number).first():
                messages.error(request, 'Account Number already exist')
                return HttpResponseRedirect("/Account/")
            else:
                accountdata = Account(account_number=account_number, 
                                    client_id=clgrp, 
                                    account_name=account_name, 
                                    account_role=account_role, 
                                    location=locationdata, 
                                    abn=abn
                                    )
                accountdata.save()
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    return HttpResponseRedirect("/Account/")

def editAccountfun(request):
    if request.method == 'POST':
        taccount_number = request.POST.get('account_number')
        account_name = request.POST.get('account_name')
        account_role = request.POST.get('account_role')
        tlocation = request.POST.get('locationdata')
        tabn = request.POST.get('abndata')
        try:
            account = get_object_or_404(Account, account_number=taccount_number)
            account.account_name = account_name
            account.account_role = account_role
            account.location = tlocation
            account.abn = tabn
            with transaction.atomic():
                account.save()
            return HttpResponseRedirect("/Account/")
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    else:
        messages.error(request, 'Could not save the details')
    return HttpResponseRedirect("/Account/")

def delete_Accountfun(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/pages-register/")
    instance = get_object_or_404(Account, account_number=id)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect("/Account/")
    return HttpResponseRedirect("/Account/")


#Client Contact
def ClientContactfun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        query = request.GET.get('q')
        accountdata = Account.objects.all()
        if query:
            clientcontactdata = ClientContact.objects.filter(
                Q(contact_id__icontains=query) | 
                Q(account_number__account_number__icontains=query) |
                Q(name__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(email__icontains=query) |
                Q(address__icontains=query) |
                Q(role__icontains=query) 
            )
        else:
            clientcontactdata = ClientContact.objects.all()
            
        
        context = {
            "clientcontactdata": clientcontactdata,
            "accountdata": accountdata,
        }
        return render(request, 'pcapp/ClientContact.html', context)
    else:
        return render(request, "pcapp/pages-register.html")

def addClientContactfun(request):
    if request.method == 'POST':
        contact_id = request.POST.get('contact_id')
        account_number = request.POST.get('account_number')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        role = request.POST.get('role')
        try:
            accno = Account.objects.get(account_number=account_number)
            if ClientContact.objects.filter(contact_id=contact_id).first():
                messages.error(request, 'Client Contact ID already exist')
                return HttpResponseRedirect("/ClientContact/")
            else:
                clientcontactd = ClientContact(contact_id=contact_id, 
                                    account_number=accno, 
                                    name=name, 
                                    phone_number=phone_number, 
                                    email=email, 
                                    address=address, 
                                    role=role
                                    )
                clientcontactd.save()
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    return HttpResponseRedirect("/ClientContact/")

def editClientContactfun(request):
    if request.method == 'POST':
        contact_id = request.POST.get('contact_id')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        role = request.POST.get('role')
        try:
            clientcontact = get_object_or_404(ClientContact, contact_id=contact_id)
            clientcontact.name = name
            clientcontact.phone_number = phone_number
            clientcontact.email = email
            clientcontact.address = address
            clientcontact.role = role
            with transaction.atomic():
                clientcontact.save()
            return HttpResponseRedirect("/ClientContact/")
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    else:
        messages.error(request, 'Could not save the details')
    return HttpResponseRedirect("/ClientContact/")

def delete_ClientContactfun(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/pages-register/")
    instance = get_object_or_404(ClientContact, contact_id=id)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect("/ClientContact/")
    return HttpResponseRedirect("/ClientContact/")


#Deals
def Dealsfun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        query = request.GET.get('q')
        accdata = Account.objects.all()
        if query:
            dealdata = Deals.objects.filter(
                Q(deal_id__icontains=query) | 
                Q(account_number__account_number__icontains=query) |
                Q(deal_name__icontains=query) |
                Q(pricing__icontains=query) |
                Q(duration__icontains=query) |
                Q(SLAs__icontains=query) |
                Q(deal_status__icontains=query) 
            )
        else:
            dealdata = Deals.objects.all()
            
        context = {
            "dealdata": dealdata,
            "accountdata": accdata,
        }
        return render(request, 'pcapp/Deals.html', context)
    else:
        return render(request, "pcapp/pages-register.html")

def addDealsfun(request):
    if request.method == 'POST':
        deal_id = request.POST.get('deal_id')
        deal_name = request.POST.get('deal_name')
        account_number = request.POST.get('account_number')
        pricing = request.POST.get('pricing')
        duration = request.POST.get('duration')
        SLAs = request.POST.get('SLAs')
        deal_status = request.POST.get('deal_status')
        try:
            deal_accno = Account.objects.get(account_number=account_number)
            if Deals.objects.filter(deal_id=deal_id).first():
                messages.error(request, 'Deal ID already exist')
                return HttpResponseRedirect("/Deals/")
            else:
                dealsdata = Deals(deal_id=deal_id, 
                                    deal_name=deal_name, 
                                    account_number=deal_accno, 
                                    pricing=pricing, 
                                    duration=duration, 
                                    SLAs=SLAs, 
                                    deal_status=deal_status
                                    )
                dealsdata.save()
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    return HttpResponseRedirect("/Deals/")

def editDealsfun(request):
    if request.method == 'POST':
        deal_id = request.POST.get('deal_id')
        deal_name = request.POST.get('deal_name')
        pricing = request.POST.get('pricing')
        duration = request.POST.get('duration')
        SLAs = request.POST.get('SLAs')
        deal_status = request.POST.get('deal_status')
        try:
            deal = get_object_or_404(Deals, deal_id=deal_id)
            deal.deal_name = deal_name
            deal.pricing = pricing
            deal.duration = duration
            deal.SLAs = SLAs
            deal.deal_status = deal_status
            with transaction.atomic():
                deal.save()
            return HttpResponseRedirect("/Deals/")
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    else:
        messages.error(request, 'Could not save the details')
    return HttpResponseRedirect("/Deals/")

def delete_dealsfun(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/pages-register/")
    instance = get_object_or_404(Deals, deal_id=id)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect("/Deals/")
    return HttpResponseRedirect("/Deals/")

#Contract
def Contractfun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        query = request.GET.get('q')
        dealdata = Deals.objects.all()
        if query:
            contractdata = Contract.objects.filter(
                Q(contract_id__icontains=query) | 
                Q(deal_id__deal_id__icontains=query) |
                Q(contract_type__icontains=query) |
                Q(start_date__icontains=query)
            )
        else:
            contractdata = Contract.objects.all()
            
        context = {
            "dealdata": dealdata,
            "contractdata": contractdata,
        }
        return render(request, 'pcapp/Contract.html', context)
    else:
        return render(request, "pcapp/pages-register.html")

def addContractfun(request):
    if request.method == 'POST':
        contract_id = request.POST.get('contract_id')
        deal_id = request.POST.get('deal_id')
        contract_type = request.POST.get('contract_type')
        start_date = request.POST.get('start_date')
        try:
            dealno = Deals.objects.get(deal_id=deal_id)
            if Contract.objects.filter(contract_id=contract_id).first():
                messages.error(request, 'Client Contract ID already exist')
                return HttpResponseRedirect("/Contract/")
            else:
                contract = Contract(contract_id=contract_id, 
                                    deal_id=dealno, 
                                    contract_type=contract_type, 
                                    start_date=start_date
                                    )
                contract.save()
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    return HttpResponseRedirect("/Contract/")

def editContractfun(request):
    if request.method == 'POST':
        contract_id = request.POST.get('contract_id')
        contract_type = request.POST.get('contract_type')
        start_date = request.POST.get('start_date')
        try:
            contract = get_object_or_404(Contract, contract_id=contract_id)
            contract.contract_type = contract_type
            contract.start_date = start_date
            with transaction.atomic():
                contract.save()
            return HttpResponseRedirect("/Contract/")
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    else:
        messages.error(request, 'Could not save the details')
    return HttpResponseRedirect("/Contract/")

def delete_Contractfun(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/pages-register/")
    instance = get_object_or_404(Contract, contract_id=id)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect("/Contract/")
    return HttpResponseRedirect("/Contract/")

#Client Group
def ClientGroupfun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        query = request.GET.get('q')
        if query:
            clientgroupdata = ClientGroup.objects.filter(
                Q(client_id__icontains=query) | 
                Q(industry__icontains=query) |
                Q(company_name__icontains=query) 
            )
        else:
            clientgroupdata = ClientGroup.objects.all()
        
        context = {
            "clientgroupdata": clientgroupdata,
        }
        return render(request, 'pcapp/ClientGroup.html', context)
    else:
        return render(request, "pcapp/pages-register.html")

def addClientGroupfun(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        industry = request.POST.get('industry')
        company_name = request.POST.get('company_name')
        try:
            if ClientGroup.objects.filter(client_id=client_id).first():
                messages.error(request, 'Client ID already exist')
                return HttpResponseRedirect("/ClientGroup/")
            else:
                clientgroupd = ClientGroup(client_id=client_id, 
                                    industry=industry, 
                                    company_name=company_name
                                    )
                clientgroupd.save()
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    return HttpResponseRedirect("/ClientGroup/")

def editClientGroupfun(request):
    if request.method == 'POST':
        # Get the employee data from the form
        client_id = request.POST.get('client_id')
        industry = request.POST.get('industry')
        company_name = request.POST.get('company_name')
        try:
            cg = ClientGroup.objects.get(client_id=client_id)

            cg.industry = industry
            cg.company_name = company_name
            with transaction.atomic():
                cg.save()
            return HttpResponseRedirect("/ClientGroup/")
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    else:
        messages.error(request, 'Could not save the details')
    return HttpResponseRedirect("/ClientGroup/")

def delete_ClientGroupfun(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/pages-register/")
    instance = get_object_or_404(ClientGroup, client_id=id)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect("/ClientGroup/")
    return HttpResponseRedirect("/ClientGroup/")


#-------------------------------------------------------------------------------------------------------
#Employee and department domain
#timesheet
def Timesheetfun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        query = request.GET.get('q')
        employeedata = Employee.objects.all()
        departmentdata = Department.objects.all()
        if query:
            timesheetdata = Timesheet.objects.filter(
                Q(department_id__department_name__icontains=query) | 
                Q(employee_id__employee_name__icontains=query) |
                Q(date__icontains=query) |
                Q(working_hours__icontains=query) |
                Q(start_time__icontains=query) |
                Q(end_time__icontains=query)
            )
        else:
            timesheetdata = Timesheet.objects.all()
        base_url = f"{request.scheme}://{request.get_host()}"
        context = {
            "timesheetdata": timesheetdata,
            "employeedata": employeedata,
            "departmentdata": departmentdata,
            "base_url" : base_url
        }
        
        return render(request, 'pcapp/Timesheet.html', context)
    else:
        return render(request, "pcapp/pages-register.html")

def addTimesheetfun(request):
    if request.method == 'POST':
        department_id = request.POST.get('department_id')
        employee_id = request.POST.get('employee_id')
        date = request.POST.get('date')
        working_hours = request.POST.get('working_hours')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        myfile = request.FILES.get('photos') if 'photos' in request.FILES else None
        try:
            dept = Department.objects.get(department_id=department_id)
            emp = Employee.objects.get(employee_id=employee_id)
            if Timesheet.objects.filter(employee_id=employee_id).first() and Timesheet.objects.filter(department_id=department_id).first() and Timesheet.objects.filter(date=date).first():
                    messages.error(request, 'Record already exist') 
                    return HttpResponseRedirect("/Timesheet/")
            else:
                timesheet = Timesheet(department_id=dept,
                                    employee_id=emp, 
                                    date=date, 
                                    working_hours=working_hours, 
                                    start_time=start_time, 
                                    end_time=end_time,
                                    myfile=myfile
                                    )
            with transaction.atomic():
                timesheet.save()
            return HttpResponseRedirect("/Timesheet/")
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            #duplicate_entry = str(e).split("'")[1]
            #messages.error(request, f'{duplicate_entry} already exist')
            messages.error(request, e)
        except Exception as e:
            #messages.error(request, str(e).split("\"")[1])
            messages.error(request, e)
    return HttpResponseRedirect("/Timesheet/")

def edittimesheetfun(request):
    if request.method == 'POST':
        id = request.POST.get('tid')
        working_hours = request.POST.get('working_hours')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        try:
            timesheet = get_object_or_404(Timesheet, id=id)
            timesheet.working_hours = working_hours
            timesheet.start_time = start_time
            timesheet.end_time = end_time
            with transaction.atomic():
                timesheet.save()
            return HttpResponseRedirect("/Timesheet/")
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    else:
        messages.error(request, 'Could not save the details')
    return HttpResponseRedirect("/Timesheet/")

def delete_timesheetfun(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/pages-register/")
    instance = get_object_or_404(Timesheet, id=id)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect("/Timesheet/")
    return HttpResponseRedirect("/Timesheet/")

#Employee
def EmployeeDepartmentfun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        query = request.GET.get('q')
        if query:
            empdata = Employee.objects.filter(
                Q(employee_id__icontains=query) | 
                Q(employee_name__icontains=query) |
                Q(employee_email__icontains=query) |
                Q(employee_phone__icontains=query)
            )
        else:
            empdata = Employee.objects.all()
        
        context = {
            "empdata": empdata,
        }
        return render(request, 'pcapp/EmployeeDepartment.html', context)
    else:
        return render(request, "pcapp/pages-register.html")

def addemployeefun(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee_name = request.POST.get('employee_name')
        employee_email = request.POST.get('employee_email')
        employee_phone = request.POST.get('employee_phone')
        try:
            if Employee.objects.filter(employee_id=employee_id).first():
                messages.error(request, 'Employee ID already exist')
                return HttpResponseRedirect("/EmployeeDepartment/")
            else:
                employee = Employee(employee_id=employee_id, 
                                    employee_name=employee_name, 
                                    employee_email=employee_email, 
                                    employee_phone=employee_phone
                                    )
                employee.save()
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    return HttpResponseRedirect("/EmployeeDepartment/")

def editemployeefun(request):
    if request.method == 'POST':
        # Get the employee data from the form
        employee_id = request.POST.get('employee_id')
        employee_name = request.POST.get('employee_name')
        employee_phone = request.POST.get('employee_phone')
        employee_email = request.POST.get('employee_email')
        try:
            employee = Employee.objects.get(employee_id=employee_id)
        
            employee.employee_name = employee_name
            employee.employee_phone = employee_phone
            employee.employee_email = employee_email
            with transaction.atomic():
                employee.save()
            return HttpResponseRedirect("/EmployeeDepartment/")
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    else:
        messages.error(request, 'Could not save the details')
    return HttpResponseRedirect("/EmployeeDepartment/")

def delete_employeefun(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/pages-register/")
    instance = get_object_or_404(Employee, employee_id=id)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect("/EmployeeDepartment/")
    return HttpResponseRedirect("/EmployeeDepartment/")

#Department
def Departmentfun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        query = request.GET.get('q')
        if query:
            deptdata = Department.objects.filter(
                Q(department_id__icontains=query) | 
                Q(department_name__icontains=query)
            )
        else:
            deptdata = Department.objects.all()
        
        context = {
            "deptdata": deptdata,
        }
        return render(request, 'pcapp/Department.html', context)
    else:
        return render(request, "pcapp/pages-register.html")
    return render(request, 'pcapp/Department.html', context)

def addDepartmentfun(request):
    if request.method == 'POST':
        department_id = request.POST.get('department_id')
        department_name = request.POST.get('department_name')
        try:
            if Department.objects.filter(department_id=department_id).first() or Department.objects.filter(department_name=department_name).first():
                messages.error(request, 'Department ID or Name already exist, select another Department ID')    # , 'Department ID already exist, select another Department ID'
                return HttpResponseRedirect("/Department/")
            else:
                department = Department(department_id=department_id, 
                                    department_name=department_name
                                    )
                department.save()
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
        return HttpResponseRedirect("/Department/")
    return HttpResponseRedirect("/Department/")

def editDepartmentfun(request):
    if request.method == 'POST':
        department_id = request.POST.get('department_id')
        department_name = request.POST.get('department_name')
        try:
            department = Department.objects.filter(department_id=department_id).first()
            if department:
                if Department.objects.filter(department_name=department_name).first():
                    messages.error(request, 'Department Name already exist, select another Departemnt Name')
                else:
                    department.department_name = department_name
            else:
                messages.error(request, 'Could not find the record in database, contact database admin')
                return HttpResponseRedirect("/Department/")
            with transaction.atomic():
                department.save()
        except Exception as e:
            messages.error(request, str(e).split("\"")[1])
        return HttpResponseRedirect("/Department/")
    else:
        messages.error(request, 'Could not save the details')
    return HttpResponseRedirect("/Department/")

def delete_Departmentfun(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/pages-register/")
    try:
        instance = get_object_or_404(Department, department_id=id)
        if request.method == 'POST':
            instance.delete()
            return HttpResponseRedirect("/Department/")
    except Exception as e:
        messages.error(request, 'An error occurred while trying to delete the department.')
    return redirect('Department')

#-------------------------------------------------------------------------------------------------------
#register, login, logout
def regfun(request): #for user registration
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['cpassword']
        try:
            if password == c_password:
                user = User.objects.create(
                    name=name,
                    email=email,
                    password=password
                )
                user.set_password(password)
                user.save()
                messages.success(request, 'User registered successfully!')
                return redirect('pages-register')
            else:
                messages.error(request, 'Passwod doesnot match please write correct password')
                return redirect('pages-register')
        except Exception as e:
            messages.error(request, 'Error registering user')
    # Render the home.html template for GET requests
    return render(request, 'pcapp/pages-register.html')

def loginffun(request):  #for user login
    try:
        if request.method == 'POST':
            email = request.POST.get('loginemail')
            password = request.POST.get('loginpassword')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active: 
                    if user.is_approved:
                        login(request, user)
                        return HttpResponseRedirect("/index/")  # Redirect to index page on successful login
                    else:
                        messages.error(request, 'Account is not Activated, please contact Admin to Activate your account')
                        return HttpResponseRedirect("/pages-register/")  # Redirect to pages-register on failure
                else:
                    messages.error(request, 'Account is not Activ, please contact Admin to Activate your account')
                    return HttpResponseRedirect("/pages-register/")  # Redirect to pages-register on failure
            else:
                messages.error(request, 'Invalid login credentials')
                return HttpResponseRedirect("/pages-register/")  # Redirect to pages-register on failure
        else:
            return render(request, "pcapp/index.html")
    except Exception as e:
        messages.error(request, 'An error occurred: {}'.format(str(e)))
        return HttpResponseRedirect("/pages-register/")  # Redirect to pages-register on failure
		
def logoutfun(request):	 #for user logout
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return HttpResponseRedirect("/pages-register/")




#Material Supplier
def MaterialSupplierfun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        query = request.GET.get('q')
        if query:
            materialdata = MaterialSupplier.objects.filter(
                Q(supplier_id__icontains=query) | 
                Q(supplier_name__icontains=query) |
                Q(business_name__icontains=query) |
                Q(phone_support_queries__icontains=query) |
                Q(email_support_queries__icontains=query) |
                Q(material_supply_category__icontains=query) 
            )
        else:
            materialdata = MaterialSupplier.objects.all()
        
        context = {
            "materialdata": materialdata,
        }
        return render(request, 'pcapp/MaterialSupplier.html', context)
    else:
        return render(request, "pcapp/pages-register.html")

def addMaterialSupplierfun(request): 
    if request.method == 'POST':
        supplier_name = request.POST.get('supplier_name')
        business_name = request.POST.get('business_name')
        business_address = request.POST.get('business_address')
        phone_support_queries = request.POST.get('phone_support_queries')
        email_support_queries = request.POST.get('email_support_queries')
        material_supply_category = request.POST.get('material_supply_category')
        try:
            matsupplier = MaterialSupplier(supplier_name=supplier_name, 
                                business_name=business_name, 
                                business_address=business_address, 
                                phone_support_queries=phone_support_queries, 
                                email_support_queries=email_support_queries, 
                                material_supply_category=material_supply_category
                                )
            matsupplier.save()
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    return HttpResponseRedirect("/MaterialSupplier/")

def editMaterialSupplierfun(request):
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_id')
        supplier_name = request.POST.get('supplier_name')
        business_name = request.POST.get('business_name')
        business_address = request.POST.get('business_address')
        phone_support_queries = request.POST.get('phone_support_queries')
        email_support_queries = request.POST.get('email_support_queries')
        material_supply_category = request.POST.get('material_supply_category')
        try:
            matsupplier = MaterialSupplier.objects.get(supplier_id=supplier_id)
        
            matsupplier.supplier_name = supplier_name
            matsupplier.business_name = business_name
            matsupplier.business_address = business_address
            matsupplier.phone_support_queries = phone_support_queries
            matsupplier.email_support_queries = email_support_queries
            matsupplier.material_supply_category = material_supply_category
            with transaction.atomic():
                matsupplier.save()
            return HttpResponseRedirect("/MaterialSupplier/")
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    else:
        messages.error(request, 'Could not save the details')
    return HttpResponseRedirect("/MaterialSupplier/")

def delete_MaterialSupplierfun(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/pages-register/")
    instance = get_object_or_404(MaterialSupplier, supplier_id=id)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect("/MaterialSupplier/")
    return HttpResponseRedirect("/MaterialSupplier/")



# Stores Branch Names
def StoresBranchNamesfun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        query = request.GET.get('q')
        materialsupplierdata = MaterialSupplier.objects.all()
        
        if query:
            storebranchdata = StoresBranchNames.objects.filter(
                Q(ABN__icontains=query) | 
                Q(supplier_id__supplier_id__icontains=query) |
                Q(store_id__icontains=query) |
                Q(branch_name__icontains=query) |
                Q(address__icontains=query) |
                Q(branch_contact__icontains=query) |
                Q(phone__icontains=query) |
                Q(email__icontains=query) |
                Q(region_of_operation__icontains=query) 
            )
        else:
            storebranchdata = StoresBranchNames.objects.all()
        
        context = {
            "storebranchdata": storebranchdata,
            "materialsupplierdata":materialsupplierdata,
        }
        return render(request, 'pcapp/Stores.html', context)
    else:
        return render(request, "pcapp/pages-register.html")


def addStoresBranchNamesfun(request):
    if request.method == 'POST':
        ABN = request.POST.get('ABN')
        supplier_id = request.POST.get('supplier_id')
        store_id = request.POST.get('store_id')
        branch_name = request.POST.get('branch_name')
        address = request.POST.get('address')
        region_of_operation = request.POST.get('region_of_operation')
        branch_contact = request.POST.get('branch_contact')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        try:
            materialsupplierdata = MaterialSupplier.objects.get(supplier_id=supplier_id)
            if StoresBranchNames.objects.filter(ABN=ABN).first():
                    messages.error(request, 'Record already exist') 
                    return HttpResponseRedirect("/Stores/")
            else:
                storebranch = StoresBranchNames(ABN=ABN,
                                    supplier_id=materialsupplierdata, 
                                    store_id=store_id, 
                                    branch_name=branch_name, 
                                    address=address, 
                                    region_of_operation=region_of_operation,
                                    branch_contact=branch_contact, 
                                    phone=phone, 
                                    email=email
                                    )
                storebranch.save()
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    return HttpResponseRedirect("/Stores/")




def editStoresBranchNamesfun(request):
    if request.method == 'POST':
        ABN = request.POST.get('ABN')
        supplier_id = request.POST.get('supplier_id')
        store_id = request.POST.get('store_id')
        branch_name = request.POST.get('branch_name')
        address = request.POST.get('address')
        region_of_operation = request.POST.get('region_of_operation')
        branch_contact = request.POST.get('branch_contact')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        try:
            storebranchdata = get_object_or_404(StoresBranchNames, ABN=ABN)
            storebranchdata.store_id = store_id
            storebranchdata.branch_name = branch_name
            storebranchdata.address = address
            storebranchdata.region_of_operation = region_of_operation
            storebranchdata.branch_contact = branch_contact
            storebranchdata.phone = phone
            storebranchdata.email = email
            with transaction.atomic():
                storebranchdata.save()
            return HttpResponseRedirect("/Stores/")
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    else:
        messages.error(request, 'Could not save the details')
    return HttpResponseRedirect("/Stores/")


def delete_StoresBranchNamesfun(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/pages-register/")
    instance = get_object_or_404(StoresBranchNames, ABN=id)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect("/Stores/")
    return HttpResponseRedirect("/Stores/")








# Material Invoice
def MaterialInvoicefun(request):
    if request.user.is_staff or request.user.is_admin or request.user.is_active:   
        query = request.GET.get('q')
        storebranchdata = StoresBranchNames.objects.all()
        if query:
            matinvoicedata = MaterialInvoice.objects.filter(
                Q(ABN__ABN__icontains=query) | 
                Q(items__icontains=query) |
                Q(quantity__icontains=query) |
                Q(individual_price__icontains=query) |
                Q(total_price__icontains=query) |
                Q(approver__icontains=query) |
                Q(date_time__icontains=query) 
            )
        else:
            matinvoicedata = MaterialInvoice.objects.all()
        
        context = {
            "matinvoicedata": matinvoicedata,
            "storebranchdata":storebranchdata,
        }
        return render(request, 'pcapp/MaterialInvoice.html', context)
    else:
        return render(request, "pcapp/pages-register.html")


def addMaterialInvoicefun(request):
    if request.method == 'POST':
        ABN = request.POST.get('ABN')
        items = request.POST.get('items')
        quantity = int(request.POST.get('quantity'))
        individual_price = Decimal(request.POST.get('individual_price'))
        total_price = quantity * individual_price
        approver = request.POST.get('approver')
        try:
            storeabn = StoresBranchNames.objects.get(ABN=ABN)
            matinvoicedata = MaterialInvoice(ABN=storeabn,
                                items=items, 
                                quantity=quantity, 
                                individual_price=individual_price, 
                                total_price=total_price, 
                                approver=approver
                                )
            matinvoicedata.save()
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    return HttpResponseRedirect("/MaterialInvoice/")




def editMaterialInvoicefun(request):
    if request.method == 'POST':
        invoice_id = request.POST.get('invoice_id')
        items = request.POST.get('items')
        quantity = int(request.POST.get('quantity'))
        individual_price = Decimal(request.POST.get('individual_price'))
        total_price = quantity * individual_price
        approver = request.POST.get('approver')
        try:
            matinvdata = get_object_or_404(MaterialInvoice, invoice_id=invoice_id)
            matinvdata.items = items
            matinvdata.quantity = quantity
            matinvdata.individual_price = individual_price
            matinvdata.total_price = total_price
            matinvdata.approver = approver
            with transaction.atomic():
                matinvdata.save()
            return HttpResponseRedirect("/MaterialInvoice/")
        except IntegrityError as e:
            # Extract the duplicate entry from the error message
            split_message = str(e).split("'")
            if len(split_message) > 1:
                duplicate_entry = split_message[1]
                messages.error(request, f'{duplicate_entry} already exist')
            else:
                messages.error(request, str(e))
        except Exception as e:
            split_message = str(e).split("\"")
            if len(split_message) > 1:
                error_message = split_message[1]
                messages.error(request, error_message)
            else:
                messages.error(request, str(e))
    else:
        messages.error(request, 'Could not save the details')
    return HttpResponseRedirect("/MaterialInvoice/")


def delete_MaterialInvoicefun(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/pages-register/")
    instance = get_object_or_404(MaterialInvoice, invoice_id=id)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect("/MaterialInvoice/")
    return HttpResponseRedirect("/MaterialInvoice/")

