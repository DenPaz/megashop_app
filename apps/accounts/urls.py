from django.urls import path

from .views import AddressUpdateView
from .views import OrderListView
from .views import PasswordUpdateView
from .views import PersonalInfoUpdateView

app_name = "accounts"

urlpatterns = [
    path(
        route="personal-info-update/",
        view=PersonalInfoUpdateView.as_view(),
        name="personal_info_update",
    ),
    path(
        route="address-update/",
        view=AddressUpdateView.as_view(),
        name="address_update",
    ),
    path(
        route="password-update/",
        view=PasswordUpdateView.as_view(),
        name="password_update",
    ),
    path(
        route="order-list/",
        view=OrderListView.as_view(),
        name="order_list",
    ),
]
