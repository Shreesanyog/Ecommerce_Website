from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from datetime import datetime
from store.models import Product, Cart, ContactSubmission
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User


def index(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_count = 0
    
    products = Product.objects.all()  # Retrieve all products from the database
    
    context = {
        'cart_count': cart_count,
        'products': products,  # Pass the products to the template context
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request,'about.html')
def help(request):
    return render(request,'help.html')

# def contact(request):
#     if request.method=="POST":
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone= request.POST.get('phone')
#         desc = request.POST.get('desc')
#         contact=Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
#         contact.save()
#     return render(request,'contact.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save form data to the database
        ContactSubmission.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        # Redirect to the home page after successful form submission
        return redirect('/')
    
    return render(request,'contact.html')

def handlelogin(request):
    if request.method=="POST":
        uname=request.POST.get("username")
        pass1=request.POST.get("pass1")
        myuser=authenticate(username=uname,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentails")
            return redirect('/login')
    return render(request,'login.html')

def handlesignup(request):
    if request.method=="POST":
        uname=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("pass1")
        confirmpassword=request.POST.get("pass2")
        # print(uname,email,password,confirmpassword)
        if password!=confirmpassword:
            messages.warning(request,"Password is Incorrect")
            return redirect('/signup')


        try:
            if User.objects.get(username=uname):
                messages.info(request,"UserName Is Taken")
                return redirect('/signup')
        except:
            pass
        try:
            if User.objects.get(email=email):
                messages.info(request,"Email Is Taken")
                return redirect('/signup')
        except:
            pass
    
        myuser=User.objects.create_user(uname,email,password)
        myuser.save()
        messages.success(request,"Signup Success Please login!")
        return redirect('/login')
              
    return render(request,'signup.html')


def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/login')

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

    
@login_required
def add_to_cart(request, product_id):
    print("add_to_cart function called")  # Add this line to check if the function is called
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.add(product)
        cart_count = cart.items.count()  # Get the updated cart count
        
        print("Product added to cart:", product.name)  # Add this line to check if the product is added to the cart
        print("Cart count:", cart_count)  # Add this line to check the cart count
        
        return JsonResponse({'cart_count': cart_count})  # Return the cart count as JSON
    else:
        return HttpResponse("You must be logged in to add items to your cart.")




@login_required
def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items_count = cart.items.count()
    except Cart.DoesNotExist:
        cart_items_count = 0
        cart = None

    context = {
        'cart_items_count': cart_items_count,
        'cart': cart,
    }

    return render(request, 'cart.html', context)
