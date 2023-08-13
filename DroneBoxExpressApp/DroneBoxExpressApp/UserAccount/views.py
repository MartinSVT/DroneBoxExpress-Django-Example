from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views import generic as views
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views, login
from django.contrib.auth.mixins import LoginRequiredMixin
from DroneBoxExpressApp.UserAccount.models import DroneBoxProfile
from DroneBoxExpressApp.UserAccount.forms import DroneBoxUserCreationForm, DroneBoxLoginForm, DroneBoxProfileEditForm

UserModel = get_user_model()


class UserRegisterView(views.CreateView):
    model = UserModel
    form_class = DroneBoxUserCreationForm
    template_name = 'UserAccount/register_template.html'
    success_url = reverse_lazy('Home-Page')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = "Not Logged In"
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(auth_views.LoginView):
    form_class = DroneBoxLoginForm
    template_name = 'UserAccount/login_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = "Not Logged In"
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class UserLogoutView(LoginRequiredMixin, auth_views.LogoutView):
    template_name = "UserAccount/logout_template.html"

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


class ProfileDetailsView(LoginRequiredMixin, views.DetailView):
    model = DroneBoxProfile
    template_name = "UserAccount/profile_template.html"

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
            if kwargs.get('pk') != self.request.user.pk:
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class ProfileEdithView(LoginRequiredMixin, views.UpdateView):
    model = DroneBoxProfile
    template_name = "UserAccount/profile_edit_template.html"
    form_class = DroneBoxProfileEditForm

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

    def get_success_url(self):
        temp_pk = self.kwargs['pk']
        return reverse_lazy("Profile-Details", kwargs={'pk': temp_pk})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        else:
            if kwargs.get('pk') != self.request.user.pk:
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class ProfileDeleteView(LoginRequiredMixin, views.DeleteView):
    model = DroneBoxProfile
    template_name = "UserAccount/profile_delete_template.html"
    success_url = reverse_lazy("Home-Page")

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
            if kwargs.get('pk') != self.request.user.pk:
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)
