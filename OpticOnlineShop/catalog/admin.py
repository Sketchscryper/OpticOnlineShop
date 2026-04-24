from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_product_count']
    prepopulated_fields = {'slug': ('name',)}
    
    def get_product_count(self, obj):
        return obj.get_product_count()
    get_product_count.short_description = 'Товаров'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_active', 'created']
    list_filter = ['is_active', 'category', 'created']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_active']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'slug', 'price', 'stock', 'is_active')
        }),
        ('Изображение', {
            'fields': ('image_url',),
        }),
        ('Описание', {
            'fields': ('description',),
            'classes': ('wide',),
            'description': '''
                <div style="background: #f0f7ff; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <strong>📝 Форматирование текста:</strong><br>
                    • Просто вставляйте текст из блокнота — все переносы строк и отступы сохранятся<br>
                    • Пустые строки создают отступы между абзацами<br>
                    • Отступы (пробелы или табуляция в начале строки) будут сохранены<br>
                    • Можно использовать HTML-теги: &lt;b&gt;, &lt;i&gt;, &lt;ul&gt;, &lt;li&gt; и др.
                </div>
            ''',
        }),
    )