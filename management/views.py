from django.shortcuts import render,redirect

from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Sum
from .filters import OwnerFilter,BillFilter
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    owner = Owner.objects.all()
    filter = OwnerFilter(request.GET,queryset=owner)
    owner = filter.qs
    context = {'owners':owner,'filter':filter}
    return render(request,'index.html',context)

@login_required(login_url='login')
def register(request):
    form = OwnerForm()

    if request.method == 'POST':
        form = OwnerForm(request.POST)
        flat = form['flat'].value()
        floor = form['floor'].value()
        if not(Owner.objects.filter(flat=flat,floor=floor).exists()):
            form.save()
            name = form['name'].value()
            messages.success(request,f'Congratulations! Account was created for {name}.')
            return redirect('home')
        else:
            messages.info(request,f'Flat owner for {floor}{flat} already exists')
    
    context = {'form':form,'word':'Enter'}
    return render(request,'register.html',context)

def bills(request):
    bill = Bill.objects.last()
    form = BillForm(request.POST)
    
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bills')
    context = {'form':form,'bill':bill}
    return render(request,'bills.html',context)

def loginPage(request):
    if request.method == 'POST':
        user = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=user,password=password)
        if user is None:
            messages.info(request,'Your Username or Password is incorrect')
            return redirect('login')
        else:
            login(request,user)
            return redirect('/')

    return render(request,'login.html')

def logOut(request):
    logout(request)
    return redirect('/')

@login_required(login_url='login')
def update(request,pk):
    owner = Owner.objects.get(id=pk)
    form = OwnerForm(instance=owner)

    if request.method == 'POST':
        form = OwnerForm(request.POST,instance=owner)
        form.save()
        name = form['name'].value()
        messages.success(request,f'Congratulations! Account was updated for {name}.')
        return redirect('home')

    context = {'form':form,'word':'Update'}
    return render(request,'register.html',context)

@login_required(login_url='login')
def deleteOwner(request,pk):
    owner = Owner.objects.get(id=pk)

    if request.method == 'POST':
        admin = request.POST.get('admin')
        password = request.POST.get('password')

        validate = authenticate(username=admin,password=password)
        if validate is not None:
            owner.delete()
            return redirect('/')
        else:
            messages.info(request,"username or password doesn't match")

    context = {'owner':owner} 
    return render(request,'delete.html',context)

def bill_info(request,key):

    bills = Bill.objects.last()
    info = Payment.objects.all()
    if info.count() < 1:
        messages.info(request,"No payment entries available.")
        return redirect('bills')

    owner_count = Owner.objects.all().count()

    water_due = bills.water - list(Payment.objects.all().aggregate(Sum('water_bill')).values())[0]
    current_due = bills.current - list(Payment.objects.all().aggregate(Sum('current_bill')).values())[0]
    gas_due = bills.gas - list(Payment.objects.all().aggregate(Sum('gas_bill')).values())[0]
    service_due = bills.service_charge - list(Payment.objects.all().aggregate(Sum('servicecharge')).values())[0] 
    extra_due = bills.extra - list(Payment.objects.all().aggregate(Sum('extracharge')).values())[0]

    def due_list(lst,per_person):
        due_lst = []
        for i in lst:
            for val in i.values():
                due_lst.append(per_person-val)
        return due_lst
    
    water_info = Payment.objects.all().values('water_bill')
    current_info = Payment.objects.all().values('current_bill')
    gas_info = Payment.objects.all().values('gas_bill')
    service_info = Payment.objects.all().values('servicecharge')
    extra_info = Payment.objects.all().values('extracharge')

    water_due_lst = due_list(water_info,bills.water/owner_count)
    current_due_lst = due_list(current_info,bills.current/owner_count)
    gas_due_lst = due_list(gas_info,bills.gas/owner_count)
    service_due_lst = due_list(service_info,bills.service_charge/owner_count)
    extra_due_lst = due_list(extra_info,bills.extra/owner_count)


    dict = {'1':['Water',bills.water,bills.water/owner_count,info.values('name','flat','floor','water_bill'),water_due,water_due_lst],
            '2':['Electricity',bills.current,bills.current/owner_count,info.values('name','flat','floor','current_bill'),current_due,current_due_lst],
            '3':['Gas',bills.gas,bills.gas/owner_count,info.values('name','flat','floor','gas_bill'),gas_due,gas_due_lst],
            '4':['Service Charge',bills.service_charge,bills.service_charge/owner_count,info.values('name','flat','floor','servicecharge'),service_due,service_due_lst],
            '5':['Extra',bills.extra,bills.extra/owner_count,info.values('name','flat','floor','extracharge'),extra_due,extra_due_lst]
            }
    #owner = Owner.objects.all()
    filter = BillFilter(request.GET,queryset=dict[key][3])
    dict[key][3] = filter.qs
    context = {'bills':dict[key],'filter':filter}
    return render(request,'bills_info.html',context)

@login_required(login_url='login')
def payment(request):
    form = PaymentForm()

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,'payment.html',context)

@login_required(login_url='login')
def update_payment(request,pk):
    owner = Owner.objects.get(id=pk)
    payment = Payment.objects.get(name=owner)
    form = PaymentForm(instance=payment)

    if request.method == 'POST':
        form = PaymentForm(request.POST,instance=payment)
        form.save()
        flat = form['flat'].value()
        floor = form['floor'].value()
        messages.info(request,f'Bill for {floor}{flat} updated')
        return redirect('/')

    context = {'form':form}
    return render(request,'payment.html',context)

@login_required(login_url='login')
def delete_payment(request,pk):

    if request.method == 'POST':
        payment = Payment.objects.get(id=pk)
        admin = request.POST.get('admin')
        password = request.POST.get('password')

        validate = authenticate(username=admin,password=password)
        if validate is not None:
            payment.delete()
            return redirect('bills')
        else:
            messages.info(request,"username or password doesn't match")

    owner = Owner.objects.get(id=pk)
    payment = Payment.objects.get(name=owner)
    context = {'payment':payment} 
    return render(request,'delete_payment.html',context)

def view(request,pk):
    owner = Owner.objects.get(id=pk)
    try:
        payment = Payment.objects.get(name=pk)
        context = {'owner':owner,'payment':payment}
    except:
        context = {'owner':owner}
    
    return render(request,'view.html',context)