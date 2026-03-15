from pathlib import Path

p = Path('/root/tavily-key-generator/email_providers/base.py')
text = p.read_text()

old = """            subject = self._decode_blob((msg.get(\"subject\") or \"\")).lower()
            if \"verify\" not in subject and \"tavily\" not in subject:
                continue

            html = self._decode_blob(msg.get(\"html\") or \"\")
            text = self._decode_blob(msg.get(\"text\") or \"\")
            raw = self._decode_blob(msg.get(\"raw\") or \"\")
"""
new = """            subject = self._decode_blob((msg.get(\"subject\") or \"\")).lower()

            html = self._decode_blob(msg.get(\"html\") or \"\")
            text = self._decode_blob(msg.get(\"text\") or \"\")
            raw = self._decode_blob(msg.get(\"raw\") or \"\")

            # 有些邮箱后端不提供 subject 字段，但 raw 里有完整头部；用内容本身做 gate
            gate_blob = (subject + "\n" + html + "\n" + text + "\n" + raw).lower()
            if not any(k in gate_blob for k in ("verify", "tavily", "email-verification", "ticket=", "auth.tavily.com")):
                continue
"""

if old not in text:
    raise SystemExit('target gate block not found')
text = text.replace(old, new)
p.write_text(text)
print(f'patched {p}')
