# SaludYa - Hackathon Nicaragua 2026

## Descripción del Proyecto
SaludYa es una aplicación móvil diseñada para promover hábitos saludables mediante recordatorios personalizados y notificaciones amigables. Nuestro objetivo es facilitar el autocuidado diario y prevenir enfermedades mediante pequeñas acciones constantes.

##  Equipo "Los Pollitos"
- **Programación:** Lyane Ashanthy Centeno Campbell, Jose Gabriel Espinoza Corea
- **Diseño:** Robert Ronbin Ronsel
- **Marketing:** Nestor David Centeno Zacarias
- **Pitch/Oratoria:** Darvis Cruz Carrero Caballero

## Tecnologías Implementadas
- **Backend:** Django con Djongo (para integración con NoSQL).
- **Base de Datos:** MongoDB Compass.
- **Control de Versiones:** GitHub.
- **Entorno:** VS Code.

##  Requerimientos Funcionales
1. **Registro de Perfil:** Personalización de rutina según el usuario (estudiante, trabajador, adulto mayor).
2. **Configuración de Recordatorios:** Alarmas para agua, pausas activas y medicamentos.
3. **Sistema de Notificaciones:** Avisos amigables en tiempo real.
4. **Panel de Progreso:** Visualización del cumplimiento de metas diarias.



##  Guía de Instalación
1. Clonar este repositorio: `git clone https://github.com/lyanecenteno176-lang/SaludYa.git`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar variables de entorno para la conexión de MongoDB.
4. Ejecutar migraciones: `python manage.py migrate`
5. Iniciar servidor: `python manage.py runserver`