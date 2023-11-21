from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate,  login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm, RecipieForm, SoldForm, InventoryCategoryForm, RecipieCategoryForm, SoldCategoryForm
from .models import InventoryItem, Category, CategoryItem, Recipie, ItemRecipie, Sold, Platform, SoldItem


class Index(TemplateView):
    template_name = 'inventory/index.html'


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = InventoryItem.objects.filter(user=self.request.user.id).order_by('id')

        return render(request, 'inventory/dashboard.html', {'items': items})


class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'inventory/signup.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )

            login(request, user)
            return redirect('index')
        return render(request, 'inventory/signup.html', {'form': form})


class AddItemInventory(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditItemInventory(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')


class DeleteItemInventory(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'


class Stock(LoginRequiredMixin, View):

    def get(self, request):
        items = Recipie.objects.filter(user=self.request.user.id).order_by('id')

        return render(request, 'inventory/stock.html', {'items': items})


class DeleteItemStock(LoginRequiredMixin, DeleteView):
    model = Recipie
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('stock')
    context_object_name = 'item'


class AddNewRecipie(LoginRequiredMixin, CreateView):
    model = Recipie
    form_class = RecipieForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('stock')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryItem.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditRecipie(LoginRequiredMixin, View):

    def get(self, request, pk):

        items = ItemRecipie.objects.filter(recipie=pk)
        name = Recipie.objects.get(pk=pk)

        return render(request, 'inventory/recipie.html', {'items': items, 'pk': pk, 'name': name})


class DeleteItemRecipie(LoginRequiredMixin, DeleteView):
    model = ItemRecipie
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('stock')
    context_object_name = 'item'


def increase_recipie(request, item_id):
    ingredient = ItemRecipie.objects.get(id=item_id)
    pk = ingredient.recipie_set.all()
    for i in pk:
        pk = i.id
    ingredient.quantity += 1
    ingredient.save()

    return redirect('recipie', pk)


def reduce_recipie(request, item_id):
    ingredient = ItemRecipie.objects.get(id=item_id)
    pk = ingredient.recipie_set.all()
    for i in pk:
        pk = i.id

    if ingredient.quantity >= 2:
        ingredient.quantity -= 1
        ingredient.save()
    else:
        pass

    return redirect('recipie', pk)


class AddToRecipie(LoginRequiredMixin, View):

    def get(self, request, pk):
        items = InventoryItem.objects.all()

        return render(request, 'inventory/addtorecipie.html', {'items': items, 'pk': pk})


def include(request, item_id, pk):
    inventory = InventoryItem.objects.get(pk=item_id)
    recipie = Recipie.objects.get(pk=pk)

    if ItemRecipie.objects.filter(item=inventory, recipie=pk).exists():
        new_item_recipie = ItemRecipie.objects.get(item=inventory, recipie=pk)
        new_item_recipie.quantity += 1
        new_item_recipie.save()
    else:
        new_item_recipie = ItemRecipie.objects.create(item=inventory, quantity=1)
        new_item_recipie.save()

        recipie.items.add(new_item_recipie)
        recipie.save()

    return redirect('add_to_recipie', pk)


def produce_recipie(request, item_id):
    recipie = Recipie.objects.get(pk=item_id)
    items_recipie = ItemRecipie.objects.filter(recipie=item_id)
    qty_item = 0
    qty_recipie = 0

    for item in items_recipie:
        item_inventory = InventoryItem.objects.get(itemrecipie=item)
        if item_inventory.quantity >= item.quantity:
            qty_recipie += 1
            qty_item += 1
        else:
            qty_item += 1

    if qty_item == qty_recipie:
        for item in items_recipie:
            item_inventory = InventoryItem.objects.get(itemrecipie=item)
            item_inventory.quantity -= item.quantity
            item_inventory.save()

        recipie.quantity += 1
        recipie.save()
    else:
        pass



    return redirect('stock')


class SoldItems(LoginRequiredMixin, View):

    def get(self, request):
        items = Sold.objects.filter(user=self.request.user.id).order_by('id')

        return render(request, 'inventory/sold.html', {'items': items})


class DeleteSoldItem(LoginRequiredMixin, DeleteView):
    model = Sold
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('sold')
    context_object_name = 'item'


class DeleteSaleItem(LoginRequiredMixin, DeleteView):
    model = SoldItem
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('sold')
    context_object_name = 'item'


class AddNewSale(LoginRequiredMixin, CreateView):
    model = Sold
    form_class = SoldForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('sold')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platform'] = Platform.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def change_sale_status(request, item_id):
    sale = Sold.objects.get(id=item_id)
    items = SoldItem.objects.filter(sold=item_id)
    qty_sale = 0
    qty_stock = 0

    for item in items:
        stock_item = Recipie.objects.get(solditem=item)
        if stock_item.quantity >= item.quantity:
            qty_sale += 1
            qty_stock += 1
        else:
            qty_sale += 1

    if sale.status == 'In Process':
        if qty_sale == qty_stock:
            for item in items:
                stock_item = Recipie.objects.get(solditem=item)
                if item.quantity <= stock_item.quantity:
                    stock_item.quantity -= item.quantity
                    stock_item.save()

            sale.status = 'Done'
            sale.save()
    else:
        pass

    return redirect('sold')


class EditSale(LoginRequiredMixin, View):

    def get(self, request, pk):

        items = SoldItem.objects.filter(sold=pk)
        name = Sold.objects.get(pk=pk)

        return render(request, 'inventory/sold_details.html', {'items': items, 'pk': pk, 'name': name})


class AddToSale(LoginRequiredMixin, View):

    def get(self, request, pk):

        items = Recipie.objects.all()

        return render(request, 'inventory/addtosale.html', {'items': items, 'pk': pk})


def include_into_sale(request, item_id, pk):
    sale = Sold.objects.get(id=pk)
    item = Recipie.objects.get(id=item_id)

    if SoldItem.objects.filter(item=item, sold=pk).exists():
        new_item_sale = SoldItem.objects.get(item=item, sold=pk)
        new_item_sale.quantity += 1
        new_item_sale.save()

    else:
        new_item_sale = SoldItem.objects.create(item=item, quantity=1)
        new_item_sale.save()

        sale.items.add(new_item_sale)
        sale.save()

    return redirect('add_to_sale', pk)


def increase_sale(request, item_id):
    item = SoldItem.objects.get(id=item_id)
    pk = item.sold_set.all()
    for i in pk:
        pk = i.id
    item.quantity += 1
    item.save()

    return redirect('sold_details', pk)


def reduce_sale(request, item_id):
    item = SoldItem.objects.get(id=item_id)
    pk = item.sold_set.all()
    for i in pk:
        pk = i.id

    if item.quantity >= 2:
        item.quantity -= 1
        item.save()
    else:
        pass

    return redirect('sold_details', pk)


class AllCategories(TemplateView):
    template_name = 'inventory/categories.html'


# class EditInventoryCategory(LoginRequiredMixin, UpdateView):
#     model = Category
#     form_class = InventoryCategoryForm
#     template_name = 'inventory/item_form.html'
#     success_url = reverse_lazy('edit_categories')
#
#
# class EditRecipieCategory(LoginRequiredMixin, UpdateView):
#     model = CategoryItem
#     form_class = RecipieCategoryForm
#     template_name = 'inventory/item_form.html'
#     success_url = reverse_lazy('edit_categories')
#
#
# class EditSoldCategory(LoginRequiredMixin, UpdateView):
#     model = Platform
#     form_class = SoldCategoryForm
#     template_name = 'inventory/item_form.html'
#     success_url = reverse_lazy('edit_categories')
#
#
# class InventoryCategories(LoginRequiredMixin, View):
#
#     def get(self, request):
#         items = Category.objects.all()
#
#         return render(request, 'inventory/edit_categories.html', {'items': items})
