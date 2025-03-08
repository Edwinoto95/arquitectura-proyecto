from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm

# Función para verificar si el usuario está autenticado
def check_auth(request):
    return request.session.get('authenticated', False)

# Vista de login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == 'admin' and password == 'admin123':
            request.session['authenticated'] = True
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

# Vista de logout
def logout(request):
    if 'authenticated' in request.session:
        del request.session['authenticated']
    return redirect('login')

# Vista de inicio (protegida)
def inicio(request):
    if not check_auth(request):
        return redirect('login')
    
    total_clientes = Cliente.objects.count()
    
    contexto = {
        'total_clientes': total_clientes,
    }
    
    return render(request, 'inicio.html', contexto)

# VISTAS PARA CLIENTES (todas protegidas)
def lista_clientes(request):
    if not check_auth(request):
        return redirect('login')
    
    clientes = Cliente.objects.all()
    return render(request, 'lista_clientes.html', {'clientes': clientes})

def cliente_form(request, id=0):
    if not check_auth(request):
        return redirect('login')
    
    if request.method == "GET":
        if id == 0:  # Es un nuevo cliente
            form = ClienteForm()
        else:  # Es edición de cliente existente
            cliente = get_object_or_404(Cliente, pk=id)
            form = ClienteForm(instance=cliente)
        return render(request, 'cliente_form.html', {'form': form})
    else:  # POST
        if id == 0:  # Crear nuevo
            form = ClienteForm(request.POST)
            mensaje = 'Cliente añadido correctamente.'
        else:  # Actualizar existente
            cliente = get_object_or_404(Cliente, pk=id)
            form = ClienteForm(request.POST, instance=cliente)
            mensaje = 'Cliente actualizado correctamente.'
        
        if form.is_valid():
            form.save()
            messages.success(request, mensaje)
            return redirect('lista_clientes')
        
        return render(request, 'cliente_form.html', {'form': form})

def eliminar_cliente(request, id):
    if not check_auth(request):
        return redirect('login')
    
    cliente = get_object_or_404(Cliente, pk=id)
    cliente.delete()
    messages.success(request, 'Cliente eliminado correctamente.')
    return redirect('lista_clientes')





from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Proyecto, Cliente
from .forms import ProyectoForm

# Vistas para Proyecto
class ProyectoListView(ListView):
    model = Proyecto
    template_name = 'proyecto_list.html'
    context_object_name = 'proyectos'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        cliente_id = self.request.GET.get('cliente')
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        return queryset

class ProyectoDetailView(DetailView):
    model = Proyecto
    template_name = 'proyecto_detail.html'
    context_object_name = 'proyecto'

class ProyectoCreateView(CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyecto_form.html'
    success_url = reverse_lazy('proyecto_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Proyecto creado correctamente.')
        return super().form_valid(form)

class ProyectoUpdateView(UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyecto_form.html'
    
    def get_success_url(self):
        return reverse_lazy('proyecto_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Proyecto actualizado correctamente.')
        return super().form_valid(form)

class ProyectoDeleteView(DeleteView):
    model = Proyecto
    template_name = 'proyecto_confirm_delete.html'
    success_url = reverse_lazy('proyecto_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Proyecto eliminado correctamente.')
        return super().delete(request, *args, **kwargs)
