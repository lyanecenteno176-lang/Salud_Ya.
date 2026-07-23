// Datos de ejemplo para el Marketplace.
// Productos registrados en las dos categorías principales: Medicamentos y Ejercicio y Bienestar.
const products = [
    {
        name: 'Tapete de Yoga',
        description: 'Tapete acolchado antideslizante ideal para yoga, pilates y estiramientos.',
        category: 'Ejercicio y Bienestar',
        subcategory: 'Yoga',
        price: 295.00,
        available: true,
        image: '/static/saludya_app/images/Tapete-de-Yoga.png',
        tag: '🌿 Recomendado',
        tagType: 'tag-recommended',
    },
    {
        name: 'Bandas de Resistencia',
        description: 'Set de bandas elásticas para fuerza, tonificación y movilidad.',
        category: 'Ejercicio y Bienestar',
        subcategory: 'Fuerza',
        price: 180.00,
        available: true,
        image: '/static/saludya_app/images/Bandas-de-Resistencia.jpg',
        tag: '💪 Fitness',
        tagType: 'tag-fitness',
    },
    {
        name: 'Mancuernas de 5 lb',
        description: 'Par de mancuernas con recubrimiento suave para entrenamientos de fuerza.',
        category: 'Ejercicio y Bienestar',
        subcategory: 'Fuerza',
        price: 380.00,
        available: true,
        image: '/static/saludya_app/images/Mancuernas-5lb.jpg',
        tag: '🔥 Oferta',
        tagType: 'tag-sale',
    },
    {
        name: 'Botella Deportiva 1 L',
        description: 'Botella reusable con tapa a prueba de fugas para tus rutinas diarias.',
        category: 'Ejercicio y Bienestar',
        subcategory: 'Accesorios',
        price: 110.00,
        available: true,
        image: '/static/saludya_app/images/Botella-deportiva.jpg',
        tag: '🆕 Nuevo',
        tagType: 'tag-new',
    },
    {
        name: 'Cuerda para Saltar Ajustable',
        description: 'Cuerda ligera con mango ergonómico para entrenamiento de cardio.',
        category: 'Ejercicio y Bienestar',
        subcategory: 'Cardio',
        price: 130.00,
        available: true,
        image: '/static/saludya_app/images/Cuerda-para-Saltar-Ajustable.jpg',
        tag: '💪 Fitness',
        tagType: 'tag-fitness',
    },
    {
        name: 'Rodillo de Espuma',
        description: 'Foam roller para liberación muscular y recuperación post-entrenamiento.',
        category: 'Ejercicio y Bienestar',
        subcategory: 'Recuperación',
        price: 210.00,
        available: true,
        image: '/static/saludya_app/images/Rodillo-de-Espuma.jpg',
        tag: '⭐ Más vendido',
        tagType: 'tag-bestseller',
    },
    {
        name: 'Báscula Digital',
        description: 'Báscula con pantalla LED para controlar tu salud y progreso diario.',
        category: 'Ejercicio y Bienestar',
        subcategory: 'Monitoreo de Salud',
        price: 265.00,
        available: true,
        image: '/static/saludya_app/images/Bascula-Digital.jpg',
        tag: '🌿 Recomendado',
        tagType: 'tag-recommended',
    },
    {
        name: 'Banda Elástica para Estiramientos',
        description: 'Banda ligera para movilidad, rehabilitación y estiramientos suaves.',
        category: 'Ejercicio y Bienestar',
        subcategory: 'Yoga',
        price: 90.00,
        available: true,
        image: '/static/saludya_app/images/Banda-Elastica.jpg',
        tag: '🆕 Nuevo',
        tagType: 'tag-new',
    },
    {
        name: 'Pelota de Pilates',
        description: 'Pelota de estabilidad para tonificar el core y mejorar el equilibrio.',
        category: 'Ejercicio y Bienestar',
        subcategory: 'Recuperación',
        price: 175.00,
        available: false,
        image: '/static/saludya_app/images/Pelota-de-Pilates.jpg',
        tag: '🔥 Oferta',
        tagType: 'tag-sale',
    },
    {
        name: 'Guantes Deportivos',
        description: 'Guantes de agarre para levantar peso y proteger tus manos.',
        category: 'Ejercicio y Bienestar',
        subcategory: 'Accesorios',
        price: 155.00,
        available: true,
        image: '/static/saludya_app/images/Guantes-Deportivos.jpg',
        tag: '💪 Fitness',
        tagType: 'tag-fitness',
    },
    {
        name: 'Toalla Deportiva de Microfibra',
        description: 'Toalla absorbente, compacta y de secado rápido para tus entrenos.',
        category: 'Ejercicio y Bienestar',
        subcategory: 'Accesorios',
        price: 85.00,
        available: true,
        image: '/static/saludya_app/images/Toalla-Deportiva.jpg',
        tag: '🌿 Recomendado',
        tagType: 'tag-recommended',
    },
    {
        name: 'Shaker Deportivo',
        description: 'Shaker con compartimento para polvos y líquidos para nutrición post-entreno.',
        category: 'Ejercicio y Bienestar',
        subcategory: 'Accesorios',
        price: 115.00,
        available: true,
        image: '/static/saludya_app/images/Shaker-Deportivo.jpg',
        tag: '⭐ Más vendido',
        tagType: 'tag-bestseller',
    },
    {
        name: 'Paracetamol 500 mg',
        description: 'Alivio rápido para dolores leves y reducción de fiebre.',
        category: 'Medicamentos',
        subcategory: 'Analgésicos',
        price: 45.00,
        available: true,
        image: '/static/saludya_app/images/paracetamol-500mg.jpg',
        tag: '⭐ Más vendido',
        tagType: 'tag-bestseller',
    },
    {
        name: 'Ibuprofeno 400 mg',
        description: 'Antiinflamatorio para dolores musculares y fiebre.',
        category: 'Medicamentos',
        subcategory: 'Analgésicos',
        price: 65.00,
        available: true,
        image: '/static/saludya_app/images/Ibuprofeno-400 mg.jpg',
        tag: '💪 Fitness',
        tagType: 'tag-fitness',
    },
    {
        name: 'Jarabe Antigripal Multicitrico',
        description: 'Alivio para síntomas gripales y congestión respiratoria.',
        category: 'Medicamentos',
        subcategory: 'Antigripales',
        price: 80.00,
        available: true,
        image: '/static/saludya_app/images/Jarabe-Antigripal-Multicitrico.jpg',
        tag: '🌿 Recomendado',
        tagType: 'tag-recommended',
    },
    {
        name: 'Vitamina C 1000 mg',
        description: 'Suplemento para reforzar el sistema inmunológico.',
        category: 'Medicamentos',
        subcategory: 'Vitaminas',
        price: 55.00,
        available: true,
        image: '/static/saludya_app/images/Vitamina-C-1000 mg.jpg',
        tag: '🆕 Nuevo',
        tagType: 'tag-new',
    },
    {
        name: 'Omeprazol',
        description: 'Alivio digestivo para acidez y malestar estomacal.',
        category: 'Medicamentos',
        subcategory: 'Cuidado Digestivo',
        price: 95.00,
        available: true,
        image: '/static/saludya_app/images/Omeprazol.jpg',
        tag: '🔥 Oferta',
        tagType: 'tag-sale',
    },
    {
        name: 'Gel Antibacterial',
        description: 'Higiene instantánea sin enjuague para manos y superficies.',
        category: 'Medicamentos',
        subcategory: 'Higiene Personal',
        price: 48.00,
        available: false,
        image: '/static/saludya_app/images/Gel-Antibacterial.jpg',
        tag: '🔥 Oferta',
        tagType: 'tag-sale',
    },
    {
        name: 'Curitas Adhesivas',
        description: 'Vendajes para heridas leves y cuidado rápido.',
        category: 'Medicamentos',
        subcategory: 'Primeros Auxilios',
        price: 25.00,
        available: true,
        image: '/static/saludya_app/images/Curitas-Adhesivas.jpg',
        tag: '⭐ Más vendido',
        tagType: 'tag-bestseller',
    },
    {
        name: 'Manzana Roja',
        description: 'Fruta fresca rica en fibra y antioxidantes para el día a día.',
        category: 'Alimentos Saludables',
        subcategory: 'Frutas',
        price: 35.00,
        available: true,
        image: '/static/saludya_app/images/Manzana-Roja.jpg',
        tag: '🌱 Orgánico',
        tagType: 'tag-organic',
        nutrition: { calories: '52 kcal', protein: '0.3 g', fiber: '2.4 g', vitamins: 'Vitamina C' },
        flags: ['Bajo en azúcar', 'Sin gluten'],
    },
    {
        name: 'Banano',
        description: 'Plátano maduro y dulce, fuente natural de potasio y energía.',
        category: 'Alimentos Saludables',
        subcategory: 'Frutas',
        price: 28.00,
        available: true,
        image: '/static/saludya_app/images/Banano.jpg',
        tag: '🥗 Saludable',
        tagType: 'tag-healthy',
        nutrition: { calories: '89 kcal', protein: '1.1 g', fiber: '2.6 g', vitamins: 'Vitamina B6' },
        flags: ['Sin gluten'],
    },
    {
        name: 'Naranja',
        description: 'Cítrico natural lleno de vitamina C y frescura para tu comida.',
        category: 'Alimentos Saludables',
        subcategory: 'Frutas',
        price: 32.00,
        available: true,
        image: '/static/saludya_app/images/Naranja.jpg',
        tag: '❤️ Recomendado',
        tagType: 'tag-recommended',
        nutrition: { calories: '47 kcal', protein: '0.9 g', fiber: '2.4 g', vitamins: 'Vitamina C' },
        flags: ['Bajo en azúcar', 'Sin gluten'],
    },
    {
        name: 'Brócoli',
        description: 'Verdura crucífera llena de vitaminas, minerales y antioxidantes.',
        category: 'Alimentos Saludables',
        subcategory: 'Verduras',
        price: 70.00,
        available: true,
        image: '/static/saludya_app/images/Brocoli.jpg',
        tag: '🌱 Orgánico',
        tagType: 'tag-organic',
        nutrition: { calories: '55 kcal', protein: '3.7 g', fiber: '2.6 g', vitamins: 'Vitamina K' },
        flags: ['Alto en fibra', 'Sin gluten'],
    },
    {
        name: 'Zanahoria',
        description: 'Hortaliza crujiente con betacarotenos para salud visual y piel.',
        category: 'Alimentos Saludables',
        subcategory: 'Verduras',
        price: 42.00,
        available: true,
        image: '/static/saludya_app/images/Zanahoria.jpg',
        tag: '⭐ Más vendido',
        tagType: 'tag-bestseller',
        nutrition: { calories: '41 kcal', protein: '0.9 g', fiber: '2.8 g', vitamins: 'Vitamina A' },
        flags: ['Bajo en azúcar', 'Sin gluten'],
    },
    {
        name: 'Espinaca',
        description: 'Verdura de hoja verde ideal para ensaladas y batidos nutritivos.',
        category: 'Alimentos Saludables',
        subcategory: 'Verduras',
        price: 58.00,
        available: true,
        image: '/static/saludya_app/images/Espinaca.jpg',
        tag: '🥗 Saludable',
        tagType: 'tag-healthy',
        nutrition: { calories: '23 kcal', protein: '2.9 g', fiber: '2.2 g', vitamins: 'Vitamina K' },
        flags: ['Sin gluten', 'Alto en fibra'],
    },
    {
        name: 'Avena Integral',
        description: 'Cereal clásico para desayunos energéticos y ricos en fibra.',
        category: 'Alimentos Saludables',
        subcategory: 'Cereales',
        price: 120.00,
        available: true,
        image: '/static/saludya_app/images/Avena-Integral.jpg',
        tag: '💪 Fitness',
        tagType: 'tag-fitness',
        nutrition: { calories: '389 kcal', protein: '16.9 g', fiber: '10.6 g', vitamins: 'Hierro' },
        flags: ['Alto en fibra'],
    },
    {
        name: 'Arroz Integral',
        description: 'Granos integrales ricos en fibra para comidas nutritivas.',
        category: 'Alimentos Saludables',
        subcategory: 'Cereales',
        price: 95.00,
        available: true,
        image: '/static/saludya_app/images/Arroz-Integral.jpg',
        tag: '🌱 Orgánico',
        tagType: 'tag-organic',
        nutrition: { calories: '123 kcal', protein: '2.7 g', fiber: '1.8 g', vitamins: 'Magnesio' },
        flags: ['Sin gluten', 'Alto en fibra'],
    },
    {
        name: 'Pechuga de Pollo',
        description: 'Pechuga magra perfecta para recetas altas en proteínas.',
        category: 'Alimentos Saludables',
        subcategory: 'Proteínas',
        price: 185.00,
        available: true,
        image: '/static/saludya_app/images/Pechuga-de-Pollo.jpg',
        tag: '🥗 Saludable',
        tagType: 'tag-healthy',
        nutrition: { calories: '165 kcal', protein: '31 g', fiber: '0 g', vitamins: 'Vitamina B6' },
        flags: ['Rico en proteínas', 'Sin gluten'],
    },
    {
        name: 'Huevos',
        description: 'Docena de huevos frescos para un desayuno nutritivo y versátil.',
        category: 'Alimentos Saludables',
        subcategory: 'Proteínas',
        price: 140.00,
        available: true,
        image: '/static/saludya_app/images/Huevos.jpg',
        tag: '⭐ Más vendido',
        tagType: 'tag-bestseller',
        nutrition: { calories: '155 kcal', protein: '13 g', fiber: '0 g', vitamins: 'Vitamina D' },
        flags: ['Rico en proteínas', 'Sin gluten'],
    },
    {
        name: 'Atún en Agua',
        description: 'Lata de atún bajo en grasa, rica en proteínas y omega-3.',
        category: 'Alimentos Saludables',
        subcategory: 'Proteínas',
        price: 110.00,
        available: true,
        image: '/static/saludya_app/images/Atun-en-Agua.jpg',
        tag: '❤️ Recomendado',
        tagType: 'tag-recommended',
        nutrition: { calories: '116 kcal', protein: '26 g', fiber: '0 g', vitamins: 'Vitamina B12' },
        flags: ['Rico en proteínas', 'Sin gluten'],
    },
    {
        name: 'Yogur Natural',
        description: 'Yogur suave sin azúcar añadido para cuidar tu digestión.',
        category: 'Alimentos Saludables',
        subcategory: 'Lácteos',
        price: 70.00,
        available: true,
        image: '/static/saludya_app/images/Yogur-Natural.jpg',
        tag: '🌱 Orgánico',
        tagType: 'tag-organic',
        nutrition: { calories: '59 kcal', protein: '10 g', fiber: '0 g', vitamins: 'Calcio' },
        flags: ['Bajo en azúcar'],
    },
    {
        name: 'Leche Descremada',
        description: 'Leche baja en grasa rica en calcio para tu nutrición diaria.',
        category: 'Alimentos Saludables',
        subcategory: 'Lácteos',
        price: 95.00,
        available: true,
        image: '/static/saludya_app/images/Leche-Descremada.jpg',
        tag: '🆕 Nuevo',
        tagType: 'tag-new',
        nutrition: { calories: '83 kcal', protein: '8 g', fiber: '0 g', vitamins: 'Calcio' },
        flags: ['Bajo en azúcar'],
    },
    {
        name: 'Almendras',
        description: 'Snack crujiente rico en grasas saludables y fibra natural.',
        category: 'Alimentos Saludables',
        subcategory: 'Snacks Saludables',
        price: 145.00,
        available: true,
        image: '/static/saludya_app/images/Almendras.jpg',
        tag: '🥗 Saludable',
        tagType: 'tag-healthy',
        nutrition: { calories: '579 kcal', protein: '21 g', fiber: '12 g', vitamins: 'Vitamina E' },
        flags: ['Alto en fibra', 'Sin gluten'],
    },
    {
        name: 'Nueces',
        description: 'Snack ideal para energía sostenida y salud cerebral.',
        category: 'Alimentos Saludables',
        subcategory: 'Snacks Saludables',
        price: 155.00,
        available: true,
        image: '/static/saludya_app/images/Nueces.jpg',
        tag: '🌱 Orgánico',
        tagType: 'tag-organic',
        nutrition: { calories: '654 kcal', protein: '15 g', fiber: '7 g', vitamins: 'Magnesio' },
        flags: ['Alto en fibra', 'Sin gluten'],
    },
    {
        name: 'Agua Mineral',
        description: 'Agua pura natural lista para hidratarte en cualquier momento.',
        category: 'Alimentos Saludables',
        subcategory: 'Bebidas Saludables',
        price: 20.00,
        available: true,
        image: '/static/saludya_app/images/Agua-Mineral.jpg',
        tag: '❤️ Recomendado',
        tagType: 'tag-recommended',
        nutrition: { calories: '0 kcal', protein: '0 g', fiber: '0 g', vitamins: 'Sin vitaminas' },
        flags: ['Sin gluten'],
    },
    {
        name: 'Agua de Coco',
        description: 'Bebida natural con electrolitos para hidratación saludable.',
        category: 'Alimentos Saludables',
        subcategory: 'Bebidas Saludables',
        price: 60.00,
        available: true,
        image: '/static/saludya_app/images/Agua-de-Coco.jpg',
        tag: '🌿 Orgánico',
        tagType: 'tag-organic',
        nutrition: { calories: '19 kcal', protein: '0.7 g', fiber: '1.1 g', vitamins: 'Potasio' },
        flags: ['Bajo en azúcar', 'Sin gluten'],
    },
    {
        name: 'Jugo Natural sin azúcar',
        description: 'Jugo de frutas recién exprimido sin azúcar añadida.',
        category: 'Alimentos Saludables',
        subcategory: 'Bebidas Saludables',
        price: 85.00,
        available: true,
        image: '/static/saludya_app/images/Jugo Natural sin azúcar.jpg',
        tag: '🥗 Saludable',
        tagType: 'tag-healthy',
        nutrition: { calories: '45 kcal', protein: '0.5 g', fiber: '1.2 g', vitamins: 'Vitamina C' },
        flags: ['Bajo en azúcar', 'Sin gluten'],
    },
];

const mainCategories = ['Todos', 'Medicamentos', 'Ejercicio y Bienestar', 'Alimentos Saludables'];
const subcategoryMap = {
    Todos: ['Todos', 'Analgésicos', 'Antigripales', 'Vitaminas', 'Cuidado Digestivo', 'Primeros Auxilios', 'Higiene Personal', 'Yoga', 'Fuerza', 'Cardio', 'Recuperación', 'Accesorios', 'Monitoreo de Salud', 'Frutas', 'Verduras', 'Cereales', 'Proteínas', 'Lácteos', 'Snacks Saludables', 'Bebidas Saludables'],
    Medicamentos: ['Todos', 'Analgésicos', 'Antigripales', 'Vitaminas', 'Cuidado Digestivo', 'Primeros Auxilios', 'Higiene Personal'],
    'Ejercicio y Bienestar': ['Todos', 'Yoga', 'Fuerza', 'Cardio', 'Recuperación', 'Accesorios', 'Monitoreo de Salud'],
    'Alimentos Saludables': ['Todos', 'Frutas', 'Verduras', 'Cereales', 'Proteínas', 'Lácteos', 'Snacks Saludables', 'Bebidas Saludables'],
};

const mainCategoryButtons = document.getElementById('mainCategoryButtons');
const subcategoryButtons = document.getElementById('subcategoryButtons');
const productGrid = document.getElementById('productGrid');
const resultInfo = document.getElementById('resultInfo');
const searchInput = document.getElementById('searchInput');
const clearSearch = document.getElementById('clearSearch');

let activeMainCategory = 'Todos';
let activeSubcategory = 'Todos';
let activeSearch = '';

function formatPrice(value) {
    return `C$ ${value.toFixed(2)}`;
}

// Crea la tarjeta de producto utilizando el template HTML.
function createCard(product) {
    const template = document.getElementById('product-card-template');
    const card = template.content.cloneNode(true);
    const article = card.querySelector('.product-card');
    const img = card.querySelector('.product-image');
    const badge = card.querySelector('.category-badge');
    const tag = card.querySelector('.product-tag');
    const name = card.querySelector('.product-name');
    const description = card.querySelector('.product-description');
    const category = card.querySelector('.product-category');
    const nutritionList = card.querySelector('.nutrition-list');
    const productFlags = card.querySelector('.product-flags');
    const price = card.querySelector('.product-price');
    const stock = card.querySelector('.product-stock');
    const btnAdd = card.querySelector('.btn-add');
    const btnDetail = card.querySelector('.btn-detail');

    img.src = product.image;
    img.alt = product.name;
    badge.textContent = product.subcategory;
    tag.textContent = product.tag;
    tag.classList.add(product.tagType);
    name.textContent = product.name;
    description.textContent = product.description;
    category.textContent = product.category;
    price.textContent = formatPrice(product.price);
    stock.textContent = product.available ? 'Disponible' : 'Agotado';

    nutritionList.innerHTML = '';
    if (product.nutrition) {
        Object.entries(product.nutrition).forEach(([key, value]) => {
            const item = document.createElement('span');
            item.className = 'nutrition-item';
            item.textContent = `${key}: ${value}`;
            nutritionList.appendChild(item);
        });
    }

    productFlags.innerHTML = '';
    if (product.flags) {
        product.flags.forEach(flag => {
            const badgeFlag = document.createElement('span');
            badgeFlag.className = 'product-flag';
            badgeFlag.textContent = flag;
            productFlags.appendChild(badgeFlag);
        });
    }

    if (!product.available) {
        article.classList.add('unavailable');
        btnAdd.disabled = true;
        btnAdd.textContent = 'Sin stock';
    }

    btnDetail.addEventListener('click', () => {
        alert(`Producto: ${product.name}\nCategoría: ${product.category} / ${product.subcategory}\nPrecio: ${formatPrice(product.price)}\n\n${product.description}`);
    });

    btnAdd.addEventListener('click', () => {
        if (!product.available) return;
        article.classList.add('added');
        btnAdd.textContent = 'Agregado';
        setTimeout(() => {
            if (product.available) btnAdd.textContent = 'Agregar al carrito';
            article.classList.remove('added');
        }, 900);
    });

    return article;
}

function updateResultInfo(count) {
    const categoryLabel = activeMainCategory === 'Todos' ? 'todas las categorías' : activeMainCategory;
    const subcategoryLabel = activeSubcategory === 'Todos' ? 'todas las subcategorías' : activeSubcategory;
    if (activeMainCategory === 'Todos' && activeSubcategory === 'Todos' && !activeSearch.trim()) {
        resultInfo.textContent = `Mostrando ${count} productos`;
    } else {
        resultInfo.textContent = `Mostrando ${count} resultados para "${activeSearch || 'todos'}" en ${categoryLabel} / ${subcategoryLabel}`;
    }
}

// Filtra y renderiza los productos visibles según categoría principal, subcategoría y búsqueda.
function renderProducts() {
    productGrid.innerHTML = '';
    const filteredProducts = products.filter(product => {
        const matchesMain = activeMainCategory === 'Todos' || product.category === activeMainCategory;
        const matchesSub = activeSubcategory === 'Todos' || product.subcategory === activeSubcategory;
        const matchesSearch = product.name.toLowerCase().includes(activeSearch.toLowerCase());
        return matchesMain && matchesSub && matchesSearch;
    });

    filteredProducts.forEach(product => {
        productGrid.appendChild(createCard(product));
    });
    updateResultInfo(filteredProducts.length);
}

// Genera botones para la categoría principal.
function renderMainCategoryButtons() {
    mainCategoryButtons.innerHTML = '';
    mainCategories.forEach(category => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'filter-pill';
        button.textContent = category;
        if (category === activeMainCategory) {
            button.classList.add('active');
        }

        button.addEventListener('click', () => {
            activeMainCategory = category;
            activeSubcategory = 'Todos';
            mainCategoryButtons.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            renderSubcategoryButtons();
            renderProducts();
        });

        mainCategoryButtons.appendChild(button);
    });
}

// Genera botones de subcategoría según la categoría principal seleccionada.
function renderSubcategoryButtons() {
    subcategoryButtons.innerHTML = '';
    const subcats = subcategoryMap[activeMainCategory] || subcategoryMap.Todos;

    subcats.forEach(subcategory => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'filter-pill';
        button.textContent = subcategory;
        if (subcategory === activeSubcategory) {
            button.classList.add('active');
        }

        button.addEventListener('click', () => {
            activeSubcategory = subcategory;
            subcategoryButtons.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            renderProducts();
        });

        subcategoryButtons.appendChild(button);
    });
}

searchInput.addEventListener('input', (event) => {
    activeSearch = event.target.value;
    renderProducts();
});

clearSearch.addEventListener('click', () => {
    searchInput.value = '';
    activeSearch = '';
    renderProducts();
});

renderMainCategoryButtons();
renderSubcategoryButtons();
renderProducts();