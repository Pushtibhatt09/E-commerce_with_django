from django.views.generic import TemplateView, DetailView
from base.models import Product, Category, OrderItem


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        trending_products = Product.objects.filter(trending=True)[:10]
        discounted_products = Product.objects.exclude(discount__isnull=True).exclude(discount=0)[:10]
        featured_products = Product.objects.filter(featured=True)[:10]
        new_arrivals = Product.objects.order_by('-created_at')[:10]
        categories = Category.objects.all()

        recently_viewed = []
        if self.request.user.is_authenticated:
            recently_viewed = self.request.session.get('recently_viewed', [])

        personalized_picks = []
        if self.request.user.is_authenticated and OrderItem.objects.filter(order__user=self.request.user).exists():
            personalized_picks = Product.objects.filter(
                category__products__in=OrderItem.objects.filter(
                    order__user=self.request.user
                ).values_list('product', flat=True)
            ).distinct()[:10]

        most_buys = Product.objects.filter(orderitem__isnull=False).distinct()[:10]
        festive_specials = Product.objects.filter(category__name__icontains='festive')[:10]

        context.update({
            'trending_products': trending_products,
            'discounted_products': discounted_products,
            'featured_products': featured_products,
            'new_arrivals': new_arrivals,
            'categories': categories,
            'recently_viewed': Product.objects.filter(id__in=recently_viewed),
            'personalized_picks': personalized_picks,
            'most_buys': most_buys,
            'festive_specials': festive_specials,
        })
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get(self, request, *args, **kwargs):
        product = self.get_object()

        if request.user.is_authenticated:
            recently_viewed = request.session.get('recently_viewed', [])
            if product.id not in recently_viewed:
                recently_viewed.insert(0, product.id)
            request.session['recently_viewed'] = recently_viewed[:10]

        return super().get(request, *args, **kwargs)
