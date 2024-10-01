from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib.auth import login
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os

# Create your views here.
def guest(request):
    return render(request,'guest.html')

def loginpage(request):
    return render(request,'loginpage.html')

def userlog(request):
    if request.method=='POST':
        U_name=request.POST['username']
        Pas=request.POST['password']
        user=auth.authenticate(username=U_name,password=Pas)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('adminhome')
            else:
                login(request,user)
                auth.login(request,user)
                return redirect('home')
        else:
            messages.info(request,"Invalid username or password")
            return redirect('loginpage')

    return render(request,'customerreg.html')

# def cartcount(request):
#     if request.user.is_authenticated:
#         # Find the user's cart
#         cart = Cart.objects.filter(user=request.user).first()
        
#         # If the user has a cart, count the distinct products in it
#         if cart:
#             cart_item_count = CartItem.objects.filter(cart=cart).values('product').distinct().count()
#         else:
#             cart_item_count = 0
#     else:
#         cart_item_count = 0
#     return render(request, 'home.html',{'cart_item_count': cart_item_count})


def customerreg(request):
    return render(request,'customerreg.html')

def custregdetails(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['username']
        email = request.POST['email']
        address = request.POST['address']
        pwd = request.POST['password']
        cpwd = request.POST['confirm_password']
        phone = request.POST['phone']
        cimage = request.FILES['image'] 
        if pwd == cpwd:
            if User.objects.filter(username=uname).exists():
                messages.info(request, "Username already exists")
                return redirect('customerreg')
            else:
                user = User.objects.create_user(first_name=fname, last_name=lname, username=uname, password=pwd, email=email)
                user.save()
                u = User.objects.get(id=user.id)
                reg = Customer(phone=phone, address=address,image=cimage, user=u)
                reg.save()
                return redirect('/')
        else:
            messages.info(request, "Passwords do not match")
            return render(request, 'customerreg.html')  

    return render(request,'customerreg.html')

@login_required(login_url='guest')
def adminhome(request):
    return render(request,'adminhome.html')

def addcat(request):
    return render(request,'addcat.html')


def catdetails(request):
    if request.method == "POST":
        c_name = request.POST['categoryName']
        if Category.objects.filter(categoryname=c_name).exists():
            messages.error(request, 'Category already exists!')
            return redirect('addcat')
        else:
            cat = Category(categoryname=c_name)
            cat.save()
            messages.success(request, 'New category added successfully!')
            return redirect('viewcat')
    
    return render(request, 'addcat.html')


def addpro(request):
    cat=Category.objects.all()
    return render(request,'addpro.html',{'cat1':cat})


def prodetails(request):
    if request.method == "POST":
        p_name = request.POST['name']
        p_des = request.POST['description']
        p_pr = request.POST['price']
        p_qty = request.POST['quantity']
        p_img = request.FILES['image']  
        p_cat = request.POST['category']
        
        if Product.objects.filter(productname=p_name).exists():
            messages.error(request, 'Product already exists!')
            return redirect('addpro')      
        productdetails = Category.objects.get(id=p_cat)   
        pro = Product(productname=p_name,description=p_des,price=p_pr,quantity=p_qty,image=p_img,category=productdetails)
        pro.save() 
        messages.success(request, 'New product added successfully!')
        return redirect('viewproduct')
    
    return render(request, 'addpro.html') 


def viewproduct(request):
    pro=Product.objects.all()
    return render(request,'viewproduct.html',{'product':pro})

def editproduct(request, pk):
    product=Product.objects.get(id=pk)
    category = Category.objects.all()
    return render(request, 'editproduct.html', {'category': category, 'product': product})

def editprodetails(request, pk):
    product=Product.objects.get(id=pk)
    if request.method == 'POST':
        product.productname = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.category = Category.objects.get(id=request.POST.get('category'))
        
        new_image = request.FILES.get('image')
        if new_image:
            if product.image:
                os.remove(product.image.path)
            product.image = new_image

        product.save()
        return redirect('viewproduct') 

    return render(request, 'editproduct.html', {'product': product})


def viewcat(request):
    cat=Category.objects.all()
    return render(request,'viewcat.html',{'category':cat})

def editcat(request, pk):
    category=Category.objects.get(id=pk)
    return render(request, 'editcat.html', {'category': category})

def editcatdetails(request, pk):
    category=Category.objects.get(id=pk)
    if request.method =='POST':
        category.categoryname = request.POST.get('categoryName')
        category.save()
        return redirect('viewcat')  
    return render(request, 'editcat.html', {'category': category})


def manageuser(request):
    user=Customer.objects.all()
    return render(request,'manageuser.html',{'users':user})


@login_required(login_url='guest')
def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        
        if cart:
            cart_item_count = CartItem.objects.filter(cart=cart).values('product').distinct().count()
        else:
            cart_item_count = 0
    else:
        cart_item_count = 0

    return render(request, 'home.html', {'categories': categories,'products': products,'cart_item_count': cart_item_count })


    


def category_product(request, category_id):
    category = Category.objects.filter(id=category_id).first()  
    if category is None:
        messages.error(request, "Category not found.")
        return redirect('home')  

    products = Product.objects.filter(category=category) 
    categories = Category.objects.all() 

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        
        if cart:
            cart_item_count = CartItem.objects.filter(cart=cart).values('product').distinct().count()
        else:
            cart_item_count = 0
    else:
        cart_item_count = 0
 
    return render(request, 'category_product.html', {'category': category, 'products': products, 'categories': categories,'cart_item_count': cart_item_count  })



def add_to_cart(request, id):
    product =Product.objects.get(id=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:  
        cart_item.quantity += 1  
        cart_item.save()  
    else:
        cart_item.quantity = 1  
        cart_item.save()  
    return redirect('view_cart')

def view_cart(request):
    categories = Category.objects.all()
    cart = Cart.objects.filter(user=request.user).first()  
    items = cart.items.all() if cart else []  
    
    total_price = sum(item.total_price for item in items) 

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        
        if cart:
            cart_item_count = CartItem.objects.filter(cart=cart).values('product').distinct().count()
        else:
            cart_item_count = 0
    else:
        cart_item_count = 0 

    return render(request, 'cart.html', {'categories': categories,'cart_items': items, 'total_price': total_price,'cart_item_count': cart_item_count })


def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()  
    return redirect('view_cart')

def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity', 1))

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity = max(1, cart_item.quantity - 1) 
        
        cart_item.save() 

    return redirect('view_cart')


def edituser(request):
    categories = Category.objects.all()
    cu = Customer.objects.get(user=request.user)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        
        if cart:
            cart_item_count = CartItem.objects.filter(cart=cart).values('product').distinct().count()
        else:
            cart_item_count = 0
    else:
        cart_item_count = 0 
    return render(request, 'edituser.html', {"cust": cu,'cart_item_count': cart_item_count,'categories': categories })

def update_user(request, pk):
    cust = Customer.objects.get( id=pk)
    user = cust.user 
    if request.method == 'POST':
      
        new_first_name = request.POST.get('fname')
        new_last_name = request.POST.get('lname')
        new_username = request.POST.get('uname')
        new_address = request.POST.get('address')
        new_email = request.POST.get('email')
        new_phone = request.POST.get('phone')
        new_img = request.FILES.get('image')

       
        if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
            messages.error(request, "This username is already taken. Please choose another one.")
            return redirect('edituser')

        if User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
            messages.error(request, "This email is already in use.")
            return redirect('edituser')

        if len(new_phone) != 10 or not new_phone.isdigit() or Customer.objects.filter(phone=new_phone).exclude(pk=cust.pk).exists():
            messages.error(request, "Phone number must be exactly 10 digits and unique.")
            return redirect('edituser')

      
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.username = new_username
        user.email = new_email
        user.save()

        cust.address = new_address
        cust.phone = new_phone

        if new_img:
            if cust.image:
                os.remove(cust.image.path)  
            cust.image = new_img

        cust.save()
        messages.success(request, "User information updated successfully!")
        return redirect('card')

    return render(request, 'edituser.html', {'cu': cust})

def about(request):
    return render(request,'about.html')



def deleteproduct(request,pk):
    po=Product.objects.get(id=pk)
    po.delete()
    return redirect('viewproduct')

def deletecat(request,pk):
    ca=Category.objects.get(id=pk)
    ca.delete()
    return redirect('viewcat')

def deleteuser(request,pk):
    u=Customer.objects.get(id=pk)
    u.delete()
    return redirect('manageuser')

def card(request): 
    categories = Category.objects.all()
    cu=Customer.objects.get(user=request.user)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        
        if cart:
            cart_item_count = CartItem.objects.filter(cart=cart).values('product').distinct().count()
        else:
            cart_item_count = 0
    else:
        cart_item_count = 0 
    return render(request,'card.html',{'cus':cu,'cart_item_count': cart_item_count,'categories':categories })

@login_required(login_url='guest')
def logout(request):
    auth.logout(request)
    return render(request,'guest.html')



