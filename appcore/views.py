from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import Product, OrderItem, ShoppingCart, ShippingDetails, ProductReview
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .forms import ShippingDetailsForm, ProductReviewForm
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
from django.core.mail import send_mail
from .helpers import to_dict, get_html_email
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'appcore/index.html'
    context_object_name = 'index_context'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        trending_products = Product.objects.extra(where=['%s ILIKE ANY (tags)'], params=['trending',])
        mobile_phones = Product.objects.extra(where=['%s ILIKE ANY (tags)'], params=['mobile',])
        mobile_phone_brands = mobile_phones.values_list("manufacturer")
        mobile_phone_brands = set(brand[0] for brand in mobile_phone_brands)
        tablets = Product.objects.extra(where=['%s ILIKE ANY (tags)'], params=['tablet',])
        tablet_brands = tablets.values_list("manufacturer")
        tablet_brands = set(brand[0] for brand in tablet_brands)
        context.update({"tablets": tablets})
        context.update({"mobile_phones": mobile_phones})
        context.update({'trending_products': trending_products, 'mobile_brands': mobile_phone_brands, 'tablet_brands': tablet_brands})
        return context


class ProductsView(generic.ListView):
    model = Product
    template_name = 'appcore/product.html'
    context_object_name = 'products'
    
    def get_queryset(self) -> QuerySet[Any]:
        return Product.objects.all()


class TaggedProducts(generic.ListView):
    model = Product
    context_object_name = 'possible_results'
    template_name = 'appcore/tagged_products.html'

    def get_queryset(self) -> QuerySet[Any]:
        search_query = self.kwargs['query']
        possible_results = Product.objects.annotate(search=SearchVector("tags", "product_name", "manufacturer"),
                                                ).filter(search=search_query)
        return possible_results


class ProductView(generic.DetailView):
    model = Product
    template_name = 'appcore/product_detail.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        product_id = self.kwargs['pk']
        context = {}
        product = Product.objects.get(pk=product_id)
        reviews = ProductReview.objects.filter(product=product_id)
        suggested = Product.objects.annotate(search=SearchVector("tags", "product_name", "manufacturer"),
                                                    ).filter(search=product.tags[0])
        suggested = suggested[:min(len(suggested), 6)]
        context.update({"product": product, 'suggested': suggested, 'reviews': reviews})
        return context
    

class SearchView(generic.ListView):
    model = Product
    template_name = 'appcore/search_results.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        search_query = self.kwargs['search_query']
        context = {}
        possible_results = Product.objects.annotate(search=SearchVector("tags", "product_name", "manufacturer"),
                                                    ).filter(search=search_query)
        context.update({'possible_results': possible_results, "query": search_query, "total_results": len(possible_results)})
        return context
    

class CartView(generic.View):

    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.GET.get("payment", False) == "cancelled":
            messages.info(request, "Your payment was cancelled. No Transaction was made.")
        self.template_name = 'appcore/checkout_cart.html'
        return render(request, self.template_name, {})
    
    def post(self, request, *args, **kwargs):
        return render(request, 'appcore/checkout_info.html', {})
    

class ShippingDetailsView(generic.View):

    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(request, 'appcore/checkout_info.html')

    
    def post(self, request, *args, **kwargs):
        exists = ShippingDetails.objects.filter(user=request.user).exists()
        form = ShippingDetailsForm(request.POST)
        if form.is_valid():
            if exists:
                return redirect('core:checkout_billing')
            f = form.save(commit=False)
            f.user_id = request.user.id
            f.save()
            return redirect('core:checkout_billing')
        messages.error(request, "Please fill all required fileds correctly.")
        return redirect('core:checkout_shipping')




class ContactView(generic.TemplateView):
    template_name = 'appcore/contact_us.html'


class FAQView(generic.TemplateView):
    template_name = 'appcore/faq.html'


class AccountView(generic.TemplateView):
    template_name = 'appcore/my_account.html'


class AboutView(generic.TemplateView):
    template_name = 'appcore/about_us.html'


def get_brand_products(request):
    brand = request.POST["brand"]
    products = request.POST["products"]
    if brand.lower() == "all brands":
        possible_results = Product.objects.extra(where=['%s ILIKE ANY (tags)'], params=[products,])
    else:
        possible_results = Product.objects.filter(manufacturer=brand).extra(where=['%s ILIKE ANY (tags)'], params=[products,])
    res = []
    for each in possible_results.all():
        res.append(to_dict(each))
    return HttpResponse(json.dumps({"products": res}), content_type = 'application/javascript; charset=utf8')
        

def product_review(request, product_id):
    form = ProductReviewForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Review Saved.")
        return redirect('core:product_details', product_id = product_id)
    messages.error(request ,"Please fill all fields correctly.")
    return redirect("core:product_details", product_id = product_id)


def search_post_request(request):
    search_query = request.POST["search_query"]
    return redirect(reverse('core:search_with_query', kwargs={"search_query": search_query}))


def add_to_shopping_cart(request, product_id, quantity=1):
    product = get_object_or_404(Product, pk=product_id)
    exists = OrderItem.objects.filter(product=product).exists()
    if exists:
        order = OrderItem.objects.get(product=product)
        order.quantity += 1
        order.save()
        messages.success(request, "Item added to cart.")
        return redirect("core:product_details", product_id=product_id)
    order_item = OrderItem.objects.create(product=product, quantity=quantity)
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    cart.items.add(order_item)
    cart.save()
    messages.success(request, "Item added to cart.")
    return redirect("core:product_details", product_id=product_id)


def change_quantity(request, product_id, change):
    order = OrderItem.objects.get(product=product_id)
    if change == "decrease":
        order.quantity -= 1
        order.save()
        return redirect('core:checkout_cart')
    order.quantity += 1
    order.save()
    return redirect('core:checkout_cart')
    

def remove_from_shopping_cart(request, item_id):
    cart = ShoppingCart.objects.get(user=request.user)
    item = OrderItem.objects.get(pk=item_id)
    cart.items.remove(item)
    cart.save()
    item.delete()
    messages.success(request, "Item has been removed from your cart.")
    return redirect("core:index")


def checkout_complete(request):
    cart = ShoppingCart.objects.get(user=request.user)
    subtotal = cart.subtotal
    ordered_items = []
    for each in cart.items.all():
        ordered_items.append(each)
        each.delete()

    try:
        send_mail(subject=f"Order #{cart.id} Confirmed", message="", from_email="elsajones68@gmail.com",
                  recipient_list=[request.user.email],
        html_message=get_html_email(ordered_items, subtotal))
    except Exception as e:
        print(e)

    cart.delete()
    return render(request, 'appcore/checkout_complete.html', {'ordered_items': ordered_items, 'subtotal': subtotal})

@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {'public_key': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)
        

@csrf_exempt
def create_checkout_session(request):
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    items = []
    for item in cart.items.all():
        items.append({"price": item.product.price_id, "quantity": item.quantity})
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'checkout_payment',
                cancel_url=domain_url + 'checkout_cart?payment=cancelled',
                payment_method_types=['card'],
                mode='payment',
                line_items=items
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})