from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
import bleach

class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog:product_list_by_category', args=[self.slug])
    
    def get_product_count(self):
        """Возвращает количество активных товаров в категории"""
        return self.product_set.filter(is_active=True).count()


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField("Название", max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Остаток", default=0)
    image_url = models.URLField("URL изображения", blank=True)
    is_active = models.BooleanField("Активен", default=True)
    created = models.DateTimeField("Создан", auto_now_add=True)
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.slug])
    
    def formatted_description(self):
        """Преобразует текст из блокнота в HTML с сохранением форматирования"""
        if not self.description:
            return ""
        
        # Экранируем HTML-символы
        text = bleach.clean(self.description, strip=False)
        
        # Разбиваем на строки
        lines = text.split('\n')
        result_lines = []
        
        for line in lines:
            if line.strip() == '':
                # Пустая строка
                result_lines.append('<br>')
            else:
                # Обычная строка - проверяем отступы
                stripped_line = line.lstrip()
                indent_chars = len(line) - len(stripped_line)
                
                if indent_chars > 0:
                    # Добавляем отступ в пикселях
                    indent_px = indent_chars * 4
                    result_lines.append(
                        f'<span style="display: block; margin-left: {indent_px}px;">{stripped_line}</span>'
                    )
                else:
                    result_lines.append(line)
        
        # Соединяем с <br>
        html = '<br>'.join(result_lines)
        
        # Оборачиваем в div с уменьшенным межстрочным интервалом
        return mark_safe(f'<div style="line-height: 1.3; white-space: pre-wrap;">{html}</div>')