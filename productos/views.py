from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from .forms import UserRegisterForm, ProductoForm
from .models import Producto


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "ingresaste correctamente")
            return redirect('home')
        else:
            messages.error(request, "usuario o contrasena incorrectos")
            return render(request, 'home.html', {})
    else:
        if request.user.is_authenticated:
            productos = Producto.objects.all().order_by('-fecha_creacion')
            total_productos = productos.count()
            stock_bajo = productos.filter(cantidad__lte=models.F('stock_minimo')).count()
            paginator = Paginator(productos, 10)
            page = request.GET.get('page')
            page_obj = paginator.get_page(page)
            context = {
                'productos': page_obj,
                'total_productos': total_productos,
                'stock_bajo': stock_bajo,
            }
            return render(request, 'home.html', context)
        return render(request, 'home.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "cerraste sesion correctamente")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "registro exitoso")
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def productos_list(request):
    if not request.user.is_authenticated:
        messages.error(request, "debes iniciar sesion")
        return redirect('home')
    productos = Producto.objects.all().order_by('-fecha_creacion')
    paginator = Paginator(productos, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'productos.html', {'productos': page_obj})


def producto_detail(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "debes iniciar sesion")
        return redirect('home')
    producto = get_object_or_404(Producto, id_productos=pk)
    return render(request, 'producto.html', {'producto': producto})


def producto_create(request):
    if not request.user.is_authenticated:
        messages.error(request, "debes iniciar sesion")
        return redirect('home')
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "producto creado correctamente")
            return redirect('productos')
    else:
        form = ProductoForm()
    return render(request, 'producto_form.html', {'form': form, 'titulo': 'Crear producto'})


def producto_update(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "debes iniciar sesion")
        return redirect('home')
    producto = get_object_or_404(Producto, id_productos=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "producto actualizado correctamente")
            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'producto_form.html', {'form': form, 'titulo': 'Editar producto'})


def producto_delete(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "debes iniciar sesion")
        return redirect('home')
    producto = get_object_or_404(Producto, id_productos=pk)
    producto.soft_delete(user_id=request.user.id)
    messages.success(request, "producto eliminado correctamente")
    return redirect('productos')
