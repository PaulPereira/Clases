import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vuln_shop.settings')
django.setup()

from shop.models import Producto, WebUser, Transaccion, Cliente, Proveedor

def poblar_base_de_datos():
    print("=" * 60)
    print("[+] LIMPIANDO REGISTROS ANTIGUOS...")
    Proveedor.objects.all().delete()
    Cliente.objects.all().delete()
    Transaccion.objects.all().delete()
    Producto.objects.all().delete()
    WebUser.objects.all().delete()

    # Superusuario y Administradores
    WebUser.objects.create(username="bart", password="SuperPassword123", tipo="admin")
    WebUser.objects.create(username="admin_sara", password="SaraAdminSecure2026", tipo="admin")
    WebUser.objects.create(username="admin_carlos", password="CarlosManagerControl!", tipo="admin")

    # Usuarios comunes
    for i in range(1, 8):
        WebUser.objects.create(username=f"usuario_{i}", password=f"pass_comun_{i}", tipo="cliente")

    print("[+] GENERANDO 50 PRODUCTOS DINÁMICOS...")
    categorias = [
        ("Portátiles", "fa-laptop"), 
        ("Smartphones", "fa-mobile-screen-button"), 
        ("Audio", "fa-headphones")
    ]
    productos_creados = []
    
    for i in range(1, 51):
        cat, icono = random.choice(categorias)
        precio_base = round(random.uniform(19.99, 999.99), 2)
        
        # CORRECCIÓN: Volvemos a activar la probabilidad de ofertas (20% de los productos)
        es_oferta = random.choice([True, False, False, False, False])
        precio_oferta = round(precio_base * 0.75, 2) if es_oferta else None # 25% de descuento
        
        p = Producto.objects.create(
            nombre=f"Gadget Pro X{i}", 
            categoria=cat, 
            precio=precio_base, 
            descripcion=f"Dispositivo tecnológico de última generación. Modelo Gadget Pro X{i}.",
            icono=icono,
            es_oferta=es_oferta,      # <-- Añadido de nuevo
            precio_oferta=precio_oferta # <-- Añadido de nuevo
        )
        productos_creados.append(p)
    print(f"    -> {Producto.objects.count()} productos añadidos con sus respectivos estados de oferta.")

    print("[+] GENERANDO 250 TRANSACCIONES...")
    for i in range(1, 251):
        prod = random.choice(productos_creados)
        total_pago = prod.precio_oferta if prod.es_oferta else prod.precio
        Transaccion.objects.create(
            id_pedido=f"#TG{10000 + i}",
            cliente=f"Comprador Aleatorio {random.randint(1, 50)}",
            producto=prod,
            total=total_pago
        )

    print("[+] GENERANDO 100 CLIENTES CON DATOS BANCARIOS...")
    nombres = ["Juan", "María", "Carlos", "Ana", "Luis", "Elena", "Pedro", "Lucía", "David", "Sofia"]
    apellidos = ["Pérez", "Gómez", "Mendoza", "Rodríguez", "Martínez", "García", "Sánchez", "López"]
    calles = ["Gran Vía", "Av. de la Constitución", "Calle Mayor", "Paseo de la Castellana"]
    ciudades = ["Madrid", "Barcelona", "Valencia", "Sevilla"]

    for i in range(1, 101):
        nom = random.choice(nombres)
        ape = random.choice(apellidos)
        Cliente.objects.create(
            nombre=nom,
            apellidos=f"{ape} {random.choice(apellidos)}",
            email=f"{nom.lower()}.{ape.lower()}{i}@example.com",
            direccion_facturacion=f"{random.choice(calles)}, {random.randint(1, 150)}, {random.choice(ciudades)}",
            numero_tarjeta=f"{random.randint(4000, 4999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            fecha_vencimiento=f"{random.randint(1, 12):02d}/{random.randint(26, 32)}",
            cvv=f"{random.randint(100, 999)}"
        )

    print("[+] GENERANDO 25 PROVEEDORES LOGÍSTICOS...")
    empresas = ["TechDistribuciones", "Global Gadgets Sl", "Logística Asia-Europa", "Importaciones Microchip"]
    for i in range(1, 26):
        emp = f"{random.choice(empresas)} #{i}"
        Proveedor.objects.create(
            empresa=emp,
            contacto_nombre=f"{random.choice(nombres)} {random.choice(apellidos)}",
            telefono=f"+34 6{random.randint(10000000, 99999999)}",
            email_corporativo=f"info@{emp.lower().replace(' ', '')}.com",
            direccion_fiscal=f"Polígono Industrial {random.choice(apellidos)}, Nave {i}, {random.choice(ciudades)}",
            cuenta_bancaria_iban=f"ES21 {random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}"
        )
    print("=" * 60)
    print("¡ENTORNO GENERAL INICIALIZADO COMPLETAMENTE CON TODAS LAS VARIABLES!")
    print("=" * 60)

if __name__ == '__main__':
    poblar_base_de_datos()