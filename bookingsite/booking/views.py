from django.shortcuts import redirect, render, get_object_or_404
from django.http import  HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .forms import *
from .models import *
from .utils import DataMixin
from .filters import *
from django_filters.views import FilterView


class IndexFilterView(DataMixin, FilterView):
        template_name = 'booking/index.html'
        context_object_name = 'offers'
        paginate_by = 2

        def get_queryset(self):
            return Offer.objects.filter(isPublished=True).order_by('-date_created')

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            c_def = self.get_user_context(title='Booking service')
            context = dict(list(context.items()) + list(c_def.items()))
            return context

class CreateBookingView(LoginRequiredMixin, DataMixin,  generic.DetailView):
    model = Offer
    template_name = 'booking/book.html'
    login_url = 'booking:sign_in'

    def get_queryset(self):
        return Offer.objects.filter(isPublished=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Book: ' + self.object.name
        form = BookingForm()
        c_def = self.get_user_context(title=title, form=form)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def post(self,request,slug):
        # request.POST['offer'] = self.object.pk
        post = request.POST.copy()
        post['user'] = request.user.pk
        post['state'] = Booking.BOOKING_STATES[0][0]
        request.POST = post
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking:profile')
        return redirect(request.META['HTTP_REFERER'])

class OfferDetailView(DataMixin, generic.DetailView):
    model = Offer
    template_name = 'booking/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=self.object.name)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Offer.objects.filter(isPublished=True)


class RegisterUser(DataMixin, generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'booking/user-auth.html'
    success_url = reverse_lazy('booking:sign_in')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('booking:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Sign up'
        c_def = self.get_user_context(title=title, menu_item_selected=title)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'booking/user-auth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Sign in'
        c_def = self.get_user_context(title=title, menu_item_selected= title)
        context = dict(list(context.items()) + list(c_def.items()))
        return context




def logout_view(request):
    logout(request)
    return redirect('booking:index')

def delete_booking_view(request, pk):
    if request.user.is_authenticated:
        booking = Booking.objects.get(pk=pk)
        if booking and booking.user.pk is request.user.pk:
            if booking.state == Booking.BOOKING_STATES[0][0] and not booking.is_past_due():
                booking.delete()
    return redirect('booking:profile')

class ProfileView (LoginRequiredMixin,DataMixin, generic.ListView):
    login_url = 'booking:sign_in'
    template_name = 'booking/profile.html'
    context_object_name = 'bookings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Profile'
        c_def = self.get_user_context(title=title, menu_item_selected=title)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Booking.objects.filter(user__pk=self.request.user.pk).order_by('-pk')

