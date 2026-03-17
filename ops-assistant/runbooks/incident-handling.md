# Incident Handling

## Default flow
1. Detect anomaly
2. Classify severity (P1/P2/P3)
3. Record report
4. If within SafeRemediate whitelist, attempt one bounded recovery
5. Re-check
6. Send Telegram alert if P1/P2 or if remediation failed
7. If config/data/security impact exists, escalate to human
