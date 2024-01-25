from django import forms
from .models import Electronic, Supplier, Order, Pos_order, Invoice
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class LaptopForm(forms.Form):
    title = forms.CharField(
        max_length=40,
        min_length=3,
        strip=True,
        label='Наименование ноутбука')
    description = forms.CharField(
        max_length=180,
        min_length=3,
        strip=True,
        label='Описание ноутбука',
        widget=forms.Textarea,
        initial='Описание')
    photo = forms.ImageField(
        label='Фото ноутбука',
        required=False)
    price = forms.IntegerField(
        min_value=1,
        label='Цена ноутбука',
        initial=1000)
    diagonal = forms.FloatField(label='Диагональ ноутбука')
    SSD_Volume = forms.IntegerField(label='Объем SSD ноутбука')

class Supplier_form(forms.ModelForm):
    class Meta:
        model = Supplier
        # fields = '__all__'

        fields = [
            'title',
            'representative_firstname',
            'representative_lastname',
            'representative_patronymic',
            'exist'
        ]

        widgets={
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'floatingInput',
                    'placeholder': 'Название'
                }
            ),
            'representative_firstname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя предствителя'
                }
            ),
            'representative_lastname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Фамилия представителя'
                }
            ),
            'representative_patronymic': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Отчество представителя'
                }
            ),
            'exist': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            )
        }

    def cleanTitle(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Поле не должно начинаться с цифры')
        return title

class ElectronicForm(forms.ModelForm):
    class Meta:
        model = Electronic
        fields = ['title', 'description', 'photo', 'price', 'diagonal', 'SSD_Volume']


class Form_registration(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control',}),
        min_length=3
    )
    email = forms.CharField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Введите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    ),
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class Form_authorization(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=3,
    )
    password = forms.CharField(
        label='Введите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )

class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Заголовок письма',
        widget=forms.TextInput(
            attrs={'class': 'form-control', },
        )
    )
    content = forms.CharField(
        label='Тело письма',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 15, },
        )
    )