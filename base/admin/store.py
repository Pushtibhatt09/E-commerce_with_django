from django.contrib import admin
from django.utils.html import format_html
from base.models import Store, Category, Product, ProductImage, Review


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'owner__username')
    raw_id_fields = ('owner',)
    date_hierarchy = 'created_at'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'name': ('name',)}
    date_hierarchy = 'created_at'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "-"

    image_preview.short_description = 'Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'rating', 'created_at')
    list_filter = ('category', 'rating', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock')
    raw_id_fields = ('category',)
    inlines = [ProductImageInline]
    date_hierarchy = 'created_at'
    actions = ['update_ratings']

    def update_ratings(self, request, queryset):
        for product in queryset:
            product.update_rating()
        self.message_user(request, f"Updated ratings for {queryset.count()} products")

    update_ratings.short_description = "Update selected product ratings"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'image_preview')
    list_editable = ('is_primary',)
    list_filter = ('is_primary',)
    raw_id_fields = ('product',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "-"

    image_preview.short_description = 'Preview'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    list_editable = ('is_approved',)
    raw_id_fields = ('product', 'user')
    date_hierarchy = 'created_at'
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"Approved {queryset.count()} reviews")

    approve_reviews.short_description = "Approve selected reviews"