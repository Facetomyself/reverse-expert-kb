#!/usr/bin/env python3
import json


def is_empty(s):
    return not (s and str(s).strip())


def top(rs, key, n=15, reverse=True):
    return sorted(rs, key=key, reverse=reverse)[:n]


def main():
    obj = json.load(open("/root/.openclaw/workspace/github-repos-audit.json"))
    repos = obj["repos"]

    active = [r for r in repos if not r.get("isArchived")]
    archived = [r for r in repos if r.get("isArchived")]
    private = [r for r in repos if r.get("isPrivate")]
    public = [r for r in repos if not r.get("isPrivate")]
    forks = [r for r in repos if r.get("isFork")]

    stale_180 = [r for r in active if (r.get("days_since_push") is not None and r["days_since_push"] > 180)]
    stale_365 = [r for r in active if (r.get("days_since_push") is not None and r["days_since_push"] > 365)]

    no_desc = [r for r in repos if is_empty(r.get("description"))]
    no_topics = [r for r in repos if len(r.get("topics") or []) == 0]
    no_license = [r for r in repos if (r.get("license") in (None, "NOASSERTION"))]

    most_star = top(public, lambda r: r.get("stargazerCount") or 0, n=10)
    most_stale = top(stale_365, lambda r: r.get("days_since_push") or -1, n=15)

    print(f"GitHub repo audit for @{obj['login']} — total {obj['repoCount']} repos")
    print(f"FetchedAt: {obj['fetchedAt']}")
    print()
    print(f"Public: {len(public)} | Private: {len(private)} | Archived: {len(archived)} | Forks: {len(forks)}")
    print(f"Active repos stale >180d: {len(stale_180)} | stale >365d: {len(stale_365)}")
    print(f"Missing description: {len(no_desc)} | Missing topics: {len(no_topics)} | Missing license: {len(no_license)}")
    print()

    print("Top public repos by stars:")
    for r in most_star:
        print(f"- {r['nameWithOwner']} ⭐{r.get('stargazerCount', 0)} (lang={r.get('primaryLanguage')}, last push={r.get('days_since_push')}d)")
    print()

    print("Most stale active repos (>365d since push):")
    for r in most_stale:
        print(f"- {r['nameWithOwner']} (last push={r.get('days_since_push')}d, updated={r.get('days_since_update')}d, private={r.get('isPrivate')})")
    print()

    print("High-priority cleanup candidates (public, not archived, missing license/desc/topics):")
    prio = [
        r for r in public
        if (not r.get("isArchived"))
        and (
            r.get("license") in (None, "NOASSERTION")
            or is_empty(r.get("description"))
            or len(r.get("topics") or []) == 0
        )
    ]
    prio = sorted(
        prio,
        key=lambda r: (r.get("stargazerCount") or 0, -(r.get("days_since_push") or 0)),
        reverse=True,
    )[:25]

    for r in prio:
        miss = []
        if r.get("license") in (None, "NOASSERTION"):
            miss.append("license")
        if is_empty(r.get("description")):
            miss.append("description")
        if len(r.get("topics") or []) == 0:
            miss.append("topics")
        print(f"- {r['nameWithOwner']} (missing: {', '.join(miss)})")


if __name__ == "__main__":
    main()
