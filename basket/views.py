from django.shortcuts import render, redirect, get_object_or_404
from electronicAccessories.models import Electronic
from .basket import Basket
from .forms import BasketAddProductForm
from django.views.decorators.http import require_POST


@require_POST
def basket_add(request, product_id):
    basket = Basket(request)
    product_obj = get_object_or_404(Electronic, pk=product_id)
    form = BasketAddProductForm(request.POST)

    if form.is_valid():
        basket_info = form.cleaned_data

        basket.add(
            product=product_obj,
            count=basket_info['count_product'],
            update_count=basket_info['update']
        )

    return redirect('list_basket_product')


def basket_remove(request, product_id):
    basket = Basket(request)
    product_obj = get_object_or_404(Electronic, pk=product_id)

    basket.remove(product_obj)
    return redirect('list_basket_product')


def basket_info(request):
    basket = Basket(request)
    return render(request, 'basket/detail.html', {'basket': basket})


def basket_clear(request):
    basket = Basket(request)
    basket.clear()
    return redirect('laptop_list')