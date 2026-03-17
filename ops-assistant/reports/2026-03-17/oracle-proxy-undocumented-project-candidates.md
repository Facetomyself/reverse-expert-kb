# oracle-proxy undocumented project candidates - 2026-03-17

This note turns raw entity-level findings into a more operational candidate list for future `infra/` normalization.

## Scope
Host: `oracle-proxy`
Method:
- compare current documented project set vs compose-path discoveries
- inspect candidate project directories over SSH
- check whether compose projects appear to be currently running

## Candidate triage

### 1. AntiCAP-WebApi-docker
- Path: `/root/AntiCAP-WebApi-docker`
- Evidence:
  - `.git` present
  - `README.md` present
  - `docker-compose.yml` present
  - compose defines container `anticap-webapi`
- Current runtime evidence:
  - `docker compose ps` shows no running service
- Initial classification:
  - **undocumented dormant project candidate**
- Suggested next step:
  - create an `infra/hosts/oracle-proxy/projects/anticap-webapi.md` note if this service still matters

### 2. FlareSolverr
- Path: `/root/FlareSolverr`
- Evidence:
  - `.git` present
  - `README.md` present
  - `docker-compose.yml` present
  - compose defines container `flaresolverr`
- Current runtime evidence:
  - no running compose service detected
- Initial classification:
  - **undocumented dormant project candidate**
- Suggested next step:
  - document as historical anti-bot utility if still relevant

### 3. ProxyCat
- Path: `/root/ProxyCat`
- Evidence:
  - `.git` present
  - `README.md` present
  - `docker-compose.yml` present
- Current runtime evidence:
  - no running compose service detected
- Initial classification:
  - **undocumented dormant project candidate**

### 4. clove
- Path: `/root/clove`
- Evidence:
  - `.git` present
  - `README.md` present
  - `docker-compose.yml` present
  - compose defines container `clove`
- Current runtime evidence:
  - no running compose service detected
- Initial classification:
  - **undocumented dormant project candidate**

### 5. gpt-load
- Path: `/root/gpt-load`
- Evidence:
  - `docker-compose.yml` present
  - compose defines container `gpt-load`
  - optional DB services commented in compose
- Current runtime evidence:
  - no running compose service detected
- Initial classification:
  - **undocumented dormant project candidate**

### 6. grok2api backup footprint
- Path: `/root/backups/grok2api-20260313-133823`
- Evidence:
  - backup compose file preserved under backups tree
  - references full `grok2api` stack with redis / postgres / mysql options
- Current runtime evidence:
  - not an active deployment path; looks archival
- Initial classification:
  - **archive artifact, not an active undocumented project**
- Suggested next step:
  - do not treat as live project; mention only as backup footprint if needed

## Summary
High-confidence undocumented dormant project candidates on `oracle-proxy`:
- AntiCAP-WebApi-docker
- FlareSolverr
- ProxyCat
- clove
- gpt-load

Archive-only candidate:
- grok2api backup footprint under `/root/backups/`

## Recommendation
Do not immediately add all five into `infra/hosts/oracle-proxy/PROJECTS.md` as active projects.
Instead:
1. record them first as dormant / undocumented candidates
2. decide which still matter operationally
3. only then normalize them into dedicated `projects/*.md` entries or an archive section
