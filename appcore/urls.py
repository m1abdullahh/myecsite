from django.urls import path
from .views import ProductsView, search_post_request, IndexView, ProductView, add_to_shopping_cart, CartView, remove_from_shopping_cart, SearchView, ContactView, AboutView, FAQView, AccountView, ShippingDetailsView, checkout_complete, TaggedProducts, product_review, change_quantity, get_brand_products, stripe_config, create_checkout_session

app_name = "core"

urlpatterns = [
    path(route="", view=IndexView.as_view(), name="index"),
    path(route="products/", view=ProductsView.as_view(), name="products"),
    path(route="<int:pk>/product_details/", view=ProductView.as_view(), name="product_details"),
    path(route="<int:product_id>/post_review/", view=product_review, name="post_review"),
    path(route="search", view=search_post_request, name="search_post_request"),
    path(route="get_brand_products", view=get_brand_products, name="get_brand_products"),
    path(route="<int:product_id>/add_to_cart", view=add_to_shopping_cart, name="add-to-cart"),
    path(route="checkout_cart/", view=CartView.as_view(), name="checkout_cart"),
    path(route="<int:product_id>_<str:change>_quantity", view=change_quantity, name="change_quantity"),
    path(route="checkout_shipping/", view=ShippingDetailsView.as_view(), name="checkout_shipping"),
    path(route="checkout_payment/", view=checkout_complete, name="checkout_payment"),
    path(route="remove_from_shopping_cart/<int:item_id>", view=remove_from_shopping_cart, name="remove-from-cart"),
    path(route="search/query=<str:search_query>", view=SearchView.as_view(), name="search_with_query"),
    path(route="<str:query>_products/", view=TaggedProducts.as_view(), name="tagged_products"),
    path(route="contact-us/", view=ContactView.as_view(), name="contact_us"),
    path(route="about-us/", view=AboutView.as_view(), name="about_us"),
    path(route="faq/", view=FAQView.as_view(), name="faq"),
    path(route="my_account/", view=AccountView.as_view(), name="my_account"),
    path(route="stripe_config", view=stripe_config, name="stripe_config"),
    path(route="create_checkout_session", view=create_checkout_session, name="create_checkout_session"),
    # path(route="get_products_by_range", view=product_list, name="products_by_range"),
]
