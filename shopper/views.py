import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Coupon, Product, Category, Vendor, CartOrder, CartOrderItems, wishlist, Address, ProductImages, ProductReview
from taggit.models import Tag
from django.db.models import Count, Avg
from .forms import ReviewForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.contrib import messages
import stripe


def shop(request):
    products = Product.objects.filter(product_status='published').order_by('-date')
    categories = Category.objects.all()
    products_feautured = Product.objects.filter(product_status='published', feautured = True)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price!=None:
        products = products.filter(price__gte=min_price).filter(price__lte=max_price)

    context = {
        'products' : products,
        'categories' : categories,
        'products_feautured' : products_feautured
    }

    return render(request, 'shopper/index.html', context)

def category_product_list_category_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status='published', category=category)

    context = {
        'category' : category,
        'products' : products
    }

    return render(request, 'shopper/category-product-list.html', context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.filter(vid=vid)
    vendors = Vendor.objects.exclude(vid=vid)

    context = {
        'vendor' : vendor,
        'vendors' : vendors
    }

    return render(request, 'shopper/vendor_detail.html', context)

def product_detailed_view(request, pid):    
    product = Product.objects.get(pid=pid, product_status='published')
    related = Product.objects.filter(category=product.category, product_status='published').exclude(pid=pid)
    related1 = Product.objects.all
    products_feautured = Product.objects.filter(feautured=True)

    reviews = ProductReview.objects.filter(product=product).order_by('-date')

    avg_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    feautured_avg_rating = {}

    for r in products_feautured:
        feautured_avg_rating[r] = ProductReview.objects.filter(product=r).aggregate(rating=Avg('rating'))

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.instance.product = product
            form.instance.rating = request.POST.get('rating')
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect(request.get_full_path())
        else:
            print('not valid form')

    form = ReviewForm

    context = {
        'product' : product,
        'related' : related1,
        'reviews' : reviews,
        'avg_rating' : avg_rating,
        'numbers' : range(1,6),
        'form' : form,
        'products_feautured': products_feautured,
        'feautured_avg_rating': feautured_avg_rating,
    }
        


    return render(request, 'shopper/product_detail.html', context)


def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status='published').order_by('-date')

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        'products' : products,
        'tag' : tag
    }

    return render(request, 'shopper/tag.html', context)


def search_view(request):
    query = request.GET.get('q')

    products = Product.objects.filter(title__icontains = query).order_by('-date')

    context = {
        'products' : products, 
        'query' : query,
    }

    return render(request, 'shopper/search.html', context)


@login_required
def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title' : request.GET['title'],
        'qty' : request.GET['qty'],
        'price' : request.GET['price'],
        'image' : request.GET['image'],
        'pid' : request.GET['pid'],
        'total' : round(float(request.GET['price']) * int(request.GET['qty']), 2),
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data[str(request.GET['id'])]['total'] = round(int(cart_data[str(request.GET['id'])]['qty'])*float(cart_data[str(request.GET['id'])]['price']), 2)
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({'data':request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

@login_required
def cart(request):
    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += item['total']
        cart_total_amount = round(cart_total_amount, 2)
        context = {
            'cart_data' : request.session['cart_data_obj'],
            'cart_total_amount' : cart_total_amount, 
            'totalcartitems': len(request.session['cart_data_obj'])
        }

        return render(request, 'shopper/cart.html', context)
    else:
        return render(request, 'shopper/cart.html')


@login_required
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    values_dict_list = request.GET['form_fields']

    values_dict_list = list(eval(values_dict_list))

    values_final = {}
    for values_dict in values_dict_list:
        values_final[values_dict['name']] = values_dict['value']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += item['total']

    cart_total_amount = round(cart_total_amount, 2)


    context = render_to_string('shopper/async/cart-list.html', {
        'cart_data' : request.session['cart_data_obj'],
        'cart_total_amount' : cart_total_amount, 
        'totalcartitems': len(request.session['cart_data_obj']),
        'values_final': values_final,
    })

    return JsonResponse({'data':context, 'totalcartitems': len(request.session['cart_data_obj'])})


@login_required
def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    values_dict_list = request.GET['form_fields']

    values_dict_list = list(eval(values_dict_list))

    values_final = {}
    for values_dict in values_dict_list:
        values_final[values_dict['name']] = values_dict['value']


    if int(product_qty) == 0:
        cart_data = request.session['cart_data_obj']
        del request.session['cart_data_obj'][product_id]
        request.session['cart_data_obj'] = cart_data

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            cart_data[str(request.GET['id'])]['total'] = round(int(product_qty)*float(cart_data[str(request.GET['id'])]['price']), 2)

            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += item['total']

    cart_total_amount = round(cart_total_amount, 2)


    context = render_to_string('shopper/async/cart-list.html', {
        'cart_data' : request.session['cart_data_obj'],
        'cart_total_amount' : cart_total_amount, 
        'totalcartitems': len(request.session['cart_data_obj']),
        'values_final': values_final,
    })

    return JsonResponse({'data':context, 'totalcartitems': len(request.session['cart_data_obj'])})


@login_required
def save_checkout_info(request):
    cart_total_amount = 0
    total_amount = 0

    if request.method == 'POST':

        data = {}

        for keys in request.POST.keys():
            data[keys] = request.POST.get(keys)

        print('################################################# FORM SENT ###########################')

        request.session['full_data'] = data

        if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                total_amount += float(item['total'])

            order = CartOrder.objects.create(
                user = request.user,
                price = total_amount,
                full_name = f'{data["first_name"]} {data["last_name"]}',
                email = data['email'],
                phone = data['mobile'],
                address = data['address'],
                city = data['city'],
                country = data['country'],
            )

            del request.session['full_data']


            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += item['total']

                cart_order_products = CartOrderItems.objects.create(
                    pid = item['pid'],
                    order=order,
                    invoice_no = 'INVOICE_NO_' + str(order.id),
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total=item['total']
                )
                
            return redirect('checkout', order.oid)
        else:
            return redirect('shop')


@login_required
def checkout(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItems.objects.filter(order=order)

    if request.method == 'POST':
        code = request.POST.get('code')
        
        coupon = Coupon.objects.filter(code=code, active=True).first()

        if coupon != None:
            if coupon in order.coupons.all():
                messages.error(request, 'Coupon is already activated')
                return redirect('checkout', order.oid)
            else:
                discount = (order.price * coupon.discount / 100) + coupon.off
                print(discount)
                order.coupons.add(coupon)
                order.price -= discount
                order.saved += discount
                order.save()


                messages.success(request, 'Coupon activated')
                return redirect('checkout', order.oid)
        else:
            messages.error(request, 'Coupon does not exist')

    context = {
        'order': order,
        'order_items': order_items,
        'stripe_publishable_key' : settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, 'shopper/checkout.html', context)


@login_required
def payment_completed(request, oid):
    order = CartOrder.objects.get(oid=oid)
    
    if order.paid_status == False:
        order.paid_status = True
        order.save()

    context = {
        'order': order, 
    }

    return render(request, 'shopper/payment_completed.html', context)


@csrf_exempt
def create_checkout_session(request, oid):
    order = CartOrder.objects.get(oid=oid)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email=order.email,
        payment_method_types = ['card'],
        line_items = [
            {
                'price_data':{
                    'currency': "USD",
                    'product_data': {
                        'name': order.full_name,
                    },
                    'unit_amount': int(order.price*1000)
                },
                'quantity': 1,
            },
        ],
        mode = 'payment',
        success_url=request.build_absolute_uri(reverse('payment_completed', args=[order.id])) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('payment_failed'))
    )

    order.paid_status = False
    order.stripe_payment_intent = checkout_session['id']
    order.save()

    return JsonResponse({'sessionId':checkout_session.id})

@login_required
def payment_failed(request):
    return render(request, 'shopper/payment_failed.html')