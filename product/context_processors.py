from django.db.models import Sum
from .models import CartItem
from .views import get_current_user

def cart_count(request):

    user = get_current_user(request)
    count = CartItem.objects.filter(user=user).aggregate(total=Sum('quantity'))['total']

    if count is None:
        count = 0

    return {'cart_count': count}