from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout
# Create your views here.
def home(request):
    users = User.objects.all()
    for user in users:
        print(f"Username: {user.username}, Password: {user.password}, role: {user.role}")
    return render(request, 'pos_app/base.html')
def register_form(request):
    return render (request, 'pos_app/test_register.html')
from django.contrib import messages

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
            # Log the user in if authentication is successful
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful!'})
        else:
            # Return an error message if authentication fails
            return JsonResponse({'status': 'error', 'message': 'Invalid username or password!'}, status=400)

    return render(request, 'login_form.html')
def login_form(request):
    return render(request, 'pos_app/login.html')

def logout_user(request):
    logout(request)  # This will destroy the session
    return JsonResponse({'status': 'success', 'message': 'Logout successful'})
