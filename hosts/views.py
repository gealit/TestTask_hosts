from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from hosts.models import Host


class HomeView(LoginRequiredMixin, ListView):
    model = Host
    template_name = 'hosts/home.html'
    context_object_name = 'hosts'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        if self.request.user.is_staff:
            return Host.objects.all()
        return Host.objects.filter(users=self.request.user)


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    next_page = 'home'
    template_name = 'hosts/login.html'


class RegisterUserView(CreateView):
    form_class = UserCreationForm
    template_name = 'hosts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')


class HostCreateView(LoginRequiredMixin, CreateView):
    model = Host
    fields = ('ip_address', 'port', 'resource')
    template_name = 'hosts/host_create.html'
    success_url = reverse_lazy('home')
    raise_exception = True

    def form_valid(self, form):
        ip_address = form.cleaned_data['ip_address']
        port = form.cleaned_data['port']
        resource = form.cleaned_data['resource']
        instance = Host.objects.create(ip_address=ip_address, port=port, resource=resource)
        instance.users.add(self.request.user)
        return HttpResponseRedirect(self.success_url)


class HostUpdateView(LoginRequiredMixin, UpdateView):
    model = Host
    fields = ['ip_address', 'port', 'resource']
    template_name = 'hosts/host_update.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'pk'
    raise_exception = True

    def get_object(self, queryset=None):
        obj = super(HostUpdateView, self).get_object()
        if not self.request.user in obj.users.all() and not self.request.user.is_staff:
            raise Http404
        return obj


class HostUpdateAdminView(LoginRequiredMixin, UpdateView):
    model = Host
    fields = ['users', 'ip_address', 'port', 'resource']
    template_name = 'hosts/host_update_admin.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'pk'
    raise_exception = True

    def get_object(self, queryset=None):
        obj = super(HostUpdateAdminView, self).get_object()
        if not self.request.user.is_staff:
            raise Http404
        return obj


class HostDeleteView(LoginRequiredMixin, DeleteView):
    model = Host
    template_name = 'hosts/host_delete.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('home')
    raise_exception = True

    def get_object(self, queryset=None):
        obj = super(HostDeleteView, self).get_object()
        if not self.request.user in obj.users.all() and not self.request.user.is_staff:
            raise Http404
        return obj
