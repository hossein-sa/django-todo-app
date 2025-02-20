from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserRegisterationForm, UserLoginForm
from .models import UserProfile
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from PIL import Image, UnidentifiedImageError

@login_required
def profile_view(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)  # ایجاد پروفایل در صورت نبود آن

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        avatar = request.FILES.get("avatar")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        # به‌روزرسانی نام و نام خانوادگی
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        # بررسی و ذخیره‌ی تصویر آواتار در صورت آپلود
        if avatar:
            try:
                img = Image.open(avatar)
                if img.format.lower() not in ['jpeg', 'png']:
                    messages.error(request, "❌ فرمت فایل نامعتبر است. لطفاً یک تصویر با فرمت jpg، jpeg یا png بارگذاری کنید.")
                    return redirect("profile")
            except UnidentifiedImageError:
                messages.error(request, "❌ فایل تصویر معتبر نیست. لطفاً یک تصویر معتبر بارگذاری کنید.")
                return redirect("profile")
            user_profile.avatar = avatar

        # بررسی و تغییر رمز عبور
        if password and password_confirm:
            if password == password_confirm:
                user.set_password(password)
                update_session_auth_hash(request, user)  # حفظ لاگین کاربر بعد از تغییر رمز
                messages.success(request, "✅ رمز عبور شما با موفقیت تغییر کرد.")
            else:
                messages.error(request, "❌ رمزهای وارد شده با یکدیگر مطابقت ندارند.")
                return redirect("profile")  # در صورت خطا، اجرا متوقف شده و کاربر به صفحه پروفایل برمی‌گردد.

        # ذخیره تغییرات
        user.save()
        user_profile.save()

        messages.success(request, "✅ پروفایل شما با موفقیت به‌روزرسانی شد.")
        return redirect("profile")

    return render(request, "accounts/profile.html", {"user": user})


def register_view(request):
    if request.method == "POST":
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  # ایجاد پروفایل برای کاربر جدید
            messages.success(request, "✅ ثبت‌نام شما با موفقیت انجام شد! لطفاً وارد حساب کاربری خود شوید.")
            return redirect("login")
        else:
            messages.error(request, "❌ مشکلی در ثبت‌نام وجود دارد. لطفاً اطلاعات خود را بررسی کنید.")

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
                messages.success(request, "✅ ورود شما موفقیت‌آمیز بود! خوش آمدید 😊")
                return redirect("todo_list")  # هدایت به صفحه لیست وظایف پس از ورود
            else:
                messages.error(request, "❌ نام کاربری یا رمز عبور اشتباه است. لطفاً دوباره تلاش کنید.")

    else:
        form = UserLoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "ℹ️ شما با موفقیت از حساب خود خارج شدید. به امید دیدار دوباره! 👋")
    return redirect("login")
