from django.shortcuts import render, HttpResponse, redirect
from gamestopapp.forms import AddProductForm, UpdateProductForm, UserRegisterForm, UserLoginForm, UpdateUserForm
from gamestopapp.models import Product, Cart, Orders, Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import  get_connection, EmailMessage
import random
from django.conf import settings
import razorpay


# Create your views here.
def index(request):
    
    return render(request, 'index.html')

@login_required(login_url= '/login')
def createProduct(request):
    
    if request.method == "GET":
        
        form = AddProductForm()
        
        context =  {'form': form}
    
        return render(request, 'addproduct.html', context)
    
    else:
        
        form = AddProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            form.save()
            
            return redirect('/products/view')
        
        else:
            
            context = {'error' : 'Product Not Saved'}
            
            return render(request, 'addproduct.html', context)
        
        
def readProduct(request):
    
    
    
    prod = Product.objects.filter(isAvailable = True)
    
    context =  {'data' : prod}  
    
    return render(request, 'showproducts.html', context)

def productDetails(request, rid):
    
    product = Product.objects.filter(id = rid)
    
    prod = Product.objects.get(id = rid)
    
    review = Review.objects.filter(product = prod)
    
    rating = 0
    n = 0
    
    for x in review:
        
        rating += x.rating
        n += 1

    avg_rating = int(rating/n)

    context = {'data' : product}
    
    context['rating'] = avg_rating
    
    return render(request, 'productdetail.html', context)

def updateProduct(request, rid):
    
    if request.method == "GET":
        
        prod = Product.objects.get(id = rid)
        
        form = UpdateProductForm()
        
        form.fields['name'].initial = prod.name
        form.fields['description'].initial = prod.description
        form.fields['manufacturer'].initial = prod.manufacturer
        form.fields['price'].initial = prod.price
        form.fields['category'].initial = prod.category        
        form.fields['isAvailable'].initial = prod.isAvailable
        
        context  = { 'form' : form }
    
        return render(request, 'updateproduct.html', context)
    
    else:
        
        prod = Product.objects.get(id = rid)
        
        form = UpdateProductForm(request.POST, instance = prod)
        
        if form.is_valid():
            
            form.save()
            
            return redirect('/products/view')
        
        else:
            
            return HttpResponse('Products Not Saved')
        

def deleteProduct(request, rid):
    
    prod = Product.objects.filter(id = rid)
    
    prod.delete()
    
    return redirect('/products/view')
        
        
def userRegister(request):
    
    if request.method == 'GET':
        
        form = UserRegisterForm()
        
        context = { 'form' : form }        
    
        return render(request, 'register.html', context)
    
    else:
        
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            
            password = form.cleaned_data['password']
            confirmPassword = form.cleaned_data['confirmPassword']
            
            if password == confirmPassword:
                
                user = form.save(commit= False)
                
                user.set_password(password)    
                
                user.save()
                    
                return redirect('/login')
                    
        else:
                
            return HttpResponse('Form Not Saved')
        
        
def userLogin(request): 
    
    if request.method == "GET":
    
        form = UserLoginForm()
        
        context = {'form' : form}
    
        return render(request, 'login.html', context)
    
    else:
        
        form = UserLoginForm(request.POST)
        
       
        if form.is_valid():
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']    
            
            user = authenticate(username = username, password = password)
            
            if user is not None:
                
                login(request, user)
                
                return redirect('/')
            
            else:
                
                return HttpResponse('username password incorrectot') 
        
        else:
            
            return HttpResponse('Form not valid')
            
            
def userLogout(request):
    
    logout(request)
    
    return redirect('/')

@login_required(login_url='/login')
def readUser(request):
    
    users = User.objects.all()
    
    context = {'data': users}
    
    return render(request, 'showusers.html', context)


def updateUser(request, rid):
    
    if request.method == 'GET':
        
        user = User.objects.get(id = rid)
        
        form = UpdateUserForm()
        
        print(user)
        
        form.fields['first_name'].initial = user.first_name
        form.fields['last_name'].initial = user.last_name
        form.fields['username'].initial = user.username
        form.fields['email'].initial = user.email
        form.fields['is_staff'].initial = user.is_staff
                
        context = {'form' : form}
    
        return render(request, 'updateuser.html', context)
    
    else:
        
        user = User.objects.filter(id = rid)
        
        form = UpdateUserForm(request.POST)
        
        if form.is_valid():
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            is_staff = form.cleaned_data['is_staff']
            
            user.update(first_name = first_name, last_name = last_name, username = username, email = email
                        , is_staff = is_staff) 
                       
            
            return redirect('/users/view')
       
        
@login_required(login_url='/login')    
def add_to_cart(request, rid):
    
    product = Product.objects.get(id = rid)
    
    data = Cart.objects.filter(user = request.user, product = product).exists()
    
    if data:
        
        return redirect('/cart')
    
    else:
        
        price = product.price
        
        cart = Cart.objects.create(user = request.user, product = product, price = price)
        
        cart.save()
        
        return redirect('/cart')


def cart(request):
    
    cart = Cart.objects.filter(user = request.user)
    
    total_price = 0
    
    for x in cart:
        total_price += x.price
    
    context = {'data' : cart}
    context['total_price'] = total_price
    
    return render(request, 'cart.html', context)


def removeCart(request, rid):
    
    data = Cart.objects.filter(id = rid)
    
    data.delete()
    
    return redirect('/cart')


def updateCart(request, cid, rid):
    
    data = Cart.objects.filter(id = rid)
    
    c = Cart.objects.get(id = rid)
    
    price = c.product.price * float(cid)
    
    data.update(quantity = cid, price = price )

    return redirect('/cart')

def add_to_order(request):
    
    data = Cart.objects.filter(user = request.user)
    
    total_price =  0
    
    for x in data:
        product = x.product
        quantity = x.quantity
        price = x.price
        
        total_price += x.price

        order = Orders.objects.create(user = request.user, product = product, quantity = quantity, price = price)
        
        order.save()
        
        
    client = razorpay.Client(auth= (settings.KEY_ID, settings.KEY_SECRET))
    
    payment = client.order.create({'amount' : int(total_price*100), 'currency' : 'INR', 'payment_capture' : 1}) 
    
    context = {'data' : payment}
    context['amount'] = int(total_price*100)
    
    data.delete()
    
    return render(request, 'payment.html', context)


def show_orders(request):
    
    data = Orders.objects.filter(user = request.user)
    
    context = {'data' : data}
    
    return render(request, 'orders.html', context)


def add_review(request, rid):
    
    product = Product.objects.get(id = rid)
    
    review = Review.objects.filter(product = product, user = request.user).exists()
    
    
    if review:
    
        return HttpResponse("Review Already Exist")
        
    else:
        
        if request.method == "GET":
        
            return render(request, 'addreview.html')
        
        else:
            
            rating = request.POST['rate']
            image = request.FILES['image']
            review = request.POST['review']
            
            r = Review.objects.create(user = request.user, product = product, rating = rating,
                                        image = image, review = review)
            
            r.save()
            
            return HttpResponse("Data Saved")    
        
        
def forgot_password(request):
    
    if request.method == "GET":
    
        return render(request, 'emailreturn.html')
    
    else:
        
        email = request.POST['email']
        
        request.session['email'] = email
        
        
        user = User.objects.filter(email = email).exists()
        
        
        if user:
        
            otp = random.randint(1000, 9999)
            
            request.session['email_otp'] = otp
            
            with get_connection(
                
                host = settings.EMAIL_HOST,
                port = settings.EMAIL_PORT,
                username = settings.EMAIL_HOST_USER,
                password = settings.EMAIL_HOST_PASSWORD,
                use_tls = settings.EMAIL_USE_TLS
                
                
            ) as connection :
                
                subject = "OTP Verification"
                email_from = settings.EMAIL_HOST_USER
                recipetion_list = [ email ]
                message = f"OTP is {otp}"
                
                EmailMessage(subject, message, email_from, recipetion_list, connection= connection).send()
                
                
                return redirect('/verify_otp')
            
        else:

                return HttpResponse("User is Not registered")            


def verify_otp(request):
    
    if request.method == "GET":
    
        return render(request, 'otpverification.html')
    
    
    else:
        
        user_otp = int(request.POST['otp'])
        
        
        email_otp = int(request.session['email_otp'])
        
        if user_otp == email_otp: 
             
            
            return redirect('/change_password')
        
        else:
            
            return redirect('/forgot_password')
        
        
def change_password(request):
    
    
    if request.method == "GET":
    
        return render(request, 'newpassword.html')
    
    else:
        
        email = request.session['email']
            
        password = request.POST['password']
            
        confirmPassword = request.POST['confirmpassword']
        
        if password == confirmPassword:
            
            user = User.objects.get(email = email)
            
            user.set_password(password)
            
            user.save()
            
            return redirect('/login')
        
        else:
            
            return HttpResponse("Password and Confirm password does not match")
            
            