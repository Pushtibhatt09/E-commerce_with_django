from django.shortcuts import render
from base.models import Product, Category
from base.models import OrderItem

def home(request):
    trending_products = Product.objects.filter(trending=True)[:10]
    discounted_products = Product.objects.exclude(discount__isnull=True).exclude(discount=0)[:10]
    featured_products = Product.objects.filter(featured=True)[:10]
    new_arrivals = Product.objects.order_by('-created_at')[:10]
    categories = Category.objects.all()

    recently_viewed = []
    if request.user.is_authenticated:
        recently_viewed = request.session.get('recently_viewed', [])

    personalized_picks = []
    if request.user.is_authenticated:
        user_orders = OrderItem.objects.filter(order__user=request.user).values_list('product_id', flat=True)
        if user_orders:
            personalized_picks = Product.objects.filter(category__products__id__in=user_orders).distinct()[:10]
    most_buys = Product.objects.filter(orderitem__isnull=False).distinct()[:10]
    festive_specials = Product.objects.filter(category__name__icontains='festive')[:10]

    context = {
        'trending_products': trending_products,
        'discounted_products': discounted_products,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'recently_viewed': Product.objects.filter(id__in=recently_viewed),
        'personalized_picks': personalized_picks,
        'most_buys': most_buys,
        'festive_specials': festive_specials,
    }

    return render(request, 'store/home.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        recently_viewed = request.session.get('recently_viewed', [])
        if product_id not in recently_viewed:
            recently_viewed.insert(0, product_id)
        request.session['recently_viewed'] = recently_viewed[:10]

    return render(request, 'store/product_detail.html', {'product': product})

