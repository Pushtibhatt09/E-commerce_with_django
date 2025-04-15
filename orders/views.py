from django.views.generic import ListView, DetailView, View, TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from base.models import Order


class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CancelOrderView(View):
    @staticmethod
    def post(request, pk):
        if not request.user.is_authenticated:
            return redirect('login')

        order = get_object_or_404(Order, pk=pk, user=request.user)

        if order.status in ['pending', 'processing']:
            order.status = 'cancelled'
            order.save()
            messages.success(request, f"Order #{order.id} has been cancelled.")
        else:
            messages.warning(request, "This order cannot be cancelled.")

        return redirect('order_list')


class TrackOrderView(TemplateView):
    template_name = 'orders/track_order.html'

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get("order_id")
        order = Order.objects.filter(id=order_id).first()
        context = self.get_context_data(order=order)
        return self.render_to_response(context)
