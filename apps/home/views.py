from django.views.generic import TemplateView

from apps.products.models import Product


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_products"] = Product.objects.order_by("-created")[:8]
        return context
