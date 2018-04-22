from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from passlib.hash import django_pbkdf2_sha256 as handler
from django.shortcuts import redirect
from .models import *
from django.http import HttpResponse, response

# Create your views here.
def home(request):
    return render(request, 'index.html')

def dashboard(request):
    try:
        session_id = request.session['user_id']
        account = Account.objects.filter(id=session_id)[:1]
        transactions = Transaction.objects.filter(username=account[0].username).order_by('-id')
        fname = account[0].first_name
        lname = account[0].last_name
    except Exception as e:
        return redirect(home)
    return render(request, 'dashboard.html', {'transactions': transactions, 'fname': fname, 'lname': lname})

def transactions(request):
    try:
        session_id = request.session['user_id']
        account = Account.objects.filter(id=session_id)[:1]
        transactions = Transaction.objects.filter(username=account[0].username).order_by('-id')
        fname = account[0].first_name
        lname = account[0].last_name
    except Exception as e:
        return redirect(home)
    return render(request, 'transactions.html', {'transactions': transactions, 'fname': fname, 'lname': lname})

def add_transaction(request):
    if request.method == "POST":
        session_id = request.session['user_id']
        account = Account.objects.filter(id=session_id)[:1]
        value = request.POST.get('value')
        transaction_type = request.POST.get('transaction_type')
        location = request.POST.get('location')
        date = request.POST.get('date')
        transaction = Transaction(date=date, username=account[0].username, transaction_type=transaction_type, value=value,location=location)
        transaction.save()
        return redirect(transactions)
    return render(request, transactions)

def categories(request):
    return render(request, 'categories.html')

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
                request.session['user_id'] = user[0].id
                return redirect(dashboard)
    return render(request, 'index.html')

def logout(request):
    del request.session['user_id']
    return redirect(home)

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
