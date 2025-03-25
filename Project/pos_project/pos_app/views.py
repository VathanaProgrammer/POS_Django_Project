from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout
from .models import Category, Product
# Create your views here.
def home(request):
    users = User.objects.all()
    for user in users:
        print(f"Username: {user.username}, Password: {user.password}, role: {user.role}")
    return render(request, 'pos_app/base.html')
def register_form(request):
    return render (request, 'pos_app/test_register.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        print(request.POST, request.FILES)  # Check the POST data for debugging
        
        if form.is_valid():
            username = form.cleaned_data['username']
            
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"status": "error", "message": "Username already exists, please choose a different one."})
            
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            image = form.cleaned_data['image']

            # Create the user and set the hashed password
            user = User(username=username, role=role, image=image)
            user.set_password(password)  # Hash the password
            user.save()  # Save the user to the database

            return JsonResponse({'status': 'success', 'message': 'Register success!'})
        else:
            print(form.errors)
            return JsonResponse({'status': 'error', 'message': 'Registration failed, form data is not valid!'})

    # If it's a GET request, instantiate the form
    else:
        form = UserRegistrationForm()

    return render(request, 'pos_app/test_register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid username or password!'}, status=400)

    return render(request, 'pos_app/login_form.html')
def login_form(request):
    return render(request, 'pos_app/login.html')

def logout_user(request):
    logout(request)  # This will destroy the session
    return JsonResponse({'message': 'Logout sucess!'})
def inventory_view(request):
    categories = Category.objects.all()
    for category in categories:
        print(f'Category name: {category.name}, Category ID: {category.id}')
    products = Product.objects.all()
    if not products.exists():  # Check if no products exist
        print('Product is empty.')
    else:
        for product in products:
            print(f"Product ID: {product.id}, Product Name: {product.name}, Category: {product.category}, quanity: {product.quantity_in_stock} status: {product.status}")
    low_stock_quantity = Product.objects.filter(quantity_in_stock__lte = 5)
    if not low_stock_quantity.exists():
        print('No product has low quantity')
    else:
        for low_stock in low_stock_quantity:
            print(f"low stock product : {low_stock.name}")
    return render(request, 'pos_app/inventory.html', {
        'categories': categories,
        'products': products,
        'low_stock_quantity' : low_stock_quantity
        })


def register_category(request):
    if request.method == 'POST':
        name = request.POST.get('category_name')
        if name:
            # Save new category
           if Category.objects.filter(name=name).exists():
            return JsonResponse({'status': 'error', 'message': 'Category already exists!'})
           else:
            Category.objects.create(name=name)
            return JsonResponse({'status': 'success', 'message': 'Category was added!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Name is required'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def add_product(request):
    if request.method == "POST" and request.FILES.get('image'):
        # Handle file upload
        image = request.FILES['image']
        name = request.POST.get('product_name')
        sku = request.POST.get('SKU')
        category_id = request.POST.get('category')
        quantity_in_stock = request.POST.get('qty')
        price = request.POST.get('price')
         # Get the Category instance based on the ID
        category = Category.objects.get(id=category_id)
        if Product.objects.filter(name =name):
            return JsonResponse({'status': "error", "message": f"{name} is already exits please choose different one."})
            print(f"add product name: {name}, category: {category}")
        else:
            product = Product.objects.create(name=name, image=image, sku=sku, category=category, quantity_in_stock=quantity_in_stock, price=price)
            return JsonResponse({"status": "success", "message": "Product was added."})
    else:
        return JsonResponse({"status": "success", "message": "Opss! something went wrong."})
        
from django.http import JsonResponse
from .models import Product, Category

def update_product(request):
    if request.method == "POST":
        try:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found.'})
        
        # Get updated data
        name = request.POST.get('product_name')
        sku = request.POST.get('SKU')
        category_id = request.POST.get('category')
        quantity_in_stock = request.POST.get('qty')
        price = request.POST.get('price')
        
        # Update fields
        product.name = name
        product.sku = sku
        product.quantity_in_stock = quantity_in_stock
        product.price = price

        # Update category if exists
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                product.category = category
            except Category.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid category selected.'})
        
        # Update image if new one uploaded
        if request.FILES.get('image'):
            image = request.FILES['image']
            product.image = image
        else:
            image = product.image
            print('Kepp the old image')
        product.save()

        return JsonResponse({'status': 'success', 'message': 'Product updated successfully.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
def delete_product(request):
    if request.method == "POST":
        try:
            product_id = request.POST.get('product_id')
            if Product.objects.filter(id = product_id):
                product = Product.objects.get(id = product_id)
                product.delete()
                return JsonResponse({'status': 'success'})
        except Product.DoesNotExist:
                return JsonResponse({'status': 'error', 'message' : 'Product not found'})
    else:
        return JsonResponse({'messge': 'Invalid method request'})

def update_category(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        category_name = request.POST.get('category_name')
        if Category.objects.filter(id = category_id):
            category = Category.objects.get(id = category_id)
            category.name = category_name
            category.save()
            return JsonResponse({'status': 'success', 'message': 'Category was updated.'})
        else:
            return JsonResponse({'status': 'error', 'message' : 'category not found!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
def delete_category(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        if Category.objects.filter(id = category_id):
            category = Category.objects.get(id = category_id)
            category.delete()
            return JsonResponse({'status': 'success', 'message': 'Category was deleted.'})
        else:
            return JsonResponse({'status': 'error', 'message':'category not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid method request'})
