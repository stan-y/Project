import json
from django.shortcuts import render
from .models import Destination, User2, Wallet
from .models import Detailed_desc
from .models import pessanger_detail
from .models import Cards
from .models import Transactions
from .models import NetBanking
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import *
from django.utils.dateparse import parse_date
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
from django import forms
from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.template import Library
from datetime import datetime
from django.contrib.auth.models import User
from paynow import Paynow
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError



import random

#  __lte=      is eqivelent to lessthan or euivelent
#    table.all().filter().exclude().filer()   for two filters and one excluding condition
# Create your views here.

def index(request):
    userid = request.user.id
    
    dests = Destination.objects.all()
    dest1 = []
    j=0
    for i in range(6):
        j=j+2
        temp =Detailed_desc.objects.get(dest_id=j)
        dest1.append(temp)

    try:
        user = User.objects.get(id = userid)
        u = User2.objects.get(user = user)
        return render(request, 'index.html',{'dests': dests, 'dest1' : dest1, 'balance' : u.balance})
    except:
        return render(request, 'index.html',{'dests': dests, 'dest1' : dest1 })

  

def result_url(request):
    dests = Destination.objects.all()
    dest1 = []
    j=0
    print(request.body)
    for i in range(6):
        j=j+2
        temp =Detailed_desc.objects.get(dest_id=j)
        dest1.append(temp)

    return render(request, 'index.html',{'dests': dests, 'dest1' : dest1})

def return_url(request):
    dests = Destination.objects.all()
    dest1 = []
    j=0
    print(request.body)
    for i in range(6):
        j=j+2
        temp =Detailed_desc.objects.get(dest_id=j)
        dest1.append(temp)

    return render(request, 'index.html',{'dests': dests, 'dest1' : dest1})

def topup(request):

    paynow = Paynow(
    '15441', 
    'f4a5d055-d142-4daa-bb13-86e908cc7f42',
    'http://127.0.0.1:8000/return_url', 
    'http://127.0.0.1:8000/result_url'
    )

    payment = paynow.create_payment('Order #100', 'test@example.com')

    payment.add('Bananas', 2.50)
    payment.add('Apples', 3.40)

    # Save the response from paynow in a variable
    response = paynow.send(payment)

    if response.success:
        # Get the link to redirect the user to, then use it as you see fit
        link = response.redirect_url

        # Get the poll url (used to check the status of a transaction). You might want to save this in your DB
        pollUrl = response.poll_url

        return redirect(link)

        # print("Poll Url: ", poll_url)

        # status = paynow.check_transaction_status(poll_url)

        # time.sleep(30)

        # print("Payment Status: ", status.status)
    return redirect(request.META.get('HTTP_REFERER'))



    dests = Destination.objects.all()
    dest1 = []
    j=0
    for i in range(6):
        j=j+2
        temp =Detailed_desc.objects.get(dest_id=j)
        dest1.append(temp)

    return render(request, 'index.html',{'dests': dests, 'dest1' : dest1})

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, last_name=last_name,
                                                first_name=first_name)

                user.save()

                print('user Created')
                return redirect('login')
        else:
            messages.info(request, 'Password is not matching ')
            return redirect('register')
        return redirect('index')
    else:
        return render(request, 'register.html')

def rfid(request):
    if request.method == 'POST':
        # card = request.POST['card']
        data = json.loads(request.body)
        card = data['card']
        try:
            user = User2.objects.get(cardId=card)
        except User2.DoesNotExist:
            data = {'message': "Card does not exist"}
            return JsonResponse(data, safe=False)     

        data = {'balance': user.balance,
                'hasTicket': user.ticket
        }

        return JsonResponse(data, safe=False)
    else:
        return render(request, 'rfid.html')

def setBalance(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # card = request.POST['card']
        # newBalance = request.POST['newBalance']
        card = data['card']
        newBalance = data['newBalance']
        try:
            # hasTicket = request.POST['hasTicket']
            hasTicket = data['hasTicket']
        except MultiValueDictKeyError:
            hasTicket = False
        try:
            user = User2.objects.get(cardId=card)
        except User.DoesNotExist:
            data = {'message': "Card does not exist"}
            return JsonResponse(data, safe=False)  
          
        if hasTicket == 'true':
            user.ticket = True
        else:
            user.ticket = False
        user.balance =  newBalance
        user.save()

        data = {'newbalance': user.balance,
                'hasTicket': user.ticket,
                'message': 'Balance updated'
        }

        return JsonResponse(data, safe=False)
    else:
        return render(request, 'balance.html')

def setGps(request):
    if request.method == 'POST':
        # id = request.POST['id']
        # long = request.POST['long']
        # lat = request.POST['lat']
        data = json.loads(request.body)

        id = data['id']
        long = data['long']
        lat = data['lat']

        try:
            location = Detailed_desc.objects.get(dest_name='Rome')
        except User2.DoesNotExist:
            data = {'message': "Location does not exist"}
            return JsonResponse(data, safe=False)   

        location.lat = lat
        location.long = long
        location.save()  

        data = {'location': location.lat,
                'longitude': location.long,
                'name': location.dest_name
        }

        return JsonResponse(data, safe=False)
    else:
        return render(request, 'location.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            try:
                u = User2.objects.get(user = user)
            except User2.DoesNotExist:
                User2.objects.create(user_id = user.id, cardId = random.randint(100,1000))


            messages.info(request, 'Sucessfully Logged in')
            email = request.user.email
            print(email)
            content = 'Hello ' + request.user.first_name + ' ' + request.user.last_name + '\n' + 'You are logged in in our site.keep connected and keep travelling.'
            # send_mail('Alert for Login', content
            #           , 'travellotours89@gmail.com', [email], fail_silently=True)
            dests = Destination.objects.all()
            return render(request, 'index.html',{'dests':dests})
        else:
            messages.info(request, 'Invalid credential')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')




@login_required(login_url='login')
def destination_list(request,city_name):
    dests = Detailed_desc.objects.all().filter(country=city_name)
    return render(request,'travel_destination.html',{'dests': dests})


def destination_details(request,city_name):
    dest = Detailed_desc.objects.get(dest_name=city_name)
    price = dest.price
    request.session['price'] = price
    request.session['city'] = city_name
    return render(request,'destination_details.html',{'dest':dest})

def search(request):
    try:
        place1 = request.session.get('place')
        print(place1)
        dest = Detailed_desc.objects.get(dest_name=place1)
        print(place1)
        return render(request, 'destination_details.html', {'dest': dest})
    except:
        messages.info(request, 'Place not found')
        return redirect('index')

class KeyValueForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()
def pessanger_detail_def(request, city_name):
    KeyValueFormSet = formset_factory(KeyValueForm, extra=1)
    if request.method == 'POST':
        formset = KeyValueFormSet(request.POST)
        if formset.is_valid():
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            date1 = datetime.now().date()
            if temp_date < date1:
                return redirect('index')
            obj = pessanger_detail.objects.get(Trip_id=3)
            pipo_id = obj.Trip_same_id
            #pipo_id =4
            request.session['Trip_same_id'] = pipo_id
            price = request.session['price']
            city = request.session['city']
            print(request.POST['trip_date'])
            #temp_date = parse_date(request.POST['trip_date'])
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            usernameget = request.user.get_username()
            print(temp_date)
            request.session['n']=formset.total_form_count()
            for i in range(0, formset.total_form_count()):
                form = formset.forms[i]

                t = pessanger_detail(Trip_same_id=pipo_id,first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                                     age=form.cleaned_data['age'],
                                     Trip_date=temp_date,payment=price,username=usernameget,city=city)
                t.save()
                # print (formset.forms[i].form-[i]-value)

            obj.Trip_same_id = (pipo_id + 1)
            obj.save()
            no_of_person = formset.total_form_count()
            price1 = no_of_person * price
            TAX = price1 * 0.05
            TAX = float("{:.2f}".format(TAX))
            final_total = TAX + price1
            request.session['pay_amount'] = final_total
            userid = request.user.id
            cardId = User2.objects.get(user_id=userid).cardId
            
            return render(request,'payment.html', {'no_of_person': no_of_person,
                                                   'price1': price1, 'TAX': TAX, 'final_total': final_total,'city': city, 'cardId': cardId })
    else:
        formset = KeyValueFormSet()

        return render(request, 'sample.html', {'formset': formset, 'city_name': city_name, })

def add_funds(request):
    KeyValueFormSet = formset_factory(KeyValueForm, extra=1)
    if request.method == 'POST':
        formset = KeyValueFormSet(request.POST)
        if formset.is_valid():
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            date1 = datetime.now().date()
            if temp_date < date1:
                return redirect('index')
            obj = pessanger_detail.objects.get(Trip_id=3)
            pipo_id = obj.Trip_same_id
            #pipo_id =4
            request.session['Trip_same_id'] = pipo_id
            price = request.session['price']
            city = request.session['city']
            print(request.POST['trip_date'])
            #temp_date = parse_date(request.POST['trip_date'])
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            usernameget = request.user.get_username()
            print(temp_date)
            request.session['n']=formset.total_form_count()
            for i in range(0, formset.total_form_count()):
                form = formset.forms[i]

                t = pessanger_detail(Trip_same_id=pipo_id,first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                                     age=form.cleaned_data['age'],
                                     Trip_date=temp_date,payment=price,username=usernameget,city=city)
                t.save()
                # print (formset.forms[i].form-[i]-value)

            obj.Trip_same_id = (pipo_id + 1)
            obj.save()
            no_of_person = formset.total_form_count()
            price1 = no_of_person * price
            TAX = price1 * 0.18
            TAX = float("{:.2f}".format(TAX))
            final_total = TAX + price1
            request.session['pay_amount'] = final_total
            return render(request,'payment.html', {'no_of_person': no_of_person,
                                                   'price1': price1, 'TAX': TAX, 'final_total': final_total,'city': city })
    
    else:
        formset = KeyValueFormSet()

        return render(request, 'paynow.html', {'formset': formset })


def upcoming_trips(request):
    username = request.user.get_username()
    date1=datetime.now().date()
    person = pessanger_detail.objects.all().filter(username=username).filter(pay_done=1)
    person = person.filter(Trip_date__gte=date1)
    print(date1)
    return render(request,'upcoming trip1.html',{'person':person})

@login_required(login_url='login')
def card_payment(request):
    card_no = request.POST.get('card_number')
    pay_method = 'Debit card'
    MM = request.POST['MM']
    YY = request.POST['YY']
    CVV = request.POST['cvv']

    request.session['dcard'] = card_no
    try:
        balance = User2.objects.get(cardId=card_no).balance
    except User2.DoesNotExist:
            msg= 'Card does not exist'
            return render(request, 'wrongdata.html', {'info':msg})


    # mail1 = User.objects.get(cardId=card_no).email
    request.session['total_balance'] = balance

    if int(balance) >= int(request.session['pay_amount']):
        # print("Twist the coder")
        rno = random.randint(100000, 999999)
        request.session['OTP'] = rno

        amt = request.session['pay_amount']
        username = request.user.get_username()
        print(username)
        user = User.objects.get(username=username)
        mail_id = user.email
        print([mail_id])
        msg = 'Your OTP For Payment of ₹' + str(amt) + ' is ' + str(rno)
        # print(msg)
        # print([mail_id])
        # print(amt)
        # send_mail('OTP for Debit card Payment',
        #             msg,
        #             'travellotours89@gmail.com',
        #             [mail_id],
        #             fail_silently=False)
        return render(request, 'OTP.html')
    return render(request, 'wrongdata.html', {'info':'Insufficient Balance'})


    # except:
    #     return render(request, 'index.html')

@login_required(login_url='login')
def net_payment(request):
    username = request.POST['cardNumber']
    Password1 = request.POST['pass']
    Bank_name = request.POST['banks']
    usernameget = request.user.get_username()
    Trip_same_id1 = request.session['Trip_same_id']
    amt = int(request.session['pay_amount'])
    pay_method = 'Net Banking'
    try:
        r = NetBanking.objects.get(Username=username, Password=Password1,Bank=Bank_name)
        balance = r.Balance
        request.session['total_balance'] = balance
        if int(balance) >= int(request.session['pay_amount']):
            total_balance = int(request.session['total_balance'])
            rem_balance = int(total_balance - int(request.session["pay_amount"]))
            r.Balance = rem_balance
            r.save(update_fields=['Balance'])
            r.save()
            t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method, Status='Successfull')
            t.save()
            return render(request, 'confirmetion_page.html')
        else:
            t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method)
            t.save()
            return render(request, 'wrongdata.html')
    except :
        return render(request, 'wrongdata.html')

@login_required(login_url='login')
def otp_verification(request):
    # otp1 = int(request.POST['otp'])
    usernameget = request.user.get_username()
    Trip_same_id1 = request.session['Trip_same_id']
    amt = int(request.session['pay_amount'])
    pay_method = 'Debit card'
    # if otp1 == int(request.session['OTP']):

    # del request.session["OTP"]
    total_balance = int(request.session['total_balance'])
    rem_balance = int(total_balance-int(request.session["pay_amount"]))
    c = User2.objects.get(cardId=request.session['dcard'])
    c.ticket = True
    c.balance = rem_balance
    c.save(update_fields=['balance'])
    c.save()
    t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method, Status='Successfull')
    t.save()
    z = pessanger_detail.objects.all().filter(Trip_same_id=Trip_same_id1)
    for obj in z:
        obj.pay_done = 1
        obj.save(update_fields=['pay_done'])
        obj.save()
        print(obj.pay_done)
    return render(request, 'confirmetion_page.html')

    # else:
    #     t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method)
    #     t.save()
    #     return render(request, 'wrong_OTP.html')

@login_required(login_url='login')
def data_fetch(request):
    username = request.user.get_username()
    person = pessanger_detail.objects.all().filter(username=username)
