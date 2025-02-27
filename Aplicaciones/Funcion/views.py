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