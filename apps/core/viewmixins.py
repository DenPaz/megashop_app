from collections.abc import Iterable

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django_htmx.http import HttpResponseClientRedirect

TemplateSpec = str | Iterable[str]


class SearchMixin:
    search_param = "q"
    search_fields = []

    def get_search_query(self):
        return self.request.GET.get(self.search_param, "").strip()

    def apply_search(self, queryset):
        query = self.get_search_query()
        if not query or not self.search_fields:
            return queryset
        terms = [term for term in query.split() if term]
        query_filter = Q()
        for term in terms:
            term_query = Q()
            for field in self.search_fields:
                term_query |= Q(**{f"{field}__icontains": term})
            query_filter |= term_query
        return queryset.filter(query_filter).distinct()

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.apply_search(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.search_param] = self.get_search_query()
        query_string = self.request.GET.copy()
        query_string.pop("page", None)
        context["query_string"] = query_string.urlencode()
        return context


class HtmxTemplateMixin:
    htmx_template_name: TemplateSpec | None = None
    htmx_param: str | None = None
    htmx_routes: dict[str, TemplateSpec] | None = None
    htmx_default_route: str | None = None
    htmx_404_on_unknown: bool = True

    def is_htmx(self) -> bool:
        return bool(getattr(self.request, "htmx", False))

    def is_boosted(self) -> bool:
        htmx = getattr(self.request, "htmx", None)
        return bool(getattr(htmx, "boosted", False)) if htmx else False

    def is_htmx_partial(self) -> bool:
        return self.is_htmx() and not self.is_boosted()

    def is_router_mode(self) -> bool:
        return bool(self.htmx_param and self.htmx_routes)

    def get_route_key(self) -> str | None:
        if not self.htmx_param:
            return None
        req = self.request
        return req.GET.get(self.htmx_param) or req.POST.get(self.htmx_param)

    def dispatch(self, request, *args, **kwargs):
        if self.is_htmx_partial():
            if self.is_router_mode():
                if not isinstance(self.htmx_routes, dict) or not self.htmx_param:
                    msg = (
                        f"{self.__class__.__name__}: router mode requires "
                        "`htmx_param` and a dict in `htmx_routes`."
                    )
                    raise ImproperlyConfigured(msg)
                if (
                    self.htmx_default_route
                    and self.htmx_default_route not in self.htmx_routes
                ):
                    msg = (
                        f"{self.__class__.__name__}: `htmx_default_route` "
                        f"('{self.htmx_default_route}') not in `htmx_routes`."
                    )
                    raise ImproperlyConfigured(msg)
            elif self.htmx_template_name is None:
                msg = (
                    f"{self.__class__.__name__}: HTMX partial request received but "
                    f"neither router mode nor `htmx_template_name` is configured."
                )
                raise ImproperlyConfigured(msg)
        return super().dispatch(request, *args, **kwargs)

    def _as_template_list(self, template: TemplateSpec | None) -> list[str] | None:
        if template is None:
            return None
        return [template] if isinstance(template, str) else list(template)

    def _resolve_single_template(self) -> list[str]:
        return self._as_template_list(self.htmx_template_name)

    def _resolve_router_template(self, key: str | None) -> list[str]:
        routes = self.htmx_routes or {}
        if key is None and self.htmx_default_route:
            names = self._as_template_list(routes[self.htmx_default_route])
            if names:
                return names
            msg = (
                f"{self.__class__.__name__}: `htmx_default_route` "
                f"('{self.htmx_default_route}') maps to an empty template list."
            )
            raise ImproperlyConfigured(msg)
        template = routes.get(key)
        if not template:
            if self.htmx_404_on_unknown:
                msg = f"Unknown HTMX route '{key}' for {self.__class__.__name__}"
                raise Http404(msg)
            if self.htmx_default_route:
                names = self._as_template_list(routes.get(self.htmx_default_route))
                if names:
                    return names
            names = self._as_template_list(self.htmx_template_name)
            if names:
                return names
            msg = (
                f"{self.__class__.__name__}: Unknown route '{key}' and no usable "
                "fallback (`htmx_default_route` or `htmx_template_name`)."
            )
            raise ImproperlyConfigured(msg)
        names = self._as_template_list(template)
        if not names:
            msg = f"{self.__class__.__name__}: route '{key}' did not map to a template."
            raise ImproperlyConfigured(msg)
        return names

    def get_template_names(self) -> list[str]:
        if self.is_htmx_partial():
            if self.is_router_mode():
                return self._resolve_router_template(self.get_route_key())
            return self._resolve_single_template()
        return super().get_template_names()

    def get_htmx_context_data(self, key: str | None) -> dict:
        return {"htmx_key": key}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.is_htmx_partial():
            context.update(self.get_htmx_context_data(self.get_route_key()))
        elif self.htmx_param:
            context["htmx_key"] = self.get_route_key() or self.htmx_default_route
        return context


class HtmxRedirectMixin:
    def get_htmx_redirect_url(self):
        return self.get_success_url()

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.htmx and isinstance(response, HttpResponseRedirect):
            return HttpResponseClientRedirect(self.get_htmx_redirect_url())
        return response

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return self._redirect_htmx(response)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return self._redirect_htmx(response)

    def _redirect_htmx(self, response):
        if self.request.htmx and isinstance(response, HttpResponseRedirect):
            return HttpResponseClientRedirect(response.url)
        return response
