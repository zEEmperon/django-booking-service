import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import *

def create_offer(slug, isPublished=True):
    return Offer.objects.create(slug=slug,isPublished=isPublished)

class IndexFilterViewTests(TestCase):

    def test_no_offers(self):
        response = self.client.get(reverse('booking:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No offers currently available:)")
        self.assertQuerysetEqual(response.context['offers'],[])

    def test_published_offer(self):
        offer = Offer.objects.create(slug = 'a',isPublished=True)
        response = self.client.get(reverse('booking:index'))
        self.assertQuerysetEqual(response.context['offers'],[offer])

    def test_unpublished_offer(self):
        offer = Offer.objects.create(slug='a', isPublished=False)
        response = self.client.get(reverse('booking:index'))
        self.assertQuerysetEqual(response.context['offers'], [])

    def test_published_and_unpublished_offer(self):
        p_offer = Offer.objects.create(slug='a', isPublished=True)
        up_offer = Offer.objects.create(slug='b', isPublished=False)
        response = self.client.get(reverse('booking:index'))
        self.assertQuerysetEqual(response.context['offers'], [p_offer])

class OfferDetailViewTests(TestCase):

    def test_published_offer(self):
        offer = create_offer(slug='a', isPublished=True)
        url = reverse('booking:detail',args=(offer.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unpublished_offer(self):
        offer = create_offer(slug='a', isPublished=False)
        url = reverse('booking:detail',args=(offer.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class BookingModelTests(TestCase):

    def test_is_past_due_with_current_date(self):
        date = timezone.now().date()
        current_date_booking = Booking(arrival_date=date)
        self.assertEqual(current_date_booking.is_past_due(), True)

    def test_is_past_due_with_past_date(self):
        date = timezone.now().date() - datetime.timedelta(days=30)
        past_date_booking = Booking(arrival_date=date)
        self.assertEqual(past_date_booking.is_past_due(), True)

    def test_is_past_due_with_future_date(self):
        date = timezone.now().date() + datetime.timedelta(days=30)
        future_date_booking = Booking(arrival_date=date)
        self.assertEqual(future_date_booking.is_past_due(), False)

    def test_get_total_price(self):
        arrival_date = timezone.now().date()
        departure_date = arrival_date + datetime.timedelta(days=5)
        price = 5
        offer = Offer(night_price=price)
        booking = Booking(arrival_date= arrival_date, departure_date = departure_date, offer=offer)
        self.assertEqual(booking.get_total_price(), 25)

class UserProfileTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='root', password='root')

    def create_offer_and_booking(self, state='P', arrival_date_offset = datetime.timedelta(days=5)):
        arrival_date = timezone.now() + arrival_date_offset
        departure_date = arrival_date + datetime.timedelta(days=5)
        offer = create_offer(slug='a')
        booking = Booking.objects.create(offer=offer, user=self.user,
                                         arrival_date=arrival_date,
                                         departure_date=departure_date, state=state)
        return offer, booking

    def test_bookings_list(self):
        self.client.login(username='root', password='root')
        offer, booking = self.create_offer_and_booking()
        url = reverse('booking:profile')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['bookings'],[booking,])

    def test_bookings_empty_list(self):
        self.client.login(username='root', password='root')
        url = reverse('booking:profile')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['bookings'],[])

    def test_proccessing_booking_delete(self):
        self.client.login(username='root', password='root')
        offer, booking = self.create_offer_and_booking()
        url = reverse('booking:delete_booking', args=(booking.pk,))
        response = self.client.get(url)
        self.assertEqual(Booking.objects.count(), 0)

    def test_accepted_booking_delete(self):
        self.client.login(username='root', password='root')
        offer, booking = self.create_offer_and_booking(state='A')
        url = reverse('booking:delete_booking', args=(booking.pk,))
        response = self.client.get(url)
        self.assertEqual(Booking.objects.count(), 1)

    def test_rejected_booking_delete(self):
        self.client.login(username='root', password='root')
        offer, booking = self.create_offer_and_booking(state='R')
        url = reverse('booking:delete_booking', args=(booking.pk,))
        response = self.client.get(url)
        self.assertEqual(Booking.objects.count(), 1)

    def test_past_booking_delete(self):
        self.client.login(username='root', password='root')
        offer, booking = self.create_offer_and_booking(arrival_date_offset=-datetime.timedelta(days=5))
        url = reverse('booking:delete_booking', args=(booking.pk,))
        response = self.client.get(url)
        self.assertEqual(Booking.objects.count(), 1)

    def test_now_booking_delete(self):
        self.client.login(username='root', password='root')
        offer, booking = self.create_offer_and_booking(arrival_date_offset=datetime.timedelta(days=0))
        url = reverse('booking:delete_booking', args=(booking.pk,))
        response = self.client.get(url)
        self.assertEqual(Booking.objects.count(), 1)

class CreateBookingTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='root', password='root')

    def get_url_and_offer(self, isPublished=True):
        self.client.login(username='root', password='root')
        offer = create_offer(slug='a', isPublished=isPublished)
        url = reverse('booking:book', args=(offer.slug,))
        return url, offer

    def get_arrival_date_and_departure_date_str(self, arrival_date_offset = datetime.timedelta(days=0),
                                                departure_date_offeset = datetime.timedelta(days=5)):
        arrival_date = timezone.now() + arrival_date_offset
        departure_date = arrival_date + departure_date_offeset
        arrival_date = arrival_date.strftime("%Y-%m-%d")
        departure_date = departure_date.strftime("%Y-%m-%d")
        return arrival_date, departure_date

    def test_book_access_published_offer(self):
        url, _ = self.get_url_and_offer()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_book_access_unpublished_offer(self):
        url, _ = self.get_url_and_offer(isPublished=False)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_book_published_offer_valid_fields(self):
        url, offer = self.get_url_and_offer()
        arrival_date, departure_date = self.get_arrival_date_and_departure_date_str(
            arrival_date_offset=datetime.timedelta(days=5))
        payment_method = 'Cash'
        HTTP_REFERER = url
        response = self.client.post(url, {'offer': offer.pk, 'arrival_date' : arrival_date,
                                          'departure_date' : departure_date,
                                          'payment_method' : payment_method}, HTTP_REFERER=HTTP_REFERER)
        self.assertEqual(Booking.objects.count(), 1)

    def test_book_published_offer_arrival_date_in_past(self):
        url, offer = self.get_url_and_offer()
        arrival_date, departure_date = self.get_arrival_date_and_departure_date_str(
            arrival_date_offset=-datetime.timedelta(days=5))
        payment_method = 'Cash'
        HTTP_REFERER = url
        response = self.client.post(url, {'offer': offer.pk, 'arrival_date' : arrival_date,
                                          'departure_date' : departure_date,
                                          'payment_method' : payment_method}, HTTP_REFERER=HTTP_REFERER)
        self.assertEqual(Booking.objects.count(), 0)

    def test_book_published_offer_arrival_date_today(self):
        url, offer = self.get_url_and_offer()
        arrival_date, departure_date = self.get_arrival_date_and_departure_date_str()
        payment_method = 'Cash'
        HTTP_REFERER = url
        response = self.client.post(url, {'offer': offer.pk, 'arrival_date' : arrival_date,
                                          'departure_date' : departure_date,
                                          'payment_method' : payment_method}, HTTP_REFERER=HTTP_REFERER)
        self.assertEqual(Booking.objects.count(), 0)

    def test_book_published_offer_departure_date_earlier_than_arrival_date(self):
        url, offer = self.get_url_and_offer()
        arrival_date, departure_date = self.get_arrival_date_and_departure_date_str(departure_date_offeset=-datetime.timedelta(days=5))
        payment_method = 'Cash'
        HTTP_REFERER = url
        response = self.client.post(url, {'offer': offer.pk, 'arrival_date' : arrival_date,
                                          'departure_date' : departure_date,
                                          'payment_method' : payment_method}, HTTP_REFERER=HTTP_REFERER)
        self.assertEqual(Booking.objects.count(), 0)

    def test_book_published_offer_departure_date_equal_to_arrival_date(self):
        url, offer = self.get_url_and_offer()
        arrival_date, departure_date = self.get_arrival_date_and_departure_date_str(departure_date_offeset=datetime.timedelta(days=0))
        payment_method = 'Cash'
        HTTP_REFERER = url
        response = self.client.post(url, {'offer': offer.pk, 'arrival_date' : arrival_date,
                                          'departure_date' : departure_date,
                                          'payment_method' : payment_method}, HTTP_REFERER=HTTP_REFERER)
        self.assertEqual(Booking.objects.count(), 0)