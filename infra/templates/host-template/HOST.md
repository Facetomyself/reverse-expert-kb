# <host-name>

## 1. Identity
- Host label: `<host-name>`
- Static hostname: `<hostname>`
- Provider: `<provider>`
- Primary role: `<primary-role>`
- SSH alias: `<ssh-alias>`
- Main purpose: `<one-line-purpose>`

## 2. System Baseline
- OS: `<os>`
- Kernel: `<kernel>`
- Architecture: `<arch>`
- CPU: `<cpu>`
- Memory: `<memory>`
- Swap: `<swap>`
- Root disk: `<disk>`

## 3. Usage Pattern
- Host style: `<pet-or-cattle>`
- Change sensitivity: `<low|medium|high>`
- Operational preference: `<how to modify safely>`

## 4. Access Notes
- Main SSH alias: `<ssh-alias>`
- Expected user: `<user>`
- Useful first checks:
  ```bash
  ssh <ssh-alias>
  hostnamectl
  docker ps
  ss -ltnp
  ```

## 5. High-Level Service Map
- `<service>` — `<what it does>`

## 6. Machine-Level Infrastructure Notes
### nginx
- `<notes>`

### systemd / docker / runtime
- `<notes>`

## 7. Documentation Scope
本主机目录重点覆盖：
- `<area-1>`
- `<area-2>`

后续仍需补全：
- `<todo-1>`
- `<todo-2>`
