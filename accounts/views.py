from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.http import HttpResponse
User = get_user_model() # Dynamically fetches your CustomUser model

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # Create user with custom model manager
        user = User.objects.create_user(email=email, password=password, phone_number=phone_number)
        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect('home')

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')

        # Authenticate using email as the username field
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            
            # Return direct HTTP responses instead of redirecting
            if user.is_superuser:
                print("user printed")
                return HttpResponse("<h1>Welcome Admin! This is the Superuser Response page.</h1>")
            else:
                return HttpResponse("<h1>Welcome! This is the Regular User Response page.</h1>")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged successfully out.")
    return redirect('login')

def home_view(request):
    return render(request, 'accounts/home.html')
