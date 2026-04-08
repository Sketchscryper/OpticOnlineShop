from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_list(request):
    category_slug = request.GET.get("category")

    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True).select_related("category")

    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    return render(
        request,
        "catalog/product_list.html",
        {
            "categories": categories,
            "products": products,
            "current_category": current_category,
        },
    )


def product_detail(request, slug: str):
    product = get_object_or_404(
        Product.objects.filter(is_active=True).select_related("category"),
        slug=slug,
    )
    return render(request, "catalog/product_detail.html", {"product": product})
