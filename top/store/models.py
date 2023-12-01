from django.db import models
from django.contrib.auth.models import User

# BigIntegerField - большое числовое поле
# Виджет этого поля - TextInput

# BooleanField - Поле истина/ложь
# Виджет - CheckboxInput

# Charfield - поле символов
# Виджет - TextInput и обязательный аргумент max_length

# TextField - большое текстовое поле
# Виджет - Textarea

# DateField - поле даты
# Два необязательных атрибута - auto_now=True(сохранение новой даты при любом сохранении модели) и auto_now_add=True(Здесь сохранение даты только при создании экземпляра модели)
# Виджет - input type='date'

# DateTimeField - поле даты и времени
# Виджет - input type='datetime'

# EmailField - поле почты (проверяет валидность адреса почты, через EmailValidator)
#
# FileField - поле файла
# ImageField - поле изображения
# Оба поля имеют необязятельный аргумент - upload_to (директория загружаемых с сервера файлов)
# 
# IntegerField - отрицательные и положительные числа
# PositiveIntegerField - положительные числа
# SmallIntegerField - от -30к до +30к

# ForeignKey (Один ко многим)
# ManyToManyField (Многие ко многим)
# OneToOne(Один к одному)

# class Meta - с помощью него можно настроить модель
# db_table - переименование таблицы модели

# verbose_name - для переименования модели(например вместо -> класса 'Comments')
# verbose_name_plural - для переименования модели во множественном числе
class Guest(models.Model):
    token = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'guests'

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'

class Brand(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'brands'

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.IntegerField()
    is_new = models.BooleanField()
    is_discount = models.BooleanField()
    category = models.ForeignKey('store.Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('store.Brand', on_delete=models.CASCADE)
    image = models.ImageField(default='s-phone.jpg', blank=True)
    favorites = models.ManyToManyField(User, related_name='favorites')


    def __str__(self):
        return self.name
    
class SliderImage(models.Model):
    image = models.ImageField()

    def __str__(self):
        return f"Image #{self.pk}"

class CartItem(models.Model):
    guest_customer = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    chosen = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name
    
    def total_price(self):
        return self.product.price * self.quantity
    

STATUS = [
    ('Создан', 'Создан'),
    ('Принят', 'Принят'),
    ('В сборке', 'В сборке'),
    ('В пути', 'В пути'),
    ('Доставлен', 'Доставлен'),
    ('Закрыт', 'Закрыт')
]

class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    total_price = models.IntegerField()
    status = models.CharField(choices=STATUS, default=STATUS[0][0], null=True, max_length=255)
    comments = models.TextField(blank=True)


    def __str__(self):
        return f"Заказ №{self.pk}"


class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    total_price = models.IntegerField()
    comments = models.TextField(blank=True)

    def __str__(self):
        return self.item.name

RATE_CHOICES = [
    (5,'Отлично'),
    (4,'Хорошо'),
    (3,'Нормально'),
    (2,'Плохо'),
    (1,'Ужасно'),
]

class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return f'{self.customer.username} o {self.product.name}'