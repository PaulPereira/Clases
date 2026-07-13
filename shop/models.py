from django.db import models

class WebUser(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('cliente', 'Cliente Común'),
    ]
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    tipo = models.CharField(max_length=15, choices=ROLES, default='cliente') # <-- NUEVO CAMPO

    def __str__(self):
        return f"{self.username} ({self.get_tipo_display()})"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    icono = models.CharField(max_length=50, default="fa-laptop")
    es_oferta = models.BooleanField(default=False)
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Transaccion(models.Model):
    id_pedido = models.CharField(max_length=20, unique=True)
    cliente = models.CharField(max_length=100)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default="Completado")

    def __str__(self):
        return f"{self.id_pedido} - {self.cliente}"

# NUEVO MODELO DE CLIENTES
class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    direccion_facturacion = models.CharField(max_length=150)
    numero_tarjeta = models.CharField(max_length=19) # Formato: 1234-5678-9012-3456
    fecha_vencimiento = models.CharField(max_length=5) # Formato: MM/AA
    cvv = models.CharField(max_length=3) # Código de seguridad

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

# NUEVO MODELO DE PROVEEDORES
class Proveedor(models.Model):
    empresa = models.CharField(max_length=100)
    contacto_nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email_corporativo = models.EmailField()
    direccion_fiscal = models.CharField(max_length=150)
    cuenta_bancaria_iban = models.CharField(max_length=34) # Datos financieros de la empresa

    def __str__(self):
        return self.empresa