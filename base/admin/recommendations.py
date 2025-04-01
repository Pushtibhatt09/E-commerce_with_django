from django.contrib import admin
from base.models import Recommendation, RecommendedProduct, ProductView


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'show_products')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

    def show_products(self, obj):
        products = obj.products.order_by('-score')[:3]
        if not products:
            return "No recommendations yet"
        return ", ".join(f"{p.product.name} ({p.score:.2f})" for p in products)

    show_products.short_description = 'Top Recommendations'


@admin.register(RecommendedProduct)
class RecommendedProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'recommendation', 'score')
    list_filter = ('recommendation__user', 'score')
    search_fields = ('product__name',)
    readonly_fields = ('product', 'recommendation', 'score')
    ordering = ('-score',)


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user_info', 'viewed_at')
    list_filter = ('product', 'viewed_at')
    search_fields = ('product__name', 'user__username')
    readonly_fields = ('viewed_at', 'ip_address', 'session_id')

    def user_info(self, obj):
        return obj.user.username if obj.user else f"Anonymous ({obj.ip_address})"

    user_info.short_description = 'User'