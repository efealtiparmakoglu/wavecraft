"""Check the shipped modules without executing the browser application."""
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.kind = None
        self.chunks = []
        self.modules = []
        self.import_maps = []

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.kind = dict(attrs).get('type')
            self.chunks = []

    def handle_data(self, data):
        if self.kind is not None:
            self.chunks.append(data)

    def handle_endtag(self, tag):
        if tag == 'script':
            if self.kind == 'module':
                self.modules.append(''.join(self.chunks))
            elif self.kind == 'importmap':
                self.import_maps.append(json.loads(''.join(self.chunks)))
            self.kind = None


parser = Scripts()
parser.feed((ROOT / 'index.html').read_text())
if not parser.modules or not parser.import_maps:
    raise SystemExit('Expected an application module and a local import map')
for mapping in parser.import_maps:
    for name, target in mapping['imports'].items():
        if not target.startswith('./') or not (ROOT / target).is_file():
            raise SystemExit(f'Missing local import: {name} -> {target}')
with tempfile.TemporaryDirectory() as tmp:
    for i, source in enumerate(parser.modules):
        module = Path(tmp) / f'inline-{i}.mjs'
        module.write_text(source)
        subprocess.run(['node', '--check', str(module)], check=True)
for module in [ROOT / 'timing.mjs', *sorted((ROOT / 'vendor').glob('*.js'))]:
    subprocess.run(['node', '--check', str(module)], check=True)
print('Application/vendor JavaScript syntax and import-map targets verified.')
