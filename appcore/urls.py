from django.urls import path
from .views import all_products_view, search_post_request, index, product_detail, add_to_shopping_cart, check_out_view, remove_from_shopping_cart, search_with_query, contact_us, about_us, faq, my_account, checkout_shipping, checkout_billing, checkout_complete, tagged_products, product_review, change_quantity, get_brand_products, stripe_config, create_checkout_session

app_name = "core"

urlpatterns = [
    path(route="", view=index, name="index"),
    path(route="products", view=all_products_view, name="products"),
    path(route="<int:product_id>/product_details", view=product_detail, name="product_details"),
    path(route="<int:product_id>/post_review", view=product_review, name="post_review"),
    path(route="search", view=search_post_request, name="search_post_request"),
    path(route="get_brand_products", view=get_brand_products, name="get_brand_products"),
    path(route="<int:product_id>/add_to_cart", view=add_to_shopping_cart, name="add-to-cart"),
    path(route="checkout_cart", view=check_out_view, name="checkout_cart"),
    path(route="<int:product_id>_<str:change>_quantity", view=change_quantity, name="change_quantity"),
    path(route="checkout_shipping", view=checkout_shipping, name="checkout_shipping"),
    path(route="checkout_billing", view=checkout_billing, name="checkout_billing"),
    path(route="checkout_payment", view=checkout_complete, name="checkout_payment"),
    path(route="remove_from_shopping_cart/<int:item_id>", view=remove_from_shopping_cart, name="remove-from-cart"),
    path(route="search/query=<str:query>", view=search_with_query, name="search_with_query"),
    path(route="<str:query>_products", view=tagged_products, name="tagged_products"),
    path(route="contact-us", view=contact_us, name="contact_us"),
    path(route="about-us", view=about_us, name="about_us"),
    path(route="faq", view=faq, name="faq"),
    path(route="my_account", view=my_account, name="my_account"),
    path(route="stripe_config", view=stripe_config, name="stripe_config"),
    path(route="create_checkout_session", view=create_checkout_session, name="create_checkout_session"),
]