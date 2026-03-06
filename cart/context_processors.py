from .models import Cart, Wishlist
def count(request):
    cart_count = 0
    wishlist_count = 0
    if request.user.is_authenticated:
        u=request.user
        cart_items = Cart.objects.filter(user=u)
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_count = Wishlist.objects.filter(user=u).count()
    return {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    }