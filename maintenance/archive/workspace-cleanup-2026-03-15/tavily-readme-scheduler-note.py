from pathlib import Path
p = Path('/root/tavily-key-generator/README.md')
text = p.read_text()
needle = '```bash\ngit clone https://github.com/skernelx/tavily-key-generator.git\ncd tavily-key-generator\npip install -r requirements.txt\nplaywright install firefox\ncp config.example.py config.py\n# 编辑 config.py 填写配置\npython main.py\n```\n'
insert = needle + '\n### Compose 定时注册（每 3 小时 5 个的方案）\n\n如果要以**平均每 36 分钟 1 个**的频率长期运行，推荐使用独立 solver + scheduler 的 compose 方案，而不是让主注册容器常驻自循环。\n\n当前建议拓扑：\n\n- `camoufox`：Tavily 私有浏览器后端\n- `camoufox-adapter`：Tavily 私有 Turnstile solver（宿主机端口 `16072`）\n- `tavily-scheduler`：每次只跑 `RUN_COUNT = 1` / `RUN_THREADS = 1`，完成后睡眠 `2160` 秒再触发下一轮\n\n这样更容易控制频率，也不会和其他项目（例如 Grok）的 solver 混用。\n'
if needle not in text:
    raise SystemExit('README quickstart block not found')
text = text.replace(needle, insert, 1)
p.write_text(text)
print('patched README')
