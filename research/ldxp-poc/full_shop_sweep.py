#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

OUT_DIR = Path('/root/.openclaw/workspace/research/ldxp-poc/full-shop-sweep-20260609')
OUT_DIR.mkdir(parents=True, exist_ok=True)
SEARCH = '/root/.openclaw/workspace/skills/search-layer/scripts/search.py'

queries = [
    'site:pay.ldxp.cn/shop',
    'site:pay.ldxp.cn/shop 链动小铺',
    'site:pay.ldxp.cn/shop 自动发卡',
    'site:pay.ldxp.cn/shop 自动发卡网',
    'site:pay.ldxp.cn/shop 店铺地址',
    'site:pay.ldxp.cn/shop 店铺',
    'site:pay.ldxp.cn/shop 商品',
    'site:pay.ldxp.cn/shop 公告',
    'site:pay.ldxp.cn/shop 购买',
    'site:pay.ldxp.cn/shop 库存',
    'site:pay.ldxp.cn/shop 卡密',
    'site:pay.ldxp.cn/shop 发卡',
    'site:pay.ldxp.cn/shop API',
    'site:pay.ldxp.cn/shop api',
    'site:pay.ldxp.cn/shop 游戏',
    'site:pay.ldxp.cn/shop 会员',
    'site:pay.ldxp.cn/shop 账号',
    'site:pay.ldxp.cn/shop 软件',
    'site:pay.ldxp.cn/shop 课程',
    'site:pay.ldxp.cn/shop 兑换',
    'site:pay.ldxp.cn/shop 充值',
    'site:pay.ldxp.cn/shop 代充',
    'site:pay.ldxp.cn/shop 微信',
    'site:pay.ldxp.cn/shop 支付宝',
    'site:pay.ldxp.cn/shop QQ',
    'pay.ldxp.cn/shop 链动小铺',
    'pay.ldxp.cn/shop 自动发卡',
    'pay.ldxp.cn/shop 店铺地址',
    'pay.ldxp.cn/shop 商品',
    'pay.ldxp.cn/shop 公告',
    'pay.ldxp.cn/shop 购买',
    'pay.ldxp.cn/shop 库存',
    'pay.ldxp.cn/shop 卡密',
    'pay.ldxp.cn/shop 发卡',
    'pay.ldxp.cn/shop API',
    'pay.ldxp.cn/shop 游戏',
    'pay.ldxp.cn/shop 会员',
    'pay.ldxp.cn/shop 账号',
    'pay.ldxp.cn/shop 软件',
    'pay.ldxp.cn/shop 充值',
]

sources = ['exa', 'tavily']
shop_re = re.compile(r'https?://pay\.ldxp\.cn/shop/([^/?#\s]+)(?:[/?#][^\s]*)?', re.I)

raw_runs = []
errors = []
merged = {}

def batches(xs, n):
    for i in range(0, len(xs), n):
        yield i // n + 1, xs[i:i+n]

for source in sources:
    for batch_no, batch in batches(queries, 5):
        cmd = [sys.executable, SEARCH, '--queries', *batch, '--mode', 'deep', '--intent', 'exploratory', '--source', source, '--num', '20']
        run_id = f'{source}_batch_{batch_no:02d}'
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=180)
        (OUT_DIR / f'{run_id}.stdout.json').write_text(proc.stdout, encoding='utf-8')
        (OUT_DIR / f'{run_id}.stderr.txt').write_text(proc.stderr, encoding='utf-8')
        if proc.returncode != 0:
            errors.append({'run_id': run_id, 'returncode': proc.returncode, 'stderr': proc.stderr[-2000:]})
            continue
        try:
            data = json.loads(proc.stdout)
        except Exception as exc:
            errors.append({'run_id': run_id, 'error': f'json parse failed: {exc}', 'stderr': proc.stderr[-2000:], 'stdout_prefix': proc.stdout[:500]})
            continue
        raw_runs.append({'run_id': run_id, 'source': source, 'queries': batch, 'count': data.get('count', 0)})
        for result in data.get('results', []):
            url = (result.get('url') or '').strip().split('#')[0]
            m = shop_re.search(url)
            if not m:
                continue
            slug = m.group(1)
            canonical = f'https://pay.ldxp.cn/shop/{slug}'
            key = slug.lower()
            title = (result.get('title') or '').strip()
            snippet = (result.get('snippet') or '').strip()
            entry = merged.setdefault(key, {
                'shop_id': slug,
                'url': canonical,
                'title_candidates': [],
                'snippet_candidates': [],
                'sources': [],
                'raw_urls': [],
                'first_seen_query_runs': [],
            })
            if title and title not in entry['title_candidates']:
                entry['title_candidates'].append(title)
            if snippet and snippet not in entry['snippet_candidates']:
                entry['snippet_candidates'].append(snippet)
            if source not in entry['sources']:
                entry['sources'].append(source)
            if url not in entry['raw_urls']:
                entry['raw_urls'].append(url)
            if run_id not in entry['first_seen_query_runs']:
                entry['first_seen_query_runs'].append(run_id)

shops = sorted(merged.values(), key=lambda x: x['shop_id'].lower())
for shop in shops:
    shop['sources'] = sorted(shop['sources'])
    shop['source_count'] = len(shop['sources'])
    shop['best_title'] = next((t for t in shop['title_candidates'] if not t.startswith('http')), shop['title_candidates'][0] if shop['title_candidates'] else '')

summary = {
    'generated_at': datetime.now(timezone(timedelta(hours=8))).isoformat(),
    'target': 'pay.ldxp.cn shop pages',
    'method': 'two-source search sweep and URL/slug dedupe',
    'sources': sources,
    'query_count': len(queries),
    'run_count': len(raw_runs),
    'raw_runs': raw_runs,
    'unique_shops': len(shops),
    'dual_source_shops': sum(1 for s in shops if s['source_count'] == 2),
    'single_source_shops': sum(1 for s in shops if s['source_count'] == 1),
    'errors': errors,
    'limitations': [
        'This is search-index coverage, not guaranteed site-internal exhaustive coverage.',
        'Search snippets/titles are not reliable enough for announcement/product/price extraction.',
    ],
}
output = {'summary': summary, 'shops': shops}
(OUT_DIR / 'shops_full_two_source_merged.json').write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
(OUT_DIR / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
