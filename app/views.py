from django.shortcuts import render,redirect
from django.views import View
from app.models import Customer,Product,Cart,OrderPlaced
from app.forms import CustomerRegistrationForm , CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductView(View):
 def get(self,request):
  totalitem = 0
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles, 'totalitem':totalitem})

class ProductDetailView(View):
 def get(self,request,pk):
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
   item_already_in_cart =Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()
  return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart})
@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')
@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user= request.user
  cart = Cart.objects.filter(user=user)
  # print(cart)
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  # print(cart_product)
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount+= tempamount
    total_amount = amount + shipping_amount
  return render(request, 'app/addtocart.html',{'carts':cart,'total_amount':total_amount, 'amount':amount})
 
def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount  = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount+= tempamount

    data={
     'quantity':c.quantity,
     'amount':amount,
     'total_amount':amount + shipping_amount,
    }
    return JsonResponse(data)
    

def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.save()
    amount  = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount+= tempamount

    data={
     'quantity':c.quantity,
     'amount':amount,
     'total_amount':amount + shipping_amount
    }
    return JsonResponse(data)
    
    
def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount  = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount+= tempamount

    data={
     'amount':amount,
     'total_amount': amount + shipping_amount
    }
    return JsonResponse(data)
    


def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':op})

def mobile(request,data=None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'Redmi' or data == 'Samsung':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
 return render(request, 'app/mobile.html',{'mobiles':mobiles})

def laptop(request,data=None):
 if data == None:
  laptops = Product.objects.filter(category='L')
 elif data == 'Dell' or data == 'Apple':
  laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'below':
  laptops = Product.objects.filter(category='L').filter(discounted_price__lt=100000)
 elif data == 'above':
  laptops = Product.objects.filter(category='L').filter(discounted_price__gt=100000)
 return render(request, 'app/laptop.html',{'laptop':laptops})

class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html',{'form':form})
 
 def post(self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Your registrations has successfully done!')
   form.save()
  return render(request, 'app/customerregistration.html',{'form':form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = sum(c.quantity * c.product.discounted_price for c in cart_items)
    shipping_amount = 70
    total_amount = amount + shipping_amount

    return render(request, 'app/checkout.html', {
        'add': add,
        'cart_items': cart_items,
        'totalamount': total_amount,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })
@login_required
def create_checkout_session(request):
    if request.method == "POST":

        custid = request.POST.get('custid')
        if not custid:
            messages.error(request, "Please select a shipping address.")
            return redirect('checkout')

        user = request.user
        customer = Customer.objects.get(id=custid)
        cart_items = Cart.objects.filter(user=user)

        total_amount = int((sum(item.quantity * item.product.discounted_price for item in cart_items) + 70) * 100)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'Commerzia Order Payment'},
                        'unit_amount': total_amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=settings.STRIPE_SUCCESS_URL + f"?custid={custid}",
                cancel_url=settings.STRIPE_CANCEL_URL,
            )

            return redirect(checkout_session.url, code=303)

        except Exception as e:
            messages.error(request, f"Stripe Error: {e}")
            return redirect('checkout')

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    if not custid:
        return redirect('checkout')

    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced.objects.create(user=user, customer=customer, product=c.product, quantity=c.quantity)
        c.delete()
    return redirect('orders')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self,request):
  form = CustomerProfileForm()
  return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})
 
 def post(self,request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name=form.cleaned_data['name']
   locality=form.cleaned_data['locality']
   city=form.cleaned_data['city']
   state=form.cleaned_data['state']
   zipcode=form.cleaned_data['zipcode']
   reg = Customer(user=usr,name=name, locality=locality, city=city, state=state, zipcode=zipcode)
   reg.save()
   messages.success(request, 'Congratulations!!! your profile updated successfully!!')
  return render(request, 'app/profile.html',{'form':form,'active':'btn-primary',"user": request.user,})
 
def search(request):
    query = request.GET.get('query')
    results = []
    if query:
        results = Product.objects.filter(title__icontains=query)
    return render(request, 'app/search.html', {'results': results, 'query': query})

def top_wear(request):
    products = Product.objects.filter(category='TW')  
    return render(request, 'app/topwear.html', {'products': products})

def bottom_wear(request):
    products = Product.objects.filter(category='BW')
    return render(request, 'app/bottomwear.html', {'products': products})


# Stripe webhook endpoint
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        custid = session['metadata'].get('custid')
        user_id = session['metadata'].get('user_id')

        # Save orders
        try:
            customer = Customer.objects.get(id=custid)
            cart_items = Cart.objects.filter(user_id=user_id)
            for item in cart_items:
                OrderPlaced.objects.create(
                    user_id=user_id,
                    customer=customer,
                    product=item.product,
                    quantity=item.quantity
                )
                item.delete()
        except Exception as e:
            print("Order saving error:", e)

    return HttpResponse(status=200)