from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout
from .models import Category, Product, Sale, SaleItem, Customer
from django.utils.timezone import now
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from django.template.loader import render_to_string
from django.db.models import Sum, Count
import time
import uuid
from .models import POSSetting
from django.core.serializers import serialize
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
        form = UserRegistrationForm(request.POST, request.FILES)  # Use request.FILES to handle file uploads

        if form.is_valid():
            username = request.POST.get('username')
            
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"status": "error", "message": "Username already exists, please choose a different one."})
            
            password = request.POST.get('password')
            role = request.POST.get('role')
            image = request.FILES.get('image')
            
            # Create the user and set the hashed password
            user = User(username=username, role=role, image=image)
            user.set_password(password)  # Hash the password
            user.save()  # Save the user to the database

            return JsonResponse({'status': 'success', 'message': 'Registration successful!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Registration failed, form data is not valid!'})

    else:
        form = UserRegistrationForm()  # Display the form on GET request

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
            print(f"Product ID: {product.id}, Product Name: {product.name}, Category: {product.category}, quanity: {product.quantity_in_stock}, dicount: {product.discount} status: {product.status}")
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
    if request.method == "POST":
        # Handle file upload
        image = request.FILES.get('image')
        name = request.POST.get('product_name')
        sku = request.POST.get('SKU')
        category_name = request.POST.get('category')
        quantity_in_stock = request.POST.get('qty')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
         # Get the Category instance based on the ID
        if image:
            final_image = image
        else:
            return JsonResponse({"status": "error", "message": "Please enter an image for " + name})
        category = Category.objects.get(name=category_name)
        if Product.objects.filter(sku=sku):
            return JsonResponse({"status": 'error', "message": "SKU is already exits please choose different one."})
        if Product.objects.filter(name =name):
            return JsonResponse({'status': "error", "message": f"{name} is already exits please choose different one."})
        else:
            product = Product.objects.create(name=name, image=final_image, sku=sku, category=category, quantity_in_stock=quantity_in_stock, price=price, discount=discount)
            return JsonResponse({"status": "success", "message": "Product was added."})
    else:
        return JsonResponse({"status": "success", "message": "Opss! something went wrong."})
        

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
        category_name= request.POST.get('category')
        quantity_in_stock = request.POST.get('qty')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        
        # Update fields
        product.name = name
        product.sku = sku
        product.quantity_in_stock = quantity_in_stock
        product.price = price
        product.discount = discount

        # Update category if exists
        if category_name:
            try:
                category = Category.objects.get(name=category_name)
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

def search_products(request):
    category_name = request.GET.get('category_name', '')  # Get category name from request
    search_text = request.GET.get('search_text', '')

    products = Product.objects.all()

    if category_name:
        products = products.filter(category__name__iexact=category_name)  # Case-insensitive match

    if search_text:
        products = products.filter(name__icontains=search_text)

    product_list = []
    for product in products:
        image_url = product.image.url if product.image else ''
        # Debugging: Print image URL for each product
        print(f"Product ID: {product.id}, Image URL: {image_url}")
        
        product_list.append({
            'id': product.id,
            'name': product.name,
            'sku': product.sku,
            'quantity_in_stock': product.quantity_in_stock,
            'price': product.price,
            'discount': product.discount,
            'status': product.status,
            'category_id': product.category.id,
            'category_name': product.category.name,
            'image': image_url
        })

    # Additional debugging: Print the image URLs in the product list
    for product in product_list:
        print(f"Product ID: {product['id']}, Image URL: {product['image']}")

    return JsonResponse({'products': product_list})


def show_product_by_category(request):
    category_name = request.GET.get('category')
    search_text = request.GET.get('search_text')
    products = Product.objects.all()
    if category_name:
        category = Category.objects.get(name = category_name)
        products = products.filter(category = category)
    if search_text:
        products = products.filter(name__icontains = search_text)

    products_List =[]
    for product in products:
        products_List.append({
            'id': product.id,
            'name': product.name,
            'sku': product.sku,
            'quantity_in_stock': product.quantity_in_stock,
            'price': product.price,
            'discount': product.discount,
            'status': product.status,
            'category_id': product.category.id,
            'category_name': product.category.name,
            'image_url': product.image.url if product.image else ''
        })
    return JsonResponse({'productLists': products_List})

def pos_view(request):
    product = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'pos_app/pos.html', {"products": product, "categories" : categories})

@csrf_exempt
def generate_receipt(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received Data:", data)  # Debugging

            # Validate required fields
            if not all(key in data for key in ['cashier', 'orderItems', 'totalAmount', 'paymentMethod']):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Get cashier
            cashier = User.objects.filter(username=data.get('cashier')).first()
            if not cashier:
                return JsonResponse({'error': 'Cashier not found'}, status=400)

            # Get or create customer
            customer_name = data.get('customer')
            customer = Customer.objects.create(name=customer_name)

           

# Generate a unique invoice number
            invoice_no = f"INV-{uuid.uuid4().hex[:8]}"  # You can customize the length

            # Create Sale record
            sale = Sale.objects.create(
                invoice_no=invoice_no,
                cashier=cashier,
                customer=customer,
                total_amount=data.get('totalAmount'),
                discount=data.get('discount', 0),
                payment_method=data.get('paymentMethod'),
            )

            # Save SaleItem records
            for item in data.get('orderItems', []):
                product = Product.objects.filter(name=item['name']).first()
                if product:
                    SaleItem.objects.create(
                        sale=sale,
                        product=product,
                        quantity=item['quantity'],
                        price=item['price'],
                        subtotal=float(item['quantity']) * float(item['price']),
                    )

                    # Reduce stock
                    product.quantity_in_stock -= int(item['quantity'])
                    product.save()
            setting = POSSetting.objects.first()
            address = setting.address
            name = setting.name
            # Render receipt HTML
            receipt_html = render_to_string('receipts/receipt_template.html', {
                'date': data.get('date'),
                'invoice_no': invoice_no,
                'cashier': data.get('cashier'),
                'customer': customer_name,
                'orderItems': data.get('orderItems'),
                'paymentMethod': data.get('paymentMethod'),
                'subtotal': data.get('subtotal'),
                'discount': data.get('discount'),
                'totalAmount': data.get('totalAmount'),
                'name': name,
                'address': address
            })

            # Return JSON response with HTML
            return JsonResponse({'html': receipt_html})

        except Exception as e:
            print("Error:", str(e))  # Debugging
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
def dasboard_view(request):
    
    return render(request, 'pos_app/dasboard.html')

from django.utils import timezone

def total_sale_counts(request):
    # Get the current date and time in local time
    now = timezone.localtime(timezone.now())

    # Start of today (midnight in the local time zone)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Start of the next day (midnight of tomorrow in the local time zone)
    end_of_day = start_of_day + timezone.timedelta(days=1)


    # Filter sales that occurred between the start and end of today
    sales_today = Sale.objects.filter(created_at__range=[start_of_day, end_of_day])
    sale_counts = sales_today.count()

    # Return the total count as a JSON response
    return JsonResponse({'sale_counts': sale_counts})

def total_orders(request):
    total_orders = Sale.objects.count()
    print('Total orders (all-time):', total_orders)
    return JsonResponse({'total_orders': total_orders})

def total_customers(request):
    total_customers = Customer.objects.all().count()
    print('Total customers: ', total_customers)
    customers = Customer.objects.all()
    for customer in customers:
        print('Customer id',customer.id ,'Customer name: ', customer.name)
    return JsonResponse({'total_customers': total_customers})
def total_product_in_stock(request):
    total_product = Product.objects.all().count()
    return JsonResponse({'total_product': total_product})

def top_selling_products(request):
    # Aggregate total quantity sold for each product
    top_products = (
        SaleItem.objects
        .values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5]
    )

    # Print for debugging
    print("Top selling products:", list(top_products))

    return JsonResponse({'top_products': list(top_products)})

def low_product(request):
    # Get all products where quantity_in_stock is less than or equal to 5
    low_stock_products = Product.objects.filter(quantity_in_stock__lte=5)
    
    # Prepare the data to send as JSON response
    products_data = list(low_stock_products.values('name','quantity_in_stock'))
    
    # Return the data as JSON
    return JsonResponse({'low_stock_products': products_data})

def recent_transactions(request):
    # Get the most recent transactions (e.g., last 5)
    recent_sales = Sale.objects.all().order_by('-created_at')[:5]
    

    for sale in recent_sales:
        print(sale.invoice_no, sale.created_at, sale.total_amount, sale.cashier.username)
    # Prepare the data to send as JSON response
    sales_data = []
    for sale in recent_sales:
        # Get product names for each sale item
        products = SaleItem.objects.filter(sale=sale).values('product__name')
        product_names = [product['product__name'] for product in products if product['product__name']]  # Exclude None values
        
        # Check if the cashier's name is set and log it if not
        cashier_name = sale.cashier.username if sale.cashier and sale.cashier.username else 'Unknown'

        # Gather the required fields for the response
        sales_data.append({
            'date': sale.created_at.strftime('%Y-%m-%d'),  # Format the date
            'order_id': sale.invoice_no,
            'products': ', '.join(product_names) if product_names else 'No products',  # Avoid empty string if no products
            'total': sale.total_amount,
            'cashier': cashier_name,
        })
    
    # Return the data as JSON
    return JsonResponse({'recent_sales': sales_data})

def report_view(request):
    return render(request, 'pos_app/report.html')

def sales_summary(request):
    # Group sales by date and cashier's username
    sales_data = (
        Sale.objects.values('created_at__date', 'cashier__username')
        .annotate(
            total_orders=Count('id'),
            total_revenue=Sum('total_amount')
        )
        .order_by('-created_at__date')
    )

    summary = []
    for sale in sales_data:
        summary.append({
            'date': sale['created_at__date'].strftime('%Y-%m-%d') if hasattr(sale['created_at__date'], 'strftime') else sale['created_at__date'],
            'orders': sale['total_orders'],
            'revenue': float(sale['total_revenue']) if sale['total_revenue'] is not None else 0.0,
            'cashier': sale['cashier__username'] or 'Unknown',
        })
    settings = POSSetting.objects.first()
    return JsonResponse({'sales_summary': summary,
    'company': {
        'name': settings.name,
        'address': settings.address,
        'logo': settings.logo.url if settings.logo else None  # Make sure to handle the logo URL properly
    }})

def fetch_products(request):
    products = Product.objects.all().values("id", "name", "sku", "quantity_in_stock", "price", "discount", "status", "category__id", "category__name", "image")
    
    product_list = []
    for product in products:
        product_list.append({
            "id": product["id"],
            "name": product["name"],
            "sku": product["sku"],
            "quantity_in_stock": product["quantity_in_stock"],
            "price": product["price"],
            "discount": product["discount"],
            "status": "Out of Stock" if product["quantity_in_stock"] == 0 else product["status"],
            "category_id": product["category__id"],
            "category_name": product["category__name"],
            "image": product["image"] if product["image"] else None,
        })
    # Count low-stock and out-of-stock products
    low_stock_count = products.filter(quantity_in_stock__lte=5).count()
    # Calculate total notification count
    final_count = low_stock_count 
    return JsonResponse({"products": product_list, 'notif_count': final_count})

def fetch_low_stock_products(request):
    products = Product.objects.filter(quantity_in_stock__lte=5)
    low_stock_products = [{'name': product.name, 'quantity': product.quantity_in_stock} for product in products]
    return JsonResponse({'low_stock_products': low_stock_products})

def setting_view(request):
    settings, created = POSSetting.objects.get_or_create(id=1)  # Ensure only one setting exists
    context = {
        'company': settings
    }
    return render (request, 'pos_app/setting.html', context)

def company_settings(request):
    settings, created = POSSetting.objects.get_or_create(id=1)  # Ensures only one setting exists

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        address = request.POST.get("address", "").strip()
        logo = request.FILES.get("logo")

        if name:
            settings.name = name
        if address:
            settings.address = address
        if logo:
            settings.logo = logo  # Assuming your model has an ImageField for the logo

        settings.save()

        return JsonResponse({"success": True, "message": "Company information updated!"})
    

    settings, created = POSSetting.objects.get_or_create(id=1)  # Ensure only one setting exists
    context = {
        'company': settings
    }
    return JsonResponse({context})
def com_name_and_addr(request):
    setting = POSSetting.objects.first()
    return JsonResponse({
        'name': setting.name,
        'address': setting.address
    })
def setting_cashier(request):
    return render(request, 'pos_app/setting_cashier.html')
def setting_general(request):
    settings, created = POSSetting.objects.get_or_create(id=1)  # Ensure only one setting exists
    context = {
        'company': settings
    }
    return render(request, 'pos_app/setting_general.html', context)
def setting_cashier_all(request):
    cashiers = User.objects.filter(role='Cashier')  # Ensure role is lowercase
    cashiers_data = []

    for cashier in cashiers:
        cashiers_data.append({
            'id': cashier.id,
            'username': cashier.username,
            'role': cashier.role,
            'name': cashier.name,
            'image': cashier.image.url if cashier.image else None  # Full URL
        })

    return JsonResponse({'cashiers': cashiers_data})

def update_user(request):
    if request.method == "POST":
            id = request.POST.get('id')
            name = request.POST.get('name')
            role = request.POST.get('role')
            image = request.FILES.get('image')

            user = User.objects.get(id=id)
            user.name = name
            user.role = role
            if image:
                user.image = image
            user.save()
            return JsonResponse({
                'meesage' : 'User was updated'
            })
def delete_user(request):
    if request.method == "POST":
        id = request.POST.get('id')
        user = User.objects.get(id=id)
        if id:
            user.delete()
            return JsonResponse({'message': 'User was removed.'})
    else:
        return JsonResponse({'message': 'Invalid request'})