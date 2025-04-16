from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from base.models import Product
from base.models import Cart, CartItem, Wishlist, Coupon


def post(request):
    action = request.POST.get('action')
    product_id = request.POST.get('product_id')
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if action == 'update_quantity':
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        item.quantity = max(1, quantity)
        item.save()
        messages.success(request, 'Quantity updated!')

    elif action == 'apply_coupon':
        code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            request.session['coupon_code'] = coupon.code
            messages.success(request, f'Coupon {code} applied!')
        except Coupon.DoesNotExist:
            messages.warning(request, 'Invalid coupon code.')

    elif action == 'remove_coupon':
        request.session.pop('coupon_code', None)
        messages.info(request, 'Coupon removed.')

    elif action == 'save_for_later':
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        Wishlist.objects.get_or_create(user=request.user, product=item.product)
        item.delete()
        messages.info(request, 'Item moved to wishlist.')

    return redirect('cart_summary')


class CartView(View):
    template_name = 'cart/cart_summary.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()
        coupon_code = request.session.get('coupon_code', '')
        discount = 0

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True)
                discount = float(coupon.discount_amount)
            except Coupon.DoesNotExist:
                messages.warning(request, "Invalid coupon.")
                request.session.pop('coupon_code', None)

        total = sum(item.subtotal_price() for item in items)
        final_total = max(total - discount, 0)

        context = {
            'cart': cart,
            'items': items,
            'total': total,
            'discount': discount,
            'final_total': final_total,
            'coupon_code': coupon_code,
        }
        return render(request, self.template_name, context)

