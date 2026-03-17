#!/usr/bin/env python3
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'state' / 'last-run.json'
RULES = ROOT / 'inventory' / 'alert-rules.yaml'


def main():
    state = json.loads(STATE.read_text())
    rules = yaml.safe_load(RULES.read_text())
    host_rules = rules.get('host_rules', {})
    hint_rules = rules.get('hint_rules', {})

    p1 = []
    for item in state.get('alerts', {}).get('p1', []):
        host = item.split(':', 1)[0]
        hr = host_rules.get(host, {})
        if hr.get('suppress_p1'):
            continue
        p1.append(item)

    p2 = []
    for item in state.get('alerts', {}).get('p2', []):
        host, rest = item.split(':', 1)
        hr = host_rules.get(host, {})
        if 'stale hints' in rest and hr.get('suppress_stale_hints'):
            continue
        suppressed = False
        for hint, cfg in hint_rules.items():
            if hint in rest:
                if cfg.get('treat_as_infra_service') and host in (cfg.get('suppress_stale_on_hosts') or []):
                    suppressed = True
                    break
                if host in (cfg.get('suppress_stale_on_hosts') or []):
                    suppressed = True
                    break
        if not suppressed:
            p2.append(item)

    state['alerts'] = {'p1': p1, 'p2': p2}
    notes = []
    for host, cfg in host_rules.items():
        if cfg.get('emit_note'):
            notes.append(f"{host}: {cfg['emit_note']}")
    state['alertRuleNotes'] = notes
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    print(json.dumps(state, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
