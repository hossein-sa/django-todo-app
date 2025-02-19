from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserRegisterationForm, UserLoginForm
from .models import UserProfile
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        password = request.POST.get("password", "").strip()
        password_confirm = request.POST.get("password_confirm", "").strip()

        # ذخیره نام و نام خانوادگی
        if first_name:
            request.user.first_name = first_name
        if last_name:
            request.user.last_name = last_name
        request.user.save()

        # تغییر پسورد (اگر مقدار جدید وارد شده باشد)
        if password and password_confirm:
            if password == password_confirm:
                request.user.password = make_password(password)  # پسورد هش شود
                request.user.save()
                update_session_auth_hash(request, request.user)  # کاربر لاگ‌اوت نشود
            else:
                return render(request, "accounts/profile.html", {
                    "profile": profile,
                    "error": "رمز عبور و تکرار آن یکسان نیستند."
                })

        # ذخیره تصویر پروفایل
        if "avatar" in request.FILES:
            profile.avatar = request.FILES["avatar"]

        profile.save()
        return redirect("profile")

    return render(request, "accounts/profile.html", {"profile": profile})


def register_view(request):
    if request.method == "POST":
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user)
            return redirect("login")
    else:
        form = UserRegisterationForm()
        
        
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("todo_list")  # Redirect to home after login
            else:
                form.add_error(None, "Invalid username or password")

    else:
        form = UserLoginForm()

    return render(request, "accounts/login.html", {"form": form})  # Ensure this line is always executed
    
def logout_view(request):
    logout(request)
    return redirect("login")