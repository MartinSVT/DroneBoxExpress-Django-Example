from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic as views
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from DroneBoxExpressApp.UserAccount.models import DroneBoxProfile
from DroneBoxExpressApp.Common.models import NewsModel
from DroneBoxExpressApp.Common.forms import NewsAddForm


class AccessDeniedView(views.TemplateView):
    template_name = 'not_authorized.html'

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


class HomeView(views.TemplateView):
    template_name = 'Common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = NewsModel.objects.all()
        context["articles"] = articles
        if self.request.user.is_authenticated:
            try:
                profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
                context["profile"] = profile
            except Http404:
                context["profile"] = "Not Logged In"
        else:
            context["profile"] = "Not Logged In"
        return context


class NewsCreateView(LoginRequiredMixin, views.CreateView):
    model = NewsModel
    form_class = NewsAddForm
    template_name = "Common/create_article_page.html"
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

    def form_valid(self, form):
        form_instance = form.instance
        try:
            profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
        except Http404:
            return redirect("Access-Denied-Page")
        form_instance.article_author = profile.get_custom_name()
        form_instance.article_author_key = profile.pk
        form_instance.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        else:
            try:
                profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
            except Http404:
                return redirect("Access-Denied-Page")
            if profile.profile_type != "Editor":
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class NewsEditView(LoginRequiredMixin, views.UpdateView):
    model = NewsModel
    template_name = "Common/create_article_page.html"
    form_class = NewsAddForm
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
            try:
                profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
                article = get_object_or_404(NewsModel, pk=self.kwargs["pk"])
            except Http404:
                return redirect("Access-Denied-Page")
            if profile.profile_type != "Editor":
                return redirect("Access-Denied-Page")
            if article.article_author_key != profile.pk:
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class NewsDeleteView(LoginRequiredMixin, views.DeleteView):
    model = NewsModel
    template_name = "Common/delete_article_page.html"
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
            try:
                profile = get_object_or_404(DroneBoxProfile, pk=self.request.user.pk)
                article = get_object_or_404(NewsModel, pk=self.kwargs["pk"])
            except Http404:
                return redirect("Access-Denied-Page")
            if profile.profile_type != "Editor":
                return redirect("Access-Denied-Page")
            if article.article_author_key != profile.pk:
                return redirect("Access-Denied-Page")
        return super().dispatch(request, *args, **kwargs)


class ContactsView(views.TemplateView):
    template_name = "Common/contact_page.html"

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


class AboutUsView(views.TemplateView):
    template_name = "Common/about_us_page.html"

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
