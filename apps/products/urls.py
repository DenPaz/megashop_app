from django.urls import path

from .views import ProductDetailView

app_name = "products"

urlpatterns = [
    path(
        route="<slug>/",
        view=ProductDetailView.as_view(),
        name="product_detail",
    ),
]
