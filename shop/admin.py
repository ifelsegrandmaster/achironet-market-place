from django.contrib import admin
from .models import (
    Category,
    Product,
    OverView,
    Specification,
    Attribute,
    Review
)

from django_summernote.admin import SummernoteModelAdmin

# Apply summernote to all TextField in model


class OverViewAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_display = ['id', 'product']


admin.site.register(OverView, OverViewAdmin)
# register


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ReviewInline(admin.TabularInline):
    model = Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ReviewInline]


class AttributeInline(admin.TabularInline):
    model = Attribute


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']
    inlines = [AttributeInline]
