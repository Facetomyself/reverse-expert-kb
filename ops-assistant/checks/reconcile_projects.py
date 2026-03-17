#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT.parent
INFRA = WS / 'infra' / 'hosts'
TMP = Path('/tmp')

HOST_PROJECT_DOCS = {
    'oracle-proxy': INFRA / 'oracle-proxy' / 'PROJECTS.md',
    'oracle-docker-proxy': INFRA / 'oracle-docker-proxy' / 'PROJECTS.md',
    'ali-cloud': INFRA / 'ali-cloud' / 'PROJECTS.md',
    'oracle-mail': INFRA / 'oracle-mail' / 'PROJECTS.md',
}


def load_json(name):
    return json.loads((TMP / name).read_text())


def extract_doc_hints(text):
    lower = text.lower()
    hints = set()
    for token in [
        'tavily', 'exafree', 'grok', 'cliproxy', 'easyimage', 'camoufox',
        'mailu', 'moemail', 'harbor', 'registry-ui', 'hubcmd', 'registry',
        'proxycat', 'flaresolverr', 'anticap', 'openai', '1panel'
    ]:
        if token in lower:
            hints.add(token)
    return sorted(hints)


def extract_runtime_hints(containers, compose_files):
    hints = set()
    for line in containers:
        low = line.lower()
        for token in [
            'tavily', 'exafree', 'grok', 'cliproxy', 'easyimage', 'camoufox',
            'mailu', 'moemail', 'harbor', 'registry-ui', 'hubcmd', 'reg-',
            'proxycat', 'flaresolverr', 'anticap', 'openai', '1panel'
        ]:
            if token in low:
                hints.add(token)
    for path in compose_files:
        low = path.lower()
        for token in [
            'tavily', 'exafree', 'grok', 'cliproxy', 'easyimage', 'camoufox',
            'mailu', 'moemail', 'harbor', 'registry-ui', 'hubcmd', 'registry',
            'proxycat', 'flaresolverr', 'anticap', 'openai', '1panel'
        ]:
            if token in low:
                hints.add(token)
    return sorted(hints)


def main():
    docker = load_json('ops_docker_inventory.json')['results']
    drift = load_json('ops_drift_scan.json')['results']
    dmap = {x['host']: x for x in docker}
    mmap = {x['host']: x for x in drift}
    out = []
    for host, doc in HOST_PROJECT_DOCS.items():
        text = doc.read_text() if doc.exists() else ''
        doc_hints = set(extract_doc_hints(text))
        runtime_hints = set(extract_runtime_hints(
            dmap.get(host, {}).get('containers', []),
            mmap.get(host, {}).get('composeFiles', []),
        ))
        undocumented = sorted(runtime_hints - doc_hints)
        stale = sorted(doc_hints - runtime_hints)
        out.append({
            'host': host,
            'documentedHints': sorted(doc_hints),
            'runtimeHints': sorted(runtime_hints),
            'undocumentedHints': undocumented,
            'staleHints': stale,
        })
    print(json.dumps({'results': out}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
