from django.shortcuts import render, get_object_or_404
from .forms import (ItemForm, JRForm, UserLoginForm, UserRegisterForm, SupForm,
                    ReqForm, IncomeForm)
from .models import (product_card, user_bin, bin, journal_request, req_bin,
                    journal_supplier, income)
from django.shortcuts import redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from collections import Counter


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('pug_store')
    return render(request, "interface/form.html", {'form': form,
                                         'title': title})

def register_view(request):
    title = "Регистрация"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        log_user = authenticate(username=user.username, password=password)
        login(request, log_user)
        return redirect('pug_store')
    return render(request, "interface/form.html", {'form': form,
                                         'title': title})

def logout_view(request):
    logout(request)
    return redirect('login_view')


def pug_store(request):
    items = product_card.objects.filter(vision=True)
    return render(request, 'interface/pug_store.html', {'items': items})

@login_required(login_url='/login/')
def add_item(request):
    if request.user.username == 'basuluu':
        if request.method == "POST":
            form  = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                item = form.save(commit=False)
                item.save()
                return redirect('detail', id=item.id)
        else:
            form = ItemForm()
        return render(request, 'interface/add_item.html', {'form': form})
    else:
        return redirect('pug_store')

@login_required(login_url='/login/')
def add_sup(request):
    if request.user.username == 'basuluu':
        if request.method == "POST":
            form  = SupForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.save()
                return redirect('journal_sup')
        else:
            form = SupForm()
        return render(request, 'interface/add_item.html', {'form': form})
    else:
        return redirect('pug_store')

@login_required(login_url='/login/')
def add_income(request):
    if request.user.username == 'basuluu':
        if request.method == "POST":
            form  = IncomeForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.save()
                return redirect('journal_income')
        else:
            form = IncomeForm()
        return render(request, 'interface/add_income.html', {'form': form})
    else:
        return redirect('pug_store')

@login_required(login_url='/login/')
def edit_item(request, id):
    if request.user.username == 'basuluu':
        item = get_object_or_404(product_card, id=id)
        if request.method == "POST":
            form  = ItemForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                item = form.save(commit=False)
                item.save()
                return redirect('detail', id=item.id)
        else:
            form = ItemForm(instance=item)
            return render(request, 'interface/add_item.html', {'form': form})
    else:
        return redirect('pug_store')

def detail(request, id):
    item = get_object_or_404(product_card, id=id)
    if request.method == "POST":
        if request.user.is_anonymous:
            return redirect('login_view')
        obj = user_bin.objects.filter(user=request.user)
        if len(obj):
            for record in obj:
                if record.id_bin.id_item.id == int(id) and record.pay_status == False:
                    q = bin.objects.filter(id_item=id, id=record.id_bin.id)
                    q.update(num=q[0].num+1)
                    return redirect('bin_v')
        obj = bin.objects.create(id_item=item, num=1)
        user_bin.objects.create(id_bin=obj, user=request.user)
        return redirect('bin_v')
    return render(request, 'interface/detail.html', {'item': item})

@login_required(login_url='/login/')
def bin_v(request):
    if request.method == "POST":
        return redirect('add_request')
    items = user_bin.objects.filter(user=request.user, pay_status=False)
    if len(list(request.GET.items())):
        if request.GET.get('Clear'):
            for item in items:
                bin.objects.filter(id=item.id_bin.id).delete()
            return redirect(bin_v)
        else:
            print('megakek')
            id = list(request.GET.keys())[0]
            bin.objects.filter(id=id).delete()
            return redirect(bin_v)
    arr = dict()
    total = 0
    for item in items:
        cost = item.id_bin.id_item.item_cost * item.id_bin.num
        arr[item.id_bin.id_item.item_name] = cost
        total += cost
    return render(request, 'interface/bin.html', {'items': items,
                                                  'arr': arr,
                                                  'total': total})
@login_required(login_url='/login/')
def add_request(request):
    if request.method == "POST":
        form  = JRForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            print(req)
            req.user = request.user
            req.save()
            print(req)
            bins = user_bin.objects.filter(user=request.user, pay_status=False)
            for bin in bins:
                req_bin.objects.create(id_req=req, id_bin=bin.id_bin)
            user_bin.objects.filter(user=request.user).update(pay_status=True)
            return redirect('pug_store')
    else:
        form = JRForm()
    return render(request, 'interface/add_request.html', {'form': form})

@login_required(login_url='/login/')
def journal_req(request):
    if request.user.username == 'basuluu':
        if request.method == "GET":
            req = journal_request.objects.all().order_by('-id')
            bins = req_bin.objects.all().order_by('-pk')

        else:
            req = journal_request.objects.all().order_by('id')
            bins = req_bin.objects.all().order_by('pk')
        return render(request, 'interface/journal_request.html', {'req': req,
                                                                'bins': bins})
    else:
        return redirect('pug_store')

@login_required(login_url='/login/')
def journal_sup(request):
    if request.user.username == 'basuluu':
        if request.method == "GET":
            obj = journal_supplier.objects.all()
        else:
            obj = journal_supplier.objects.all().order_by('-id')
        return render(request, 'interface/journal_supplier.html', {'obj': obj})
    else:
        return redirect('pug_store')

@login_required(login_url='/login/')
def journal_income(request):
    if request.user.username == 'basuluu':
        if request.method == "GET":
            obj = income.objects.all()
        else:
            obj = income.objects.all().order_by('-date')
        return render(request, 'interface/income.html', {'obj': obj})
    else:
        return redirect('pug_store')

@login_required(login_url='/login/')
def delete_item(request, id):
    if request.user.username == 'basuluu':
        item = get_object_or_404(product_card, id=id)
        item.delete()
        return redirect('pug_store')
    else:
        return redirect('pug_store')

def search_form(request):
    items = product_card.objects.filter(item_name__contains=request.GET['q'])
    return render(request, 'interface/pug_store.html', {'items': items})

def statistic(request):
    items = user_bin.objects.filter(pay_status=True)
    crunch = Counter()
    cost = dict()
    for item in items:
        crunch[item.id_bin.id_item.item_name] += item.id_bin.num
        cost[item.id_bin.id_item.item_name] = item.id_bin.id_item.item_cost
    crunch = dict(crunch)
    return render(request, 'interface/statistic.html', {'crunch': crunch,
                                                        'cost': cost})
