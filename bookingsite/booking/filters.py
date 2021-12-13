from django_filters import FilterSet, CharFilter, RangeFilter, BooleanFilter, OrderingFilter, MultipleChoiceFilter
from .models import Offer


class OfferFilter(FilterSet):
    o = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('date_created', 'date_created'),
            ('night_price', 'night_price'),
        )
    )
    name = CharFilter(lookup_expr='icontains')
    night_price = RangeFilter()
    isConditioner = BooleanFilter()
    isWifi = BooleanFilter()
    isKitchen = BooleanFilter()
    isBreakfast = BooleanFilter()
    lodging_type = MultipleChoiceFilter(choices=Offer.LODGING_TYPES)

    class Meta:
        model = Offer
        fields = ['name','night_price', 'isConditioner', 'isWifi', 'isBreakfast', 'isKitchen', 'places', 'lodging_type']