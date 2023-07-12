from appcore.models import Product, ShoppingCart

def context(request):
    context = {}
    if request.user.is_authenticated:
        cart_data, created = ShoppingCart.objects.get_or_create(user=request.user)
        categories = set()
        for i in Product.objects.values('tags'):
            for k, v in i.items():
                for j in v:
                    categories.add(j)
        brands = set()
        for i in Product.objects.values('manufacturer'):
            for k, v in i.items():
                brands.add(v)
        popular = Product.objects.extra(where=['%s ILIKE ANY (tags)'], params=['trending',])
        context.update({'brands': brands})
        context.update({'cart': cart_data})
        context.update({'categories': categories, 'popular_products': popular})
    return context