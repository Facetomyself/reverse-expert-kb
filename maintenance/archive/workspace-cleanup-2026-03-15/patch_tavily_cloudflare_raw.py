from pathlib import Path

p = Path('/root/tavily-key-generator/email_providers/cloudflare.py')
text = p.read_text()
old = """                return [
                    {
                        \"subject\": item.get(\"subject\") or \"\",
                        \"html\": item.get(\"html\") or item.get(\"raw\") or \"\",
                        \"text\": item.get(\"text\") or item.get(\"raw\") or \"\",
                    }
                    for item in results
                ]
"""
new = """                return [
                    {
                        \"subject\": item.get(\"subject\") or \"\",
                        \"html\": item.get(\"html\") or \"\",
                        \"text\": item.get(\"text\") or \"\",
                        \"raw\": item.get(\"raw\") or \"\",
                    }
                    for item in results
                ]
"""
if old not in text:
    raise SystemExit('target block not found')
text = text.replace(old, new)
p.write_text(text)
print(f'patched {p}')
