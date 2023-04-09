from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Inbound, Outbound

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
        return render(request, 'erp/product_create.html')

    elif request.method == 'POST':
        code = request.POST.get('code', '')
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        price = request.POST.get('price', '')
        size = request.POST.get('size', '')

        if code == '' or name == '' or price == '' or size == '':
            return render(request, 'erp/product_create.html', {'error': '내용을 입력하세요'})
        exist_code = Product.objects.filter(code=code)
        if exist_code:
            return render(request, 'erp/product_create.html', {'error': '동일한 상품 코드가 존재합니다'})
        Product.objects.create(
            code=code, name=name, description=description, price=price, size=size)

    return redirect('/product-list')


@login_required
# @transaction.atomic
def inbound_create(request):
    # 상품 입고 view
    # 입고 기록 생성
    if request.method == 'GET':
        all_products = Product.objects.all().order_by('code')
        return render(request, 'erp/inbound_create.html', {'products': all_products})

    elif request.method == 'POST':
        code = request.POST.get('code', '')
        quantity = request.POST.get('quantity', '')

        if code == '' or quantity == '':
            return render(request, 'erp/inbound_create.html', {'error': '내용을 입력하세요'})
        elif not type(quantity) == 'number':
            return render(request, 'erp/inbound_create.html', {'error': '수량에는 숫자만 입력해주세요'})
        else:
            product = Product.objects.get(code=request.POST.get('code'))

        Inbound.objects.create(product=product, quantity=quantity)

    # 입고 수량 조정
    product.quantity += int(quantity)
    product.save()

    return redirect('/product-list')


@login_required
# @transaction.atomic
def outbound_create(request):
    # 상품 출고 view
    # 출고 기록 생성
    if request.method == 'GET':
        all_products = Product.objects.all().order_by('code')
        return render(request, 'erp/outbound.html', {'products': all_products})

    elif request.method == 'POST':
        code = request.POST.get('code', '')
        quantity = request.POST.get('quantity', '')

        if code == '' or quantity == '':
            return render(request, 'erp/outbound.html', {'error': '내용을 입력하세요'})
        elif not type(quantity) == 'number':
            return render(request, 'erp/outbound.html', {'error': '수량에는 숫자만 입력해주세요'})
        else:
            product = Product.objects.get(code=request.POST.get('code'))

        Outbound.objects.create(product=product, quantity=quantity)

    # 출고 수량 조정
    out_quantity = product.quantity - int(quantity)
    if out_quantity >= 0:
        product.quantity = out_quantity
        product.save()
    else:
        return render(request, 'erp/outbound.html', {'error': f'재고가 부족합니다. 현재 수량: {product.quantity}개'})

    return redirect('/product-list')
