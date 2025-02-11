from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
    
class Quejas(models.Model):
    id_queja = models.AutoField(primary_key=True, verbose_name="ID del Robot")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    cedula = models.CharField(max_length=10, verbose_name="Cédula")
    detalle = models.CharField(max_length=100, verbose_name="Detalle de la queja") 
    Email = models.EmailField(max_length=100, verbose_name="Correo Electronico")
    foto = models.ImageField(upload_to='quejas/', null=True, blank=True, verbose_name="Foto del Robot")

    def __str__(self):
        return self.nombre

# Modelos para la gestión de viviendas

class Vivienda(models.Model):
    id_vivienda = models.AutoField(primary_key=True, verbose_name="ID de Vivienda")
    nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre de la Vivienda")
    direccion = models.CharField(max_length=255, verbose_name="Dirección de Vivienda")
    tipo = models.CharField(max_length=50, choices=[('Departamento', 'Departamento'), ('Casa', 'Casa'), ('Dúplex', 'Dúplex')], verbose_name="Tipo de Vivienda")
    estado = models.CharField(max_length=50, choices=[('En construcción', 'En construcción'), ('Terminada', 'Terminada'), ('Vendida', 'Vendida')], verbose_name="Estado")
    id_constructora = models.ForeignKey('Constructora', on_delete=models.CASCADE, verbose_name="Constructora")
    id_cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente", related_name='viviendas')
    foto = models.ImageField(upload_to='viviendas/', null=True, blank=True, verbose_name="Foto de la Vivienda")
    
    def __str__(self):
        return f"{self.direccion} - {self.tipo}"

class Constructora(models.Model):
    id_constructora = models.AutoField(primary_key=True, verbose_name="ID de Constructora")
    nombre = models.CharField(max_length=100, verbose_name="Nombre de Constructora")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(max_length=100, verbose_name="Correo Electrónico")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True, verbose_name="ID de Cliente")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Cliente")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(max_length=100, verbose_name="Correo Electrónico")
    foto = models.ImageField(upload_to='clientes/', null=True, blank=True, verbose_name="Foto del cliente")

    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    id_actividad = models.AutoField(primary_key=True, verbose_name="ID de Actividad")
    descripcion = models.CharField(max_length=255, verbose_name="Descripción de la Actividad")
    fecha_inicio = models.DateTimeField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateTimeField(verbose_name="Fecha de Fin")
    id_vivienda = models.ForeignKey('Vivienda', on_delete=models.CASCADE, verbose_name="Vivienda Asociada")
    id_constructora = models.ForeignKey('Constructora', on_delete=models.CASCADE, verbose_name="Constructora Asociada")
    
    def __str__(self):
        return f"{self.descripcion} ({self.id_vivienda.direccion})"
