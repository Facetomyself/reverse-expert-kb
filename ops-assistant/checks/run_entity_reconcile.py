#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP_DIR = Path('/tmp')
REPORT_DIR = ROOT / 'reports' / datetime.now().strftime('%Y-%m-%d')
STATE_DIR = ROOT / 'state'


def run(script_name, tmp_name):
    script = ROOT / 'checks' / script_name
    out = TMP_DIR / tmp_name
    p = subprocess.run(['python3', str(script)], text=True, capture_output=True, timeout=240)
    out.write_text(p.stdout if p.stdout else '')
    return p.returncode, out, p.stderr.strip()


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    rc, out_path, err = run('reconcile_project_entities.py', 'ops_reconcile_project_entities.json')
    data = json.loads(out_path.read_text()) if out_path.exists() and out_path.read_text().strip() else {'results': []}

    lines = ['# Project Entity Reconcile Run', '', f'- generated_at: {datetime.utcnow().isoformat()}Z', f'- source_json: {out_path}', '']
    for item in data.get('results', []):
        lines.append(f"## {item['host']}")
        matched = item.get('matchedProjects', [])
        missing = item.get('missingDocumentedProjects', [])
        undocumented = item.get('undocumentedCandidates', [])
        lines.append(f'- matched: {len(matched)}')
        lines.append(f'- missing documented: {len(missing)}')
        lines.append(f'- undocumented candidates: {len(undocumented)}')
        if missing:
            lines.append('- missing documented projects:')
            for x in missing[:8]:
                lines.append(f"  - {x['name']}")
        if undocumented:
            lines.append('- undocumented candidates:')
            for x in undocumented[:8]:
                lines.append(f"  - {x.get('path') or x.get('name') or x.get('kind')}")
        lines.append('')

    md = REPORT_DIR / 'project-entity-reconcile-run.md'
    md.write_text('\n'.join(lines) + '\n')
    state = {
        'lastRunAt': datetime.utcnow().isoformat() + 'Z',
        'reportPath': str(md),
        'jsonPath': str(out_path),
        'exitCode': rc,
        'stderr': err,
    }
    (STATE_DIR / 'entity-reconcile-last-run.json').write_text(json.dumps(state, ensure_ascii=False, indent=2))
    print(json.dumps(state, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
