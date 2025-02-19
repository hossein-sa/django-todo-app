from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserRegisterationForm, UserLoginForm
from .models import UserProfile
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib import messages


@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        avatar = request.FILES.get("avatar")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        # ذخیره نام و نام خانوادگی
        user.first_name = first_name
        user.last_name = last_name

        # ذخیره آواتار اگر آپلود شده باشد
        if avatar:
            user.userprofile.avatar = avatar

        # تغییر پسورد اگر مقداردهی شده باشد
        if password and password_confirm:
            if password == password_confirm:
                user.set_password(password)  # تغییر پسورد
                update_session_auth_hash(request, user)  # حفظ سشن لاگین
                messages.success(request, "رمز عبور با موفقیت تغییر کرد.")
            else:
                messages.error(request, "رمز عبور و تکرار آن مطابقت ندارند.")

        user.save()
        user.userprofile.save()

        messages.success(request, "پروفایل با موفقیت به‌روزرسانی شد.")
        return redirect("profile")  # ریدایرکت به صفحه پروفایل

    return render(request, "accounts/profile.html", {"user": user})

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