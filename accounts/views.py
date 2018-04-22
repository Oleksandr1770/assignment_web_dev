from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from passlib.hash import django_pbkdf2_sha256 as handler
from django.shortcuts import redirect
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import render_to_response
# Create your views here.
def home(request):
    return render(request, 'index.html')

def dashboard(request):
    try:
        session_id = request.COOKIES.get('ACCESS_TOKEN')
        account = Account.objects.filter(id=session_id)[:1]
        transactions = Transaction.objects.filter(username=account[0].username).order_by('-id')
        fname = account[0].first_name
        lname = account[0].last_name
    except Exception as e:
        return redirect(home)
    return render(request, 'dashboard.html', {'transactions': transactions, 'fname': fname, 'lname': lname})

def transactions(request):
    try:
        session_id = request.COOKIES['ACCESS_TOKEN']
        account = Account.objects.filter(id=session_id)[:1]
        transactions = Transaction.objects.filter(username=account[0].username).order_by('-id')
        fname = account[0].first_name
        lname = account[0].last_name
        categories = Category.objects.filter();
    except Exception as e:
        return redirect(home)
    return render(request, 'transactions.html', {'transactions': transactions, 'categories':categories, 'fname': fname, 'lname': lname})

def add_transaction(request):
    if request.method == "POST":
        session_id = request.COOKIES['ACCESS_TOKEN']
        account = Account.objects.filter(id=session_id)[:1]
        value = request.POST.get('value')
        transaction_type = request.POST.get('transaction_type')
        location = request.POST.get('location')
        date = request.POST.get('date')
        transaction = Transaction(date=date, username=account[0].username, transaction_type=transaction_type, value=value,location=location)
        if (transaction.date in [None, ''] or transaction.location in [None, ''] or transaction.value in [None, '']) is False:
            transaction.save()
        return redirect(transactions)
    return render(request, transactions)

def categories_page(request):
    try:
        session_id = request.COOKIES['ACCESS_TOKEN']
        account = Account.objects.filter(id=session_id)[:1]
        categories = Category.objects.filter();
        fname = account[0].first_name
        lname = account[0].last_name
    except Exception as e:
        return redirect(home)
    return render(request, 'categories.html', {'categories': categories, 'fname': fname, 'lname': lname})

def add_category(request):
    if request.method == "POST":
        name = request.POST['category']
        category = Category(name=name)
        if (category.name in [None, '']) is False:
            category.save()
        return redirect(categories_page)
    return render(request, categories_page)

@csrf_protect
def login(request):
    if request.method == "POST":
        username = request.POST['login_name']
        password = request.POST['login_password']
        user = Account.objects.filter(username=username)[:1]
        if user:
            hash_pass = user[0].password
            is_password_correct = handler.verify(password, hash_pass)
            if is_password_correct is False:
                return redirect(home)
            else:
                account = Account.objects.filter(username=username)[:1]
                transactions = Transaction.objects.filter(username=account[0].username).order_by('-id')
                fname = account[0].first_name
                lname = account[0].last_name
                response = HttpResponse()
                response = render(request, 'dashboard.html', {'transactions': transactions,'fname': fname, 'lname': lname})
                response.set_cookie('ACCESS_TOKEN', user[0].id)
                return response
    return render(request, 'index.html')

def logout(request):
    response = HttpResponse()
    response = render(request, 'index.html')
    response.set_cookie('ACCESS_TOKEN', '')
    return response

@csrf_protect
def register(request):
    if request.method == "POST":
        first_name = request.POST['fn']
        last_name = request.POST['ln']
        username = request.POST['un']
        email = request.POST['email']
        password = request.POST['psw']
        enc_password = handler.encrypt(password)
        user = Account(first_name=first_name, last_name=last_name, username=username, email=email, password=enc_password)
        user.save()
        return redirect(home)
    return redirect(home)

@csrf_protect
def filter(request):
    if request.method == "POST":
        session_id = request.COOKIES['ACCESS_TOKEN']
        account = Account.objects.filter(id=session_id)[:1]
        fname = account[0].first_name
        lname = account[0].last_name
        selected_type = request.POST['types'];
        transactions = Transaction.objects.filter(transaction_type=selected_type, username=account[0].username);
        categories = Category.objects.filter();
    return render(request, "transactions.html", {'categories': categories, 'transactions': transactions, 'fname': fname, 'lname': lname})

def users(request):
    if request.method == 'GET':
        if 'ACCESS_TOKEN' in request.COOKIES.keys():
            id = request.COOKIES['ACCESS_TOKEN']

            user = Account.objects.filter(id=id)
            if user:
                users = Account.objects.all().values('first_name', 'last_name', 'email', 'username')
                users_list = list(users)
                return JsonResponse(users_list, safe=False)
        
        return JsonResponse("Access denied", safe=False)
def user(request, id):
    if request.method == 'GET':
        if 'ACCESS_TOKEN' in request.COOKIES.keys():
            id = request.COOKIES['ACCESS_TOKEN']

            user = Account.objects.filter(id=id)
            if user:
                user = Account.objects.filter(id=id).values('first_name', 'last_name', 'email', 'username')
                user_list = list(user)
                return JsonResponse(user_list, safe=False)
        return JsonResponse("Access denied", safe=False)

def user_transactions(request, id):
    if request.method == 'GET':
        if 'ACCESS_TOKEN' in request.COOKIES.keys():
            id = request.COOKIES['ACCESS_TOKEN']

            user = Account.objects.filter(id=id)
            if user:
                user = Account.objects.filter(id=id).values('username')
                transactions = Transaction.objects.filter(username=user[0]['username'])
                transaction_list = list(transactions)
                return JsonResponse(transaction_list, safe=False)
        return JsonResponse("Access denied. User is not authorized", safe=False)

def categories(request):
    if request.method == 'GET':
        if 'ACCESS_TOKEN' in request.COOKIES.keys():
            id = request.COOKIES['ACCESS_TOKEN']

            user = Account.objects.filter(id=id)
            if user:
                categories = Category.objects.all().values('name')
                category_list = list()
                return JsonResponse(category_list, safe=False)
        return JsonResponse("Access denied. User is not authorized", safe=False)

def category(request, id):
    if request.method == 'GET':
        if 'ACCESS_TOKEN' in request.COOKIES.keys():
            id = request.COOKIES['ACCESS_TOKEN']

            user = Account.objects.filter(id=id)
            if user:
                category = Category.objects.filter(id=id)
                c_list = list(category)
                return JsonResponse(c_list, safe=False)
        return JsonResponse("Access denied. User is not authorized", safe=False)

def cat_transactions(request, id, category_id):
    if request.method == 'GET':
        if 'ACCESS_TOKEN' in request.COOKIES.keys():
            id = request.COOKIES['ACCESS_TOKEN']

            user = Account.objects.filter(id=id)
            if user:
                user = Account.objects.filter(id=id).values('username')
                category = Category.objects.filter(id=category_id)
                if category:
                    transactions = Transaction.objects.filter(username=user[0]['username'],transaction_type=category[0]['name'])
                    t_list = list(transactions)
                    return JsonResponse(t_list, safe=False)
                else:
                    return JsonResponse([], safe=False)
        return JsonResponse("Access denied. User is not authorized", safe=False)
