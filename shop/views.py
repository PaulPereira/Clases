from django.shortcuts import render, redirect
from django.db.models import Sum, Avg, Count
from django.core.paginator import Paginator # <-- ASEGÚRATE DE QUE ESTA LÍNEA ESTÉ ARRIBA
from shop.models import WebUser, Producto, Transaccion, Cliente, Proveedor

def index(request):
    productos = Producto.objects.all()[:4]
    return render(request, 'shop/index.html', {'productos': productos})

def productos(request):
    lista_productos = Producto.objects.all().order_by('id')
    
    # Cambiamos aquí a 10 elementos por página
    paginator = Paginator(lista_productos, 10) 
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'shop/productos.html', {'page_obj': page_obj})

def ofertas(request):
    productos_oferta = Producto.objects.filter(es_oferta=True)
    return render(request, 'shop/ofertas.html', {'productos': productos_oferta})

def contacto(request):
    return render(request, 'shop/contacto.html')

def dashboard(request):
    username = request.session.get('admin_user', 'Administrador')
    seccion = request.GET.get('seccion', '')
    
    context = {
        'username': username,
        'seccion': seccion,
    }

    if seccion == 'inventario':
        context['datos'] = Producto.objects.all()
    elif seccion == 'usuarios':
        context['datos'] = WebUser.objects.all()
    elif seccion == 'clientes':
        context['datos'] = Cliente.objects.all()
    elif seccion == 'proveedores':
        context['datos'] = Proveedor.objects.all()
    elif seccion == 'transacciones':
        context['datos'] = Transaccion.objects.all().order_by('-id')
        total_ingresos = Transaccion.objects.aggregate(Sum('total'))['total__sum'] or 0
        ticket_medio = Transaccion.objects.aggregate(Avg('total'))['total__avg'] or 0
        
        context['total_ingresos'] = round(total_ingresos, 2)
        context['ticket_medio'] = round(ticket_medio, 2)
        context['total_pedidos'] = Transaccion.objects.count()

    # CRÍTICO: Esta línea debe estar alineada AQUÍ, fuera de cualquier bloque 'if' o 'elif'
    return render(request, 'shop/dashboard.html', context) 

# Vista del administrador (Se mantiene igual de vulnerable)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def administrator(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        query = f"SELECT * FROM shop_webuser WHERE username = '{username}' AND password = '{password}'"
        try:
            user_match = list(WebUser.objects.raw(query))
            if len(user_match) > 0:
                request.session['admin_user'] = user_match[0].username
                return redirect('dashboard')
            else:
                message = "Credenciales incorrectas."
        except Exception as e:
            message = f"Error en la consulta: {str(e)}"
    return render(request, 'shop/administrator.html', {'message': message})