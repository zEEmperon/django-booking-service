from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

class Offer(models.Model):

    LODGING_TYPES = (
        ('F', 'Flat'),
        ('HST', 'Hostel'),
        ('HS', 'House'),
        ('HR', 'Hotel Room')
    )
    PLACES_NUMBERS = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    )

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(max_length=5000)

    image = models.ImageField(upload_to='photo/%Y/%m/%d/')

    lodging_type = models.CharField(max_length=3, choices=LODGING_TYPES, default='HR')
    places = models.IntegerField(default=1, choices=PLACES_NUMBERS)
    night_price = models.PositiveIntegerField(default=100, validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name='Night price')

    isWifi = models.BooleanField(default=True, verbose_name='WiFi')
    isConditioner = models.BooleanField(default=False, verbose_name='Conditioner')
    isKitchen = models.BooleanField(default=False, verbose_name='Kitchen')
    isBreakfast = models.BooleanField(default=False, verbose_name='Breakfast')

    date_created = models.DateField(auto_now_add=True)

    isPublished = models.BooleanField(default=True, verbose_name='Published')

    # добавить метод get_absolute_url()
    # сортировку сделать и фильтрацию
    # добавить комментарии (один пользователь = много комментариев)
    # добавить систему рейтинга (один пользователь = одна оценка)
    # rating = models.FloatField(default=0, editable=False)
    # total_rates = models.PositiveIntegerField(default=1, editable=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('booking:detail', kwargs={'slug':self.slug,})

class Booking(models.Model):

    PAYMENT_METHOD = (
        ('Cash', 'Cash'),
        ('Cart', 'Cart')
    )

    BOOKING_STATES = (
        ('P', 'In processing'),
        ('A', 'Accepted'),
        ('R', 'Rejected')

    )

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')

    payment_method = models.CharField(max_length=4,choices=PAYMENT_METHOD, default='Cash')

    arrival_date = models.DateField()
    departure_date = models.DateField()

    state = models.CharField(max_length=1, choices=BOOKING_STATES, default='P')

    def get_duration(self):
        pass

    def get_total_price(self):
        pass
