from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from app.models import ProductModel, UserModel
from app.utils import generate_code, send_register_email


def index(request):
    top_sales = ProductModel.objects.all().order_by('-id')[:4]
    new_arrivals = ProductModel.objects.all().order_by('-created_at')[:4]
    context = {
        'top_sales': top_sales,
        'new_arrivals': new_arrivals,
    }
    return render(request, 'index.html', context)


def mahsulotlar(request):
    products = ProductModel.objects.all()
    query = request.GET.get('search')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(category__icontains=query))

    sort_option = request.GET.get('sort')

    if sort_option == 'low price':
        products = products.order_by('-price')
    elif sort_option == 'high price':
        products = products.order_by('-price')
    elif sort_option == 'newest':
        products = products.order_by('-created_at')

    context = {
        'products': products,
    }
    return render(request, 'mahsulotlar.html', context)

def mahsulot_detail(product, pk):
    product = get_object_or_404(product,pk)

    context = {
        'product': product,
    }
    return render(product, 'mahsulot-detail.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = UserModel.objects.get(email=email)

        login(request, user)
        return redirect('index')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return render(request, 'register.html', {'errors': "Parollar mos kelmadi!"})

        if UserModel.objects.filter(name=name).exists():
            return render(request, 'register.html', {'errors': "Bu foydalanuvchi nomi allaqachon ro'yxatdan o'tgan!"})

        user = UserModel.objects.create(
            name=name,
            email=email,
            password=password
        )

        code = generate_code()
        request.session["verify_user_id"] = user.id
        request.session["verify_code"] = str(code)
        send_register_email(to_email=user.email, code=code)

        return redirect('confirm_password')

    return render(request, 'register.html')


@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = UserModel.objects.filter(email=email).last()

        if not user:
            return render(request, 'forgot-password.html', {'errors': "Bunday email ro'yxatdan o'tmagan!"})
        code = generate_code()
        request.session["verify_user_id"] = user.id
        request.session["verify_code"] = str(code)
        request.session["is_forgot"] = True
        send_register_email(to_email=user.email, code=code)

        return redirect('confirm_password')
    return render(request, 'forgot-password.html')


@csrf_exempt
def confirm_password(request):
    if request.method == 'POST':
        input_code = request.POST.get('code')
        session_code = request.session.get("verify_code")

        if input_code == session_code:
            user_id = request.session.get("verify_user_id")
            if user_id:
                user = UserModel.objects.get(id=user_id)
                user.is_active = True
                user.save()

            if request.session.get("is_forgot"):
                return redirect('reset_password')

            request.session.pop("verify_code", None)
            request.session.pop("verify_user_id", None)
            return redirect('login')
        else:
            return render(request, 'confirm-password.html', {'errors': "Tasdiqlash kodi noto'g'ri!"})

    return render(request, 'confirm-password.html')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return render(request, 'reset-password.html', {'errors': "Parollar mos kelmadi!"})

        user_id = request.session.get("verify_user_id")
        if user_id:
            user = UserModel.objects.get(id=user_id)
            user.password = password
            user.save()

            request.session.pop("verify_code", None)
            request.session.pop("verify_user_id", None)
            request.session.pop("is_forgot", None)

            return redirect('login')

    return render(request, 'reset-password.html')

def checkout(request):
    return render(request, 'checkout.html')

def savatcha(request):
    return render(request, 'savatcha.html')

def blog(request):
    return render(request, 'blog.html')

def blog_detail(request):
    return render(request, 'blog-detail.html')

def biz_haqimizda(request):
    return render(request, 'biz-haqimizda.html')

def aloqa(request):
    return render(request, 'aloqa.html')