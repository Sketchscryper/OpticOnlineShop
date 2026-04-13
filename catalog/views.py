from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product

PRODUCTS_PER_PAGE = 12


def product_list(request):
    category_slug = request.GET.get("category")
    search_query = (request.GET.get("q") or "").strip()

    categories = Category.objects.all()
    products = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .order_by("category__name", "name")
    )

    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(category__name__icontains=search_query)
        )

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    elided_page_range = paginator.get_elided_page_range(
        page_obj.number, on_each_side=1, on_ends=1
    )

    return render(
        request,
        "catalog/product_list.html",
        {
            "categories": categories,
            "page_obj": page_obj,
            "elided_page_range": elided_page_range,
            "current_category": current_category,
            "search_query": search_query,
        },
    )


def product_detail(request, slug: str):
    product = get_object_or_404(
        Product.objects.filter(is_active=True).select_related("category"),
        slug=slug,
    )
    return render(request, "catalog/product_detail.html", {"product": product})
