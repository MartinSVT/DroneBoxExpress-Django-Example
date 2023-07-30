from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics as api_views
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from DroneBoxExpressApp.Commercial.models import PricesModel, OrdersModel, DiscountsModel
from DroneBoxExpressApp.Commercial.serializers import PricesSerializer, DiscountsSerializer
from DroneBoxExpressApp.Commercial.forms import OrderCreateForm
from DroneBoxExpressApp.UserAccount.models import DroneBoxProfile


class OrdersView(LoginRequiredMixin, views.ListView):
    template_name = "Commercial/orders_page.html"
    model = OrdersModel

    def get_queryset(self, *args, **kwargs):
        return OrdersModel.objects.filter(order_profile_id=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
                context["profile"] = profile
            except Http404:
                context["profile"] = "Not Logged In"
        else:
            context["profile"] = "Not Logged In"
        return context


class CreateOrderView(LoginRequiredMixin, views.CreateView):
    model = OrdersModel
    form_class = OrderCreateForm
    template_name = "Commercial/order_create_page.html"
    success_url = reverse_lazy("Orders-Page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
                revenue = profile.total_revenue
                profile_type = profile.profile_type
                context["profile"] = profile
                context["revenue"] = revenue
                context["profile_type"] = profile_type
            except Http404:
                context["profile"] = "Not Logged In"
        else:
            context["profile"] = "Not Logged In"
        return context

    def form_valid(self, form):
        form_instance = form.instance
        try:
            temp_profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
        except Http404:
            return redirect("Access-Denied-Page")
        form_instance.order_profile = temp_profile
        form_instance.save()
        return super().form_valid(form)


class DetailsOrderView(LoginRequiredMixin, views.DetailView):
    model = OrdersModel
    template_name = "Commercial/order_details_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
                context["profile"] = profile
            except Http404:
                context["profile"] = "Not Logged In"
        else:
            context["profile"] = "Not Logged In"
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        else:
            try:
                profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
                order = get_object_or_404(OrdersModel, pk=self.kwargs["pk"])
            except Http404:
                return redirect("Access-Denied-Page")
            if profile != order.order_profile:
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class DeleteOrderView(LoginRequiredMixin, views.DeleteView):
    model = OrdersModel
    template_name = "Commercial/order_delete_page.html"
    success_url = reverse_lazy("Orders-Page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
                context["profile"] = profile
            except Http404:
                context["profile"] = "Not Logged In"
        else:
            context["profile"] = "Not Logged In"
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        else:
            try:
                profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
                order = get_object_or_404(OrdersModel, pk=self.kwargs["pk"])
            except Http404:
                return redirect("Access-Denied-Page")
            if profile != order.order_profile:
                return redirect("Access-Denied-Page")
            if order.order_status != "Pending":
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class UpdateOrderView(LoginRequiredMixin, views.UpdateView):
    model = OrdersModel
    template_name = "Commercial/order_create_page.html"
    form_class = OrderCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
                revenue = profile.total_revenue
                profile_type = profile.profile_type
                context["profile"] = profile
                context["revenue"] = revenue
                context["profile_type"] = profile_type
            except Http404:
                context["profile"] = "Not Logged In"
        else:
            context["profile"] = "Not Logged In"
        return context

    def get_success_url(self):
        temp_pk = self.kwargs['pk']
        return reverse_lazy("Details-Order-Page", kwargs={'pk': temp_pk})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        else:
            try:
                profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
                order = get_object_or_404(OrdersModel, pk=self.kwargs["pk"])
            except Http404:
                return redirect("Access-Denied-Page")
            if profile != order.order_profile:
                return redirect("Access-Denied-Page")
            if order.order_status != "Pending":
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


# Django REST Create and List View for PriceModel
class PricesListCreateView(api_views.ListCreateAPIView):
    queryset = PricesModel.objects.all()
    serializer_class = PricesSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


# Django REST Details,Update,Delete view for PriceModel
class PricesUpdateDeleteView(api_views.RetrieveUpdateDestroyAPIView):
    serializer_class = PricesSerializer
    queryset = PricesModel.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_url_kwarg = 'pk'


# Django REST Create and List View for DiscountsModel
class DiscountsListCreateView(api_views.ListCreateAPIView):
    queryset = DiscountsModel.objects.all()
    serializer_class = DiscountsSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


# Django REST Details,Update,Delete view for DiscountsModel
class DiscountsUpdateDeleteView(api_views.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscountsSerializer
    queryset = DiscountsModel.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_url_kwarg = 'pk'
