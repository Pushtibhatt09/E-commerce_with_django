from django.shortcuts import render, redirect
from base.models import Product, Category, Review
from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg
from base.models import Wishlist



class HomeView(ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.order_by('-rating')[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context.update({
            'reviews': product.reviews.filter(is_approved=True),
            'avg_rating': product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0,
            'in_wishlist': self.request.user.is_authenticated and Wishlist.objects.filter(user=self.request.user,
                                                                                          product=product).exists(),
            'review_submitted': self.request.GET.get('review_submitted', False)
        })
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        product = self.get_object()
        Review.objects.update_or_create(
            user=request.user, product=product,
            defaults={
                'rating': request.POST.get('rating', 0),
                'comment': request.POST.get('comment', '').strip(),
                'is_approved': False
            }
        )
        return redirect(f'product_detail/{product.pk}?review_submitted=True')
