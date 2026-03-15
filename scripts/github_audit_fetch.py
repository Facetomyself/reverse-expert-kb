#!/usr/bin/env python3
import json, subprocess, sys, datetime

QUERY = """
query($cursor:String){
  viewer {
    login
    repositories(first: 100, after: $cursor, ownerAffiliations: OWNER, orderBy:{field: PUSHED_AT, direction: DESC}){
      pageInfo{hasNextPage endCursor}
      nodes{
        nameWithOwner
        name
        url
        isPrivate
        isFork
        isArchived
        createdAt
        updatedAt
        pushedAt
        description
        homepageUrl
        diskUsage
        stargazerCount
        forkCount
        primaryLanguage{ name }
        licenseInfo{ spdxId }
        defaultBranchRef{ name }
        repositoryTopics(first: 20){ nodes{ topic{ name } } }
      }
    }
  }
}
""".strip()


def gh_api_graphql(cursor=None):
    args = ["gh", "api", "graphql", "-f", f"query={QUERY}"]
    if cursor:
        args += ["-f", f"cursor={cursor}"]
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr)
        raise SystemExit(p.returncode)
    return json.loads(p.stdout)


def parse_dt(s):
    if not s:
        return None
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def main():
    all_nodes = []
    cursor = None
    pages = 0
    login = None

    while True:
        pages += 1
        data = gh_api_graphql(cursor)
        viewer = data["data"]["viewer"]
        login = viewer["login"]
        repos = viewer["repositories"]
        all_nodes.extend(repos["nodes"])
        pi = repos["pageInfo"]
        if not pi["hasNextPage"]:
            break
        cursor = pi["endCursor"]
        if pages > 50:
            break

    now = datetime.datetime.now(datetime.timezone.utc)

    for r in all_nodes:
        r["primaryLanguage"] = (r.get("primaryLanguage") or {}).get("name")
        r["defaultBranch"] = (r.get("defaultBranchRef") or {}).get("name")
        r.pop("defaultBranchRef", None)

        r["license"] = (r.get("licenseInfo") or {}).get("spdxId")
        r.pop("licenseInfo", None)

        r["topics"] = [n["topic"]["name"] for n in (r.get("repositoryTopics") or {}).get("nodes", [])]
        r.pop("repositoryTopics", None)

        pushed = parse_dt(r.get("pushedAt"))
        updated = parse_dt(r.get("updatedAt"))
        r["days_since_push"] = (now - pushed).days if pushed else None
        r["days_since_update"] = (now - updated).days if updated else None

    out = {
        "login": login,
        "fetchedAt": now.isoformat(),
        "repoCount": len(all_nodes),
        "repos": all_nodes,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
