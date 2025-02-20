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
    user_profile, created = UserProfile.objects.get_or_create(user=user)  # Ensure UserProfile exists

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        avatar = request.FILES.get("avatar")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        # Update first name and last name
        user.first_name = first_name
        user.last_name = last_name

        # Save avatar if uploaded
        if avatar:
            user_profile.avatar = avatar

        # Handle password change securely
        if password and password_confirm:
            if password == password_confirm:
                user.set_password(password)
                update_session_auth_hash(request, user)  # Keep session active after password change
                messages.success(request, "رمز عبور با موفقیت تغییر کرد.")
            else:
                messages.error(request, "رمز عبور و تکرار آن مطابقت ندارند.")
                return redirect("profile")  # Stop execution and redirect if passwords don't match

        user.save()
        user_profile.save()

        messages.success(request, "پروفایل با موفقیت به‌روزرسانی شد.")
        return redirect("profile")

    return render(request, "accounts/profile.html", {"user": user})


from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    if request.method == "POST":
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  # Ensure profile is created
            messages.success(request, "ثبت‌نام با موفقیت انجام شد! لطفاً وارد شوید.")
            return redirect("login")
        else:
            messages.error(request, "خطایی در ثبت‌نام وجود دارد. لطفاً فرم را بررسی کنید.")

    else:
        form = UserRegisterationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"].strip()
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, "ورود موفقیت‌آمیز بود!")
                return redirect("todo_list")  # Redirect after login
            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")

    else:
        form = UserLoginForm()

    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "شما با موفقیت خارج شدید.")
    return redirect("login")
