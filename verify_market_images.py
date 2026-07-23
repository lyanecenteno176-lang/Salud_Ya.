from pathlib import Path
import re

js_path = Path('saludya_app/static/saludya_app/market.js')
images_dir = Path('saludya_app/static/saludya_app/images')

js = js_path.read_text(encoding='utf-8')
refs = re.findall(r"image:\s*'([^']+)'", js)
existing = {p.name for p in images_dir.iterdir()}
missing = sorted({Path(ref).name for ref in refs if Path(ref).name not in existing})
print('referenced', len(refs))
print('missing_count', len(missing))
if missing:
    print('\n'.join(missing))
else:
    print('NONE')
