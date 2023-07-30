from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics as api_views
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from DroneBoxExpressApp.Operational.serializers import RoutesSerializer
from DroneBoxExpressApp.Operational.models import RoutesModel, DroneModel, AirportModel, FlightModel
from DroneBoxExpressApp.Operational.forms import AirportCreateForm, DroneCreateForm, RouteCreateForm
from DroneBoxExpressApp.Operational.forms import AirportEditForm, DroneEditForm, FlightCompleteForm
from DroneBoxExpressApp.UserAccount.models import DroneBoxProfile


class OperationalView(LoginRequiredMixin, views.TemplateView):
    template_name = "Operational/operational_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
                context["profile"] = profile
                if profile:
                    pilot_flights = FlightModel.objects.filter(drone_operator=profile)
                    routes = RoutesModel.objects.all()
                    airports = AirportModel.objects.all()
                    drones = DroneModel.objects.all()
                    context["pilot_flights"] = pilot_flights
                    context["routes"] = routes
                    context["airports"] = airports
                    context["drones"] = drones
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
            except Http404:
                return redirect("Access-Denied-Page")
            if profile.profile_type != "Pilot":
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class CreateAirportView(LoginRequiredMixin, views.CreateView):
    model = AirportModel
    form_class = AirportCreateForm
    template_name = "Operational/airport_create_page.html"
    success_url = reverse_lazy("Operations-Page")

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
            except Http404:
                return redirect("Access-Denied-Page")
            if profile.profile_type != "Pilot":
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class EditAirportView(LoginRequiredMixin, views.UpdateView):
    model = AirportModel
    form_class = AirportEditForm
    template_name = "Operational/airport_edit_page.html"
    success_url = reverse_lazy("Operations-Page")

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
            except Http404:
                return redirect("Access-Denied-Page")
            if profile.profile_type != "Pilot":
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class CreateDroneView(LoginRequiredMixin, views.CreateView):
    model = DroneModel
    form_class = DroneCreateForm
    template_name = "Operational/drone_create_page.html"
    success_url = reverse_lazy("Operations-Page")

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
            except Http404:
                return redirect("Access-Denied-Page")
            if profile.profile_type != "Pilot":
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class EditDroneView(LoginRequiredMixin, views.UpdateView):
    model = DroneModel
    form_class = DroneEditForm
    template_name = "Operational/drone_edit_page.html"
    success_url = reverse_lazy("Operations-Page")

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
            except Http404:
                return redirect("Access-Denied-Page")
            if profile.profile_type != "Pilot":
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class CreateRouteView(LoginRequiredMixin, views.CreateView):
    model = RoutesModel
    form_class = RouteCreateForm
    template_name = "Operational/route_create_page.html"
    success_url = reverse_lazy("Operations-Page")

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
            except Http404:
                return redirect("Access-Denied-Page")
            if profile.profile_type != "Pilot":
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class EditRouteView(LoginRequiredMixin, views.UpdateView):
    model = RoutesModel
    form_class = RouteCreateForm
    template_name = "Operational/route_create_page.html"
    success_url = reverse_lazy("Operations-Page")

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
            except Http404:
                return redirect("Access-Denied-Page")
            if profile.profile_type != "Pilot":
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class DeleteRouteView(LoginRequiredMixin, views.DeleteView):
    model = RoutesModel
    template_name = "Operational/route_delete_page.html"
    success_url = reverse_lazy("Operations-Page")

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
            except Http404:
                return redirect("Access-Denied-Page")
            if profile.profile_type != "Pilot":
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class DetailsRouteRESTView(api_views.RetrieveAPIView):
    serializer_class = RoutesSerializer
    queryset = RoutesModel.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'pk'


class EditFlightsView(LoginRequiredMixin, views.UpdateView):
    model = FlightModel
    form_class = FlightCompleteForm
    template_name = "Operational/flight_compelte_page.html"
    success_url = reverse_lazy("Operations-Page")

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
                flight = get_object_or_404(FlightModel, pk=self.kwargs["pk"])
            except Http404:
                return redirect("Access-Denied-Page")
            if profile.profile_type != "Pilot":
                return redirect("Access-Denied-Page")
            if flight.drone_operator != profile:
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class DeleteFlightsView(LoginRequiredMixin, views.DeleteView):
    model = FlightModel
    template_name = "Operational/flight_canncellation_page.html"
    success_url = reverse_lazy("Operations-Page")

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
                flight = get_object_or_404(FlightModel, pk=self.kwargs["pk"])
            except Http404:
                return redirect("Access-Denied-Page")
            if profile.profile_type != "Pilot":
                return redirect("Access-Denied-Page")
            if flight.drone_operator != profile:
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)
