from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, InventoryItem, CategoryItem, Recipie, ItemRecipie, Platform, Sold, Platform


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)

    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'units', 'category']


class RecipieForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=CategoryItem.objects.all(), initial=0)

    class Meta:
        model = Recipie
        fields = ['name', 'quantity', 'category']


class EditRecipieForm(forms.ModelForm):

    item = forms.ModelChoiceField(queryset=InventoryItem.objects.all(), initial=0)

    class Meta:
        model = ItemRecipie
        fields = ['item', 'quantity']


class SoldForm(forms.ModelForm):
    platform = forms.ModelChoiceField(queryset=Platform.objects.all(), initial=0)

    class Meta:
        model = Sold
        fields = ['name', 'platform']


class InventoryCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']


class RecipieCategoryForm(forms.ModelForm):

    class Meta:
        model = CategoryItem
        fields = ['name']


class SoldCategoryForm(forms.ModelForm):

    class Meta:
        model = Platform
        fields = ['name']
