from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Inbound
from django.db import transaction

# Create your views here.


def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/product-list')
    else:
        return redirect('/login')


@login_required
def product_list(request):
    # 등록 된 상품의 리스트를 볼 수 있는 view
    if request.method == 'GET':
        all_products = Product.objects.all().order_by('code')
        return render(request, 'erp/product_list.html', {'products': all_products})


@login_required
def product_create(request):
    # 상품 등록 view
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'erp/product_create.html')
        else:
            return render(request, 'accounts/signup.html')
    elif request.method == 'POST':
        code = request.POST.get('code', '')
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        price = request.POST.get('price', '')
        size = request.POST.get('size', '')

        if code == '' or name == '' or price == '' or size == '---------':
            return render(request, 'erp/product_create.html', {'error': '내용을 채우십시오.'})

        Product.objects.create(
            code=code, name=name, description=description, price=price, size=size)

    return redirect('/product-list')


@login_required
# @transaction.atomic
def inbound_create(request):
    # 상품 입고 view
    # 입고 기록 생성
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'erp/inbound_create.html')
        else:
            return render(request, 'accounts/signup.html')
    elif request.method == 'POST':
        product = Product.objects.get(code=request.POST.get('code'))
        quantity = request.POST.get('quantity', '')
        print(quantity)
        if quantity == '':
            return render(request, 'erp/inbound_create.html', {'error': '수량은 필수값입니다.'})

        Inbound.objects.create(product=product, quantity=quantity)

    # 입고 수량 조정
    product.quantity += int(quantity)
    product.save()
    print(product.quantity)

    return redirect('/product-list')
