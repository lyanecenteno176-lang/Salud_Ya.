# SaludYa - Hackathon Nicaragua 2026

## Plataforma web para la promoción de hábitos saludables.
SaludYa es una aplicación web desarrollada con Django que busca fomentar hábitos saludables mediante herramientas de seguimiento, recordatorios, gamificación y un marketplace de productos relacionados con el bienestar. El proyecto fue desarrollado como parte del Hackathon Nicaragua 2026.

## Propuesta de Valor
> *“SaludYa ayuda a crear hábitos saludables mediante recordatorios simples, personalizados y amigables para mejorar el autocuidado diario.”*

##  Equipo "Los Pollitos"
- **Programación:** Lyane Ashanthy Centeno Campbell, Jose Gabriel Espinoza Corea
- **Diseño:** Robert Robin Ronsel Nicho
- **Marketing:** Nestor David Centeno Zacarias
- **Pitch/Oratoria:** Darvis Cruz Carrero Caballero
- 
## Funcionalidades principales.
1. Gestión de hábitos saludables.
2. Registro de consumo de agua.
3. Control de medicamentos.
4. Seguimiento de ejercicios.
5. Panel de progreso.
6. Sistema de gamificación.
7. Marketplace de productos saludables.
8. Carrito de compras.
9. Gestión de pedidos.
10. Exportación de reportes.


## Tecnologías Implementadas
1. Python 3.11
2. Django
3. SQL Server
4. HTML5
5. CSS3
6. JavaScript
7. Git y GitHub


## Definición del Problema
Muchas personas olvidan acciones preventivas básicas como:
- Tomar agua
- Tomar medicamentos
- Realizar actividad física

## Definición de Usuarios
Grupos de usuarios identificados:
- **Primario:** Estudiantes 
- **Secundario:** Trabajadores 
- **Terciario:** Adultos mayores 

## Alcance del MVP
Funciones principales del proyecto:

### 1. Hidratación
- Meta de vasos diarios
- Notificaciones

### 2. Medicación
- Nombre del medicamento
- Hora
- Confirmación de medicación tomada

### 3. Pausas Activas
- Aviso cada cierto tiempo
- Porcentaje de cumplimiento

### 4. Dashboard
- Progreso diario
- Porcentaje de cumplimiento


## Guía de Instalación

1. Clonar este repositorio: git clone https://github.com/lyanecenteno176-lang/Salud_Ya.git
   cd Salud_Ya
2. Crear un entorno virtual: python -m venv venv
3. Activar el entorno virtual (Windows):venv\Scripts\activate
4. Instalar las dependencias:pip install -r requirements.txt
5. Configurar la conexión a la base de datos en el archivo `settings.py` con los datos correspondientes de SQL Server.
6. Ejecutar las migraciones:python manage.py migrate
7. Crear un usuario administrador (opcional):python manage.py createsuperuser
8. Iniciar el servidor de desarrollo:python manage.py runserver
9. Abrir el navegador y acceder a:http://127.0.0.1:8000/



