from pathlib import Path
p = Path('/root/tavily-key-generator/config.py')
text = p.read_text()
old = 'TURNSTILE_ADAPTER_URL = "http://host.docker.internal:15072"'
new = 'TURNSTILE_ADAPTER_URL = "http://camoufox-adapter:5072"'
if old not in text:
    raise SystemExit('adapter url line not found')
text = text.replace(old, new)
p.write_text(text)
print('patched config.py')
