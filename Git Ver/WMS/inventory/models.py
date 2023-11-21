from django.db import models
from django.contrib.auth.models import User


class InventoryItem(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    units = models.CharField(max_length=10, default='')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class CategoryItem(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class ItemRecipie(models.Model):
    item = models.ForeignKey(InventoryItem, models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.item.name

    def get_item_name(self):
        return self.item

    def get_item_quantity(self):
        return self.quantity


class Recipie(models.Model):
    name = models.CharField(max_length=200)
    items = models.ManyToManyField(ItemRecipie)
    category = models.ForeignKey('CategoryItem', on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_item_name(self):
        return self.items.name


class Platform(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Platforms'

    def __str__(self):
        return self.name


class SoldItem(models.Model):
    item = models.ForeignKey(Recipie, models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.item.name

    def get_item_name(self):
        return self.item

    def get_item_quantity(self):
        return self.quantity


class Sold(models.Model):
    name = models.CharField(max_length=200, default='')
    items = models.ManyToManyField(SoldItem)
    date = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey('Platform', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=10, default='In Process')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_item_name(self):
        return self.items.name
