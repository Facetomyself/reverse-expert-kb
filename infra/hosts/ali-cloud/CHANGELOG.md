# ali-cloud / CHANGELOG

- 2026-03-15: First-pass inspection completed. Confirmed `ali-cloud` (`106.15.239.221`) is an Alibaba Cloud ECS host running Ubuntu 24.04.3. Active runtime includes `1panel.service` on port `80`, an EasyImages container on `10086`, and a `camoufox-remote` container on `39222`. Identified 1Panel state under `/opt/1panel`, EasyImages compose/data under `/opt/1panel/apps/easyimage2/easyimage2/`, and a likely manual camoufox deployment root under `/opt/camoufox-remote`.
