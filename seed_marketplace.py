import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saludya_proyecto.settings')
django.setup()

from saludya_app.models import MarketplaceCategory, Product

cats = {
    'alimentos-saludables': (
        'Alimentos Saludables',
        'Desayunos, snacks y bebidas saludables para tu día.',
    ),
    'medicamentos': (
        'Medicamentos',
        'Medicaciones farmacéuticas y orgánicas para el cuidado de la salud.',
    ),
    'ejercicio-bienestar': (
        'Ejercicio y Bienestar',
        'Yoga, gimnasios, spas de masajes y terapias psicológicas.',
    ),
}

categories = {}
for slug, (name, desc) in cats.items():
    cat, created = MarketplaceCategory.objects.get_or_create(
        slug=slug,
        defaults={'name': name, 'description': desc, 'active': True},
    )
    if not created:
        cat.name = name
        cat.description = desc
        cat.active = True
        cat.save()
    categories[slug] = cat

products = [
    (
        'Tazón energético de avena integral',
        'Desayuno saludable con avena, frutos rojos y semillas.',
        '/static/saludya_app/images/Avena-Integral.jpg',
        120.00,
        50,
        'alimentos-saludables',
        True,
    ),
    (
        'Smoothie verde detox',
        'Bebida natural de espinaca, manzana, plátano y jengibre.',
        '/static/saludya_app/images/Espinaca.jpg',
        85.00,
        40,
        'alimentos-saludables',
        True,
    ),
    (
        'Barritas de granola caseras',
        'Snack saludable para tu break con nueces y miel natural.',
        '/static/saludya_app/images/Almendras.jpg',
        65.00,
        80,
        'alimentos-saludables',
        False,
    ),
    (
        'Pack de suplementos orgánicos',
        'Vitaminas y minerales 100% orgánicos para bienestar diario.',
        '/static/saludya_app/images/Vitamina-C-1000-mg.jpg',
        220.00,
        25,
        'medicamentos',
        False,
    ),
    (
        'Jarabe natural para la tos',
        'Cuidado orgánico con miel, limón y hierbas medicinales.',
        '/static/saludya_app/images/Jarabe-Antigripal-Multicitrico.jpg',
        95.00,
        60,
        'medicamentos',
        False,
    ),
    (
        'Botiquín básico farmacéutico',
        'Medicamentos esenciales para primeros auxilios en casa.',
        '/static/saludya_app/images/Gel-Antibacterial.jpg',
        180.00,
        35,
        'medicamentos',
        False,
    ),
    (
        'Clases de yoga online',
        'Suscripción a clases de yoga en vivo para flexibilidad y calma.',
        '/static/saludya_app/images/Tapete de Yoga.jpg',
        250.00,
        100,
        'ejercicio-bienestar',
        True,
    ),
    (
        'Membresía de gimnasio mensual',
        'Acceso ilimitado a gimnasio y áreas de entrenamiento funcional.',
        '/static/saludya_app/images/Bandas-de-Resistencia.jpg',
        450.00,
        100,
        'ejercicio-bienestar',
        False,
    ),
    (
        'Sesión de spa y masaje relajante',
        'Relajación profunda para cuerpo y mente en spa urbano.',
        '/static/saludya_app/images/Toalla-Deportiva.jpg',
        380.00,
        20,
        'ejercicio-bienestar',
        False,
    ),
    (
        'Terapia psicológica inicial',
        'Consultorio con enfoque en bienestar emocional y apoyo psicológico.',
        '/static/saludya_app/images/Botella-Deportiva-1-L.jpg',
        320.00,
        15,
        'ejercicio-bienestar',
        False,
    ),
]

for name, desc, image, price, stock, cat_slug, featured in products:
    category = categories[cat_slug]
    product, created = Product.objects.get_or_create(
        name=name,
        defaults={
            'description': desc,
            'image_url': image,
            'price': price,
            'stock': stock,
            'category': category,
            'featured': featured,
            'popularity': 0,
        },
    )
    if not created:
        product.description = desc
        product.image_url = image
        product.price = price
        product.stock = stock
        product.category = category
        product.featured = featured
        product.save()

print('Categories and products created successfully')