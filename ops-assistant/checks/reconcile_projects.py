#!/usr/bin/env python3
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TMP = Path('/tmp')
PROJECT_MAP = ROOT / 'inventory' / 'project-map.yaml'

TOKENS = [
    'tavily', 'exafree', 'grok', 'cliproxy', 'easyimage', 'camoufox',
    'mailu', 'moemail', 'harbor', 'registry-ui', 'hubcmd', 'registry',
    'proxycat', 'flaresolverr', 'anticap', 'openai', '1panel', 'derper',
    'hysteria', 'outlook', 'nas'
]


def load_json(name):
    return json.loads((TMP / name).read_text())


def load_project_map():
    data = yaml.safe_load(PROJECT_MAP.read_text()) or {}
    return data.get('hosts', {})


def extract_tokens(text):
    lower = (text or '').lower()
    hints = set()
    for token in TOKENS:
        if token in lower:
            hints.add(token)
    return hints


def extract_documented_hints(projects):
    hints = set()
    for item in projects:
        hints |= extract_tokens(item.get('name', ''))
        match = item.get('match', {}) or {}
        for value in match.values():
            if isinstance(value, list):
                for part in value:
                    hints |= extract_tokens(str(part))
            else:
                hints |= extract_tokens(str(value))
    return sorted(hints)


def extract_runtime_hints(containers, compose_files, services):
    hints = set()
    for line in containers:
        hints |= extract_tokens(line)
    for path in compose_files:
        hints |= extract_tokens(path)
    for line in services:
        hints |= extract_tokens(line)
    return sorted(hints)


def main():
    docker = load_json('ops_docker_inventory.json')['results']
    drift = load_json('ops_drift_scan.json')['results']
    systemd = load_json('ops_systemd_inventory.json')['results']
    dmap = {x['host']: x for x in docker}
    mmap = {x['host']: x for x in drift}
    smap = {x['host']: x for x in systemd}
    project_map = load_project_map()
    out = []
    for host, payload in project_map.items():
        projects = payload.get('documented_projects', [])
        doc_hints = set(extract_documented_hints(projects))
        runtime_hints = set(extract_runtime_hints(
            dmap.get(host, {}).get('containers', []),
            mmap.get(host, {}).get('composeFiles', []),
            smap.get(host, {}).get('services', []),
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
