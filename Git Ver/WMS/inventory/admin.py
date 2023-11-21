from django.contrib import admin
from .models import InventoryItem, Category, CategoryItem, Recipie, ItemRecipie, Platform, Sold, SoldItem

admin.site.register(InventoryItem)
admin.site.register(Category)
admin.site.register(CategoryItem)
admin.site.register(Recipie)
admin.site.register(ItemRecipie)
admin.site.register(Platform)
admin.site.register(Sold)
admin.site.register(SoldItem)
