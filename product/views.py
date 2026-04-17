from contextlib import nullcontext

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.shortcuts import get_object_or_404, redirect


from product.models import Product, SUPPLEMENT_TYPES, CartItem, Order, OrderItem
from users.models import User
from users.services import create_anonymous_user


def get_current_user(request):
    user_data = request.session.get('user')
    if not user_data:
        user = create_anonymous_user(request)
        return user
    return User.objects.get(pk=user_data['pk'])


def home(request):
    products = Product.objects.order_by('?')
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products':products, 'categories': SUPPLEMENT_TYPES}
    return render(request,'product/home.html',context=context)


def home_with_category(request, category):
    categories = dict(SUPPLEMENT_TYPES)
    products = Product.objects.filter(category=categories[category]).order_by('?')
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products': products, 'categories': SUPPLEMENT_TYPES}
    return render(request,'product/home.html',context=context)


def detail(request, pk):
    product = Product.objects.get(pk=pk)
    is_admin = False
    if user_session := request.session.get('user'):
        if user_session.get('role') == 'A':
            is_admin = True
    context = {'product': product, 'categories': SUPPLEMENT_TYPES, 'is_admin': is_admin}
    return render(request,'product/detail.html', context=context)

def create_product(request):
    if request.method == 'POST':
        producti = Product.objects.create(
            image = request.FILES['image'],
            name = request.POST['name'],
            category = request.POST['category'],
            brand = request.POST['brand'],
            description = request.POST['description'],
            price = request.POST['price'],
            stock = request.POST['stock'],
            weight = request.POST['weight'],
            flavor = request.POST['flavor'],

        )
        return HttpResponseRedirect(reverse("detail", args=(producti.pk,)))
    return render(request, 'product/create_product.html', {'producti': Product.objects.all()})

def update_product(request, pk):
    producti = Product.objects.get(pk=pk)
    if request.method == 'POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        weight = request.POST.get('weight')
        flavor = request.POST.get('flavor')
        discount_percent = request.POST.get('discount_percent')

        if not discount_percent:
            discount_percent = 0

        if not stock:
            stock = 0

        producti.name = name
        producti.category = category
        producti.brand = brand
        producti.description = description
        producti.price = price
        producti.stock = stock
        producti.weight = weight
        producti.flavor = flavor
        producti.discount_percent = discount_percent



        if image:
            producti.image = image

        producti.save()
        return redirect('detail', pk=producti.pk)
    return render(request, 'product/update_product.html', {'producti': producti})


def delete_product(request, pk):
    producti = get_object_or_404(Product, pk=pk)
    producti.delete()
    return redirect("home")

def login(request):
    return render(request, 'product/login.html')

def signup(request):
    return render(request, 'product/signup.html')

def discounts(request):
    products = Product.objects.filter(discount_percent__gt=0).order_by('?')
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products': products, 'categories': SUPPLEMENT_TYPES}
    return render(request, 'product/discounts.html', context=context)

def contact(request):
    products = Product.objects.order_by('?')
    context = {'products': products, 'categories': SUPPLEMENT_TYPES}
    return render(request, 'product/contact.html', context=context)


def goals(request):
    products = Product.objects.order_by('?')
    context = {'products': products, 'categories': SUPPLEMENT_TYPES}
    return render(request, 'product/goals.html', context=context)


def add_to_cart(request, pk):
    user = get_current_user(request)
    if not user:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
        return redirect('login')
    product = get_object_or_404(Product, pk=pk)


    item, created = CartItem.objects.get_or_create(
        user=user,
        product=product
    )
    if not created:
        item.quantity += 1
        item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect(request.META.get('HTTP_REFERER', 'home'))


def cart_view(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    items = CartItem.objects.filter(user=user)


    cart_items = []
    total = 0
    for item in items:
        product = item.product

        if product.discount_percent:
            price = product.price - (product.price * product.discount_percent / 100)
        else:
            price = product.price
        total += price * item.quantity


        cart_items.append({
            'item': item,
            'price': price,
            'has_discount': bool(product.discount_percent),
            'original_price': product.price
        })

    return render(
        request,
        'product/cart.html',
        {
            'items': cart_items,
            'total': total,
            'categories': SUPPLEMENT_TYPES,
        }
    )

def remove_from_cart(request, pk):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    item = get_object_or_404(CartItem, pk=pk, user=user)
    item.delete()
    return redirect('cart')




def increase_quantity(request, pk):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    item = get_object_or_404(CartItem, pk=pk, user=user)
    item.quantity += 1
    item.save()
    return redirect('cart')


def decrease_quantity(request, pk):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    item = get_object_or_404(CartItem, pk=pk, user=user)
    if item.quantity > 0:
        item.quantity -= 1
        item.save()
    else:

        item.delete()
    return redirect('cart')

from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import F

def checkout(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    items_qs = CartItem.objects.filter(user=user)

    if request.method == "GET":
        cart_items = []
        total = 0

        for item in items_qs:
            product = item.product
            price = product.get_discount_price()
            total += price * item.quantity

            cart_items.append({
                'item': item,
                'price': price,
                'has_discount': bool(product.discount_percent),
                'original_price': product.price
            })

        return render(request, 'product/checkout.html', {
            'items': cart_items,
            'total': total
        })

    elif request.method == "POST":

        if not items_qs.exists():
            return redirect('cart')

        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        country = request.POST.get('country')
        city = request.POST.get('city')

        with transaction.atomic():
            total = 0

            order = Order.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                country=country,
                city=city,
                total=0
            )

            for item in items_qs:
                product = item.product
                price = product.get_discount_price()


                if product.stock < item.quantity:
                    return render(request, 'product/checkout.html', {
                        'items': items_qs,
                        'error': f"Nuk ka stock mjaftueshëm për {product.name}"
                    })


                product.stock = F('stock') - item.quantity
                product.save()
                product.refresh_from_db()

                total += price * item.quantity

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    price=price
                )

            order.total = total
            order.save()


            items_qs.delete()

        return redirect('success')


from django.db.models import Count

def admin_orders(request):
    orders = Order.objects.annotate(
        item_count=Count('items')
    ).filter(
        item_count__gt=0
    ).order_by('-created_at')

    return render(request, 'product/admin_orders.html', {'orders': orders})


def update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)
    if new_status in ['pending', 'shipped', 'delivered']:
        order.status = new_status
        order.save()

    return redirect('admin_orders')


def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('admin_orders')


def success(request):
    return render(request, 'product/success.html')






