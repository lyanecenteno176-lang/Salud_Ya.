from pathlib import Path
import shutil

images_dir = Path('saludya_app/static/saludya_app/images')
aliases = {
    'Botella-Deportiva-1-L.jpg': 'Botella-deportiva.jpg',
    'Banda-Elastica-para-Estiramientos.jpg': 'Banda-Elastica.jpg',
    'Toalla-Deportiva-de-Microfibra.jpg': 'Toalla-Deportiva.jpg',
    'Paracetamol-500-mg.jpg': 'paracetamol-500mg.jpg',
    'Ibuprofeno-400-mg.jpg': 'Ibuprofeno-400 mg.jpg',
    'Vitamina-C-1000-mg.jpg': 'Vitamina-C-1000 mg.jpg',
    'Jugo-Natural-sin-azucar.jpg': 'Jugo Natural sin azúcar.jpg',
}

for expected, source in aliases.items():
    src = images_dir / source
    dst = images_dir / expected
    if src.exists() and not dst.exists():
        shutil.copy2(src, dst)
        print(f'copied {src.name} -> {dst.name}')
    elif dst.exists():
        print(f'already exists {dst.name}')
    else:
        print(f'missing source {src.name}')
