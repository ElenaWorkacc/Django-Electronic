from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .models import Electronic, Supplier, Order, Pos_order, Invoice
from .forms import LaptopForm, Supplier_form, ElectronicForm, Form_registration, Form_authorization, ContactForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .utils import DefaultValue
from django.urls import reverse, reverse_lazy

from django.core.paginator import Paginator

from django.contrib.auth import login, logout

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from django.core.mail import send_mail
from django.conf import settings

from django.http import JsonResponse
from .serializers import ElectronicSerilizer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets

from basket.forms import BasketAddProductForm

def index(request):
    print(request)
    return HttpResponse('Hello Django!')


def laptop(request):
    electronics = Electronic.objects.all()  # Получение всех значений из базы данных
    responce = '<h1>Список ноутбуков</h1>'
    for item in electronics:
        responce += f'<div>\n<p>{item.title}</p>\n<p>{item.price}</p></div>'
    return HttpResponse(responce)


def index_template(request):
    return render(request, 'electronicAccessories/index.html')


def laptops_template(request):
    context = {'name': 'Ноутбуки'}

    laptops = Electronic.objects.all()

    # context['laptops_list'] = laptops

    paginator = Paginator(laptops, 3)
    page_number = request.GET.get('page', 1)

    page_object = paginator.get_page(page_number)

    context['pageObject'] = page_object

    if request.method == "GET":
        laptop_id = request.GET.get('id', 1)
        try:
            laptop_one = Electronic.objects.get(pk=laptop_id)
        except:
            pass
        else:
            context['laptop_one'] = laptop_one

        context['title'] = request.GET.get('title', 'HP')
    elif request.method == "POST":
        laptop_id = request.POST.get('id', 1)
        try:
            laptop_one = Electronic.objects.get(pk=laptop_id)
        except:
            pass
        else:
            context['laptop_one'] = laptop_one

        context['title'] = request.POST.get('title', 'HP')

    return render(
        request=request,
        template_name='electronicAccessories/laptops.html',
        context=context)

@login_required
def laptop_add(request):
    if request.method == "POST":
        context = dict()
        context['title'] = request.POST.get('title')
        context['description'] = request.POST.get('description')
        context['photo'] = request.POST.get('photo')
        context['price'] = request.POST.get('price')
        context['diagonal'] = request.POST.get('diagonal')
        context['SSD_Volume'] = request.POST.get('SSD_Volume')
        context['date_update'] = request.POST.get('date_update')

        Electronic.objects.create(
            title=context['title'],
            description=context['description'],
            photo=context['photo'],
            price=context['price'],
            diagonal=context['diagonal'],
            SSD_Volume=context['SSD_Volume'],
            date_update=context['date_update']
        )
        return HttpResponseRedirect('/electronic/laptopsList/')
    else:
        laptopform = LaptopForm()
        context = {'form': laptopform}
        return render(request, 'electronicAccessories/laptop-add.html', context=context)


def laptop_detail(request, laptop_id):
    laptop = get_object_or_404(Electronic, pk=laptop_id)
    basket_form = BasketAddProductForm()
    return render(request, 'electronicAccessories/laptop-info.html', {'laptop_item': laptop, 'basket_form': basket_form})

@permission_required('electronicAccessories.change_electronic')
def laptop_update(request, laptop_id):
    laptop = get_object_or_404(Electronic, pk=laptop_id)
    if request.method == 'POST':
        form = ElectronicForm(request.POST, instance=laptop)
        if form.is_valid():
            form.save()
            return redirect('one_laptop', laptop_id=laptop_id)
    else:
        form = ElectronicForm(instance=laptop)
    return render(request, 'electronicAccessories/laptop_update.html', {'laptop_item': laptop, 'form': form})

def laptop_delete(request, laptop_id):
    laptop = get_object_or_404(Electronic, pk=laptop_id)
    if request.method == 'POST':
        laptop.delete()
        return redirect('laptop_list')
    return render(request, 'electronicAccessories/laptop-delete.html', {'laptop_item': laptop})

def supplier_list(request):
    context = {'name': 'Поставщики'}
    suppliers = Supplier.objects.all()

    paginator = Paginator(suppliers, 2)
    page_number = request.GET.get('page', 1)

    page_object = paginator.get_page(page_number)

    context['pageObject'] = page_object

    return render(request, 'electronicAccessories/supplier/supplier_list.html',
                  {'pageObject': page_object, 'name': 'Список поставщиков'})


class Supplier_list_view(ListView, DefaultValue):
    model = Supplier
    template_name = 'electronicAccessories/supplier/supplier_list.html'
    context_object_name = 'supplier'
    extra_context = {'name': 'Список поставщиков из класса'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context = self.add_title_context(context=context, title_name='Страница поставщиков')
        context['info'] = 'Поставщики, которые работают с нами'
        return context

    def get_queryset(self):
        return Supplier.objects.filter(exist=True).order_by('title')


class SupplierOneView(DeleteView):
    model = Supplier
    template_name = 'electronicAccessories/supplier/supplier_info.html'
    context_object_name = 'supplier_page'
    pk_url_kwarg = 'supplier_id'


def supplier_base(request):
    if request.method == "POST":
        form = Supplier_form(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            Supplier.objects.create(
                title=form.cleaned_data['title'],
                representative_firstname=form.cleaned_data['representative_firstname'],
                representative_lastname=form.cleaned_data['representative_lastname'],
                representative_patronymic=form.cleaned_data['representative_patronymic'],
                exist=form.cleaned_data['exist']
            )

            return redirect('list_supplier')
        else:
            context = {'form': form}
            return render(request, 'electronicAccessories/supplier/supplier_add.html', context)

    else:
        form = Supplier_form
        context = {'form': form}
        return render(request, 'electronicAccessories/supplier/supplier_add.html', context)


class Supplier_create_view(CreateView):
    model = Supplier
    form_class = Supplier_form
    template_name = 'electronicAccessories/supplier/supplier_add.html'

    context_object_name = 'form'
    success_url = reverse_lazy('list_supplier_view')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class Supplier_update_view(UpdateView):
    model = Supplier
    form_class = Supplier_form
    template_name = 'electronicAccessories/supplier/supplier_update.html'

    context_object_name = 'form'

    @method_decorator(permission_required('electronicAccessories.change_supplier'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class Supplier_delete_view(DeleteView):
    model = Supplier
    success_url = reverse_lazy('list_supplier_view')

    @method_decorator(permission_required('electronicAccessories.delete_supplier'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def user_registration(request):
    if request.method == "POST":
        form = Form_registration(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('laptop_index')
    else:
        form = Form_registration()
    return render(request, 'electronicAccessories/auth/registr.html', {'form': form})


def user_authorization(request):
    if request.method == "POST":
        form = Form_authorization(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print('is_anon', request.user.is_anonymous)
            print('is_auth', request.user.is_authenticated)
            login(request, user)
            print('is_anon', request.user.is_anonymous)
            print('is_auth', request.user.is_authenticated)
            print(user)
            return redirect('laptop_index')
    else:
        form = Form_authorization()
    return render(request, 'electronicAccessories/auth/auth.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('auth')

def send_email(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                settings.EMAIL_HOST_USER,
                ['workaccountant@yandex.ru'],
                fail_silently=False
            )
            if mail:
                return redirect('laptop_index')
    else:
        form = ContactForm()
    return render(request, 'electronicAccessories/email.html', {'form': form})

@api_view(['GET', 'POST'])
def laptops_api_list(request):
    if request.method == "GET":
        laptops_list = Electronic.objects.all()
        serializer = ElectronicSerilizer(laptops_list, many=True)
        return Response({'laptops_list': serializer.data})
    elif request.method == "POST":
        serializer = ElectronicSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def laptop_api_one(request, pk, format=None):
    laptop_obj =  get_object_or_404(Electronic, pk=pk)
    if laptop_obj.exist:
        if request.method == 'GET':
            serializer = ElectronicSerilizer(laptop_obj)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ElectronicSerilizer(laptop_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Данные были успешно обновлены', 'laptop': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUESTT)
        elif request.method == 'DELETE':
            laptop_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)