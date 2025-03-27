from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Bouquet(models.Model):
    """Букет"""
    name = models.CharField(verbose_name='Название букета', max_length=50)
    image = models.ImageField(verbose_name='Изображение букета')
    price = models.PositiveIntegerField(verbose_name='Цена')
    description = models.CharField(verbose_name='Описание', max_length=100)
    composition = models.CharField(verbose_name='Состав', max_length=100)
    Birthday = 'День рождения'
    Wedding = 'Свадьба'
    School = 'В школу'
    No_reason = 'Без повода'
    Another = 'Другой повод'
    occasions = [
        (Birthday, 'День рождения'),
        (Wedding, 'Свадьба'),
        (School, 'В школу'),
        (No_reason, 'Без повода'),
        (Another, 'Другой повод'),
    ]
    occasion = models.CharField(verbose_name='Повод',
                                    max_length=256,
                                    choices=occasions,
                                    default=No_reason,)
    No_color = 'Без цветовой гаммы'
    Red = 'Красные'
    Blue = 'Синие'
    colors = [
        (No_color, 'Без цветовой гаммы'),
        (Red, 'Красные'),
        (Blue, 'Синие'),
    ]
    color_scheme = models.CharField(verbose_name='Цветовая гамма',
                                    max_length=256,
                                    choices=colors,
                                    default=No_color,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'


class Customer(models.Model):
    """Покупатель"""
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний ID покупателя',
        unique=True
    )
    tg_username = models.CharField('Имя покупателя в Telegram', max_length=50, blank=True)
    first_name = models.CharField('Имя', max_length=5, blank=True)
    last_name = models.CharField('Фамилия', max_length=256, blank=True)
    phone_number = PhoneNumberField('Номер телефона')
    home_address = models.CharField('Адрес доставки', max_length=50, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} (ID: {self.external_id})'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    """Заказ"""
    customer = models.CharField(verbose_name='Имя покупателя', blank=True, max_length=256)
    customer_chat_id = models.CharField(verbose_name='Chat ID покупателя', blank=True, max_length=256)
    order_price = models.PositiveIntegerField(verbose_name='Цена заказа')
    Processing = 'Заявка обрабатывается'
    Cooking = 'Собираем ваш букет'
    Transport = 'Букет в пути'
    Delivered = 'Букет у вас'
    order_statuses = [
        (Processing, 'Заявка обрабатывается'),
        (Cooking, 'Собираем ваш букет'),
        (Transport, 'Букет в пути'),
        (Delivered, 'Букет у вас'),
    ]
    order_status = models.CharField(verbose_name='Статус заказа',
                                    max_length=256,
                                    choices=order_statuses,
                                    default=Processing, )
    comments = models.CharField(verbose_name='Комментарии', blank=True, max_length=256)
    delivery_address = models.CharField(verbose_name='Адрес доставки', max_length=256, default=' ')
    delivery_date = models.CharField(verbose_name='Дата доставки', max_length=30, blank=True)
    delivery_time = models.CharField(verbose_name='Время доставки', max_length=30, blank=True)
    flower_name = models.ForeignKey(Bouquet,
                                  verbose_name='Название букета',
                                  related_name='orders',
                                  blank=True,
                                  null=True,
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.flower_name} {self.customer} {self.delivery_date} {self.delivery_time}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
