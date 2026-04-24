from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    
    # Получаем все активные товары
    products = Product.objects.filter(is_active=True)
    
    # Общее количество товаров
    total_products = products.count()
    
    # Фильтр по категории
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Поиск
    query = request.GET.get('q', '')
    if query and query.strip():
        search_term = query.strip().lower()
        all_products = list(products)
        filtered_products = []
        
        for product in all_products:
            if search_term in product.name.lower():
                filtered_products.append(product)
        
        products = filtered_products
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query,
        'has_filter': bool(query or category_slug),
        'products_count': len(products),
        'products_total': total_products,
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})