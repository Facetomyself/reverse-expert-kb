#!/usr/bin/env python3
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
TMP = Path('/tmp')
MAP = ROOT / 'inventory' / 'project-map.yaml'


def load_json(name):
    return json.loads((TMP / name).read_text())['results']


def load_map():
    return yaml.safe_load(MAP.read_text())['hosts']


def norm_containers(rows):
    out = []
    for line in rows:
        if '\t' in line:
            out.append(line.split('\t', 1)[0].strip())
        else:
            out.append(line.strip())
    return out


def has_prefix(containers, prefixes):
    return any(any(c.startswith(p) for p in prefixes) for c in containers)


def reconcile_host(host, spec, docker_map, drift_map, systemd_map):
    containers = norm_containers(docker_map.get(host, {}).get('containers', []))
    compose_files = drift_map.get(host, {}).get('composeFiles', [])
    services = [x.split()[0] for x in systemd_map.get(host, {}).get('services', []) if x.strip()]
    documented = []
    missing = []
    for proj in spec.get('documented_projects', []):
        match = proj.get('match', {})
        ok = False
        reasons = []
        wanted_containers = set(match.get('containers', []))
        if wanted_containers and wanted_containers.intersection(containers):
            ok = True
            reasons.append('container-match')
        prefixes = match.get('container_prefixes', [])
        if prefixes and has_prefix(containers, prefixes):
            ok = True
            reasons.append('container-prefix-match')
        wanted_compose = set(match.get('compose_paths', []))
        if wanted_compose and wanted_compose.intersection(compose_files):
            ok = True
            reasons.append('compose-match')
        wanted_systemd = set(match.get('systemd', []))
        if wanted_systemd and wanted_systemd.intersection(services):
            ok = True
            reasons.append('systemd-match')
        if ok or match.get('status') in ('archive', 'retired', 'dormant'):
            documented.append({
                'name': proj['name'],
                'status': 'matched' if ok else match.get('status', 'known'),
                'reasons': reasons,
            })
        else:
            if match.get('infra_only'):
                documented.append({
                    'name': proj['name'],
                    'status': 'infra-only-unverified',
                    'reasons': [],
                })
            else:
                missing.append({
                    'name': proj['name'],
                    'expected': match,
                })

    covered_compose = set()
    covered_containers = set()
    for proj in spec.get('documented_projects', []):
        m = proj.get('match', {})
        covered_compose.update(m.get('compose_paths', []))
        covered_containers.update(m.get('containers', []))

    undocumented = []
    for path in compose_files:
        if path not in covered_compose:
            undocumented.append({'kind': 'compose', 'path': path})
    for c in containers:
        if c not in covered_containers and not any(c.startswith(p) for p in ['reg-']):
            undocumented.append({'kind': 'container', 'name': c})

    return {
        'host': host,
        'matchedProjects': documented,
        'missingDocumentedProjects': missing,
        'undocumentedCandidates': undocumented,
    }


def main():
    docker = {x['host']: x for x in load_json('ops_docker_inventory.json')}
    drift = {x['host']: x for x in load_json('ops_drift_scan.json')}
    systemd = {x['host']: x for x in load_json('ops_systemd_inventory.json')}
    mapping = load_map()
    results = []
    for host, spec in mapping.items():
        results.append(reconcile_host(host, spec, docker, drift, systemd))
    print(json.dumps({'results': results}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
