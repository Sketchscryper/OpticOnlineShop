import re
from decimal import Decimal

from django.core.management.base import BaseCommand

from catalog.models import Category, Product

# Как в catalog/urls.py: path("catalog/<slug:slug>/", ...)
_SLUG_OK = re.compile(r"^[-a-zA-Z0-9_]+\Z")


DEMO_CATEGORIES = [
    {"name": "Оправы", "slug": "oprawy"},
    {"name": "Линзы", "slug": "linzy"},
    {"name": "Аксессуары", "slug": "aksessuary"},
]

# Slug — только [-a-zA-Z0-9_], как в catalog/urls.py (product_detail).
DEMO_PRODUCTS = [
    ("Оправы", "optic-demo-01", "Оправа Classic Metal", "Универсальная металлическая оправа.", Decimal("3490.00"), 24),
    ("Оправы", "optic-demo-02", "Оправа Slim Titanium", "Лёгкая титановая оправа.", Decimal("8990.00"), 12),
    ("Оправы", "optic-demo-03", "Оправа Acetate Bold", "Ацетатная оправа, насыщенные цвета.", Decimal("4590.00"), 18),
    ("Оправы", "optic-demo-04", "Оправа Kids Flex", "Гибкая детская оправа.", Decimal("2790.00"), 30),
    ("Линзы", "optic-demo-05", "Линзы с антибликом 1.56", "Покрытие для работы за монитором.", Decimal("2200.00"), 40),
    ("Линзы", "optic-demo-06", "Фотохром 1.60", "Затемнение на улице.", Decimal("5400.00"), 22),
    ("Линзы", "optic-demo-07", "Прогрессивные линзы", "Коррекция зрения на все дистанции.", Decimal("12900.00"), 10),
    ("Линзы", "optic-demo-08", "Blue Cut 1.67", "Тонкие линзы с защитой от синего света.", Decimal("6800.00"), 15),
    ("Аксессуары", "optic-demo-09", "Футляр жёсткий", "Защита очков в сумке.", Decimal("590.00"), 50),
    ("Аксессуары", "optic-demo-10", "Салфетка микрофибра 3 шт.", "Для бережной очистки линз.", Decimal("290.00"), 60),
    ("Аксессуары", "optic-demo-11", "Цепочка для очков", "Металлическая, регулируемая длина.", Decimal("790.00"), 35),
    ("Аксессуары", "optic-demo-12", "Спрей для линз 60 мл", "Без спирта, антистатик.", Decimal("350.00"), 45),
]


class Command(BaseCommand):
    help = "Добавляет в каталог 12 демонстрационных товаров (идемпотентно по slug)."

    def handle(self, *args, **options):
        bad_pks = [
            p.pk
            for p in Product.objects.only("pk", "slug").iterator()
            if not _SLUG_OK.match(p.slug)
        ]
        if bad_pks:
            deleted, _ = Product.objects.filter(pk__in=bad_pks).delete()
            self.stdout.write(
                self.style.WARNING(
                    f"Удалены товары со slug, не подходящим для URL (кириллица и т.п.): {deleted}"
                )
            )

        slug_to_category = {}
        for cat in DEMO_CATEGORIES:
            obj, created = Category.objects.get_or_create(
                slug=cat["slug"],
                defaults={"name": cat["name"]},
            )
            slug_to_category[cat["name"]] = obj
            if created:
                self.stdout.write(self.style.SUCCESS(f"Категория создана: {obj.name}"))

        for cat_name, slug, title, description, price, stock in DEMO_PRODUCTS:
            category = slug_to_category[cat_name]
            image_url = f"https://picsum.photos/seed/{slug}/640/480"

            product, created = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "category": category,
                    "name": title,
                    "description": description,
                    "price": price,
                    "stock": stock,
                    "is_active": True,
                    "image_url": image_url,
                },
            )
            verb = "Создан" if created else "Обновлён"
            self.stdout.write(f"  {verb}: {product.name}")

        self.stdout.write(self.style.SUCCESS("Готово: 12 товаров в каталоге."))
