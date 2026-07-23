from pathlib import Path
import re

path = Path('saludya_app/static/saludya_app/market.js')
text = path.read_text(encoding='utf-8')
lines = text.splitlines()
new_lines = []
product_name = None
for line in lines:
    stripped = line.strip()
    if stripped.startswith("name:"):
        m = re.search(r"name:\s*'([^']+)'", stripped)
        product_name = m.group(1) if m else None
    if stripped.startswith("image:") and product_name:
        fname = product_name
        for old, new in [
            ('á','a'), ('é','e'), ('í','i'), ('ó','o'), ('ú','u'),
            ('Á','A'), ('É','E'), ('Í','I'), ('Ó','O'), ('Ú','U'), ('ñ','n'),
            (' ', '-'), ('/', '-'), ('&', ''), (',', ''), ('.', ''), ('(', ''), (')', ''), ("'", ''), (":", ''), ('?', ''), ('¡', ''), ('¿', ''), ('+', '')
        ]:
            fname = fname.replace(old, new)
        fname = re.sub(r"[^A-Za-z0-9\-]", '', fname)
        new_url = f"/static/saludya_app/images/{fname}.jpg"
        line = re.sub(r"image:\s*'[^']+'", f"image: '{new_url}'", line)
        product_name = None
    new_lines.append(line)

path.write_text("\n".join(new_lines), encoding='utf-8')
print('updated image paths in', path)
