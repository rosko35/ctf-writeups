# Linux privilege escalation checklist

🇹🇷 [Türkçe](linux-privesc-checklist.tr.md)

Study notes for authorised targets only. Manual checks first; automated scripts (linpeas) second.
Look up any binary you find on [GTFOBins](https://gtfobins.github.io/).

## 1. Who am I?

```bash
id; whoami; hostname; uname -a; cat /etc/os-release
```

Interesting groups: `sudo`, `docker`, `lxd`, `disk`, `adm`, `shadow`.

## 2. sudo

```bash
sudo -l
```

- Any `NOPASSWD` entry? Is the binary on GTFOBins (find, vim, awk, python, less, ...)?
- `env_keep` with `LD_PRELOAD` or a wildcard in the allowed command can also be abused.

## 3. SUID / SGID and capabilities

```bash
find / -perm -4000 -type f 2>/dev/null          # SUID
find / -perm -2000 -type f 2>/dev/null          # SGID
getcap -r / 2>/dev/null                         # file capabilities (e.g. cap_setuid on python)
```

Compare the list against what a default install has. Non-standard binaries are the interesting ones.

## 4. Scheduled tasks

```bash
cat /etc/crontab; ls -la /etc/cron.*; crontab -l
systemctl list-timers
```

Look for scripts run by root that you can write to, or that call other programs without a full
path (PATH hijacking) or use wildcards.

## 5. Writable places and sensitive files

```bash
find / -writable -type f 2>/dev/null | grep -v -E '^/(proc|sys|dev)'
ls -la /etc/passwd /etc/shadow /etc/sudoers
ls -la ~ ~/.ssh /home /root 2>/dev/null
```

- Writable `/etc/passwd` or readable `/etc/shadow` (crack the hash offline).
- Private SSH keys, backups (`*.bak`, `*.old`), `.git` folders, database files.

## 6. Credentials lying around

```bash
cat ~/.bash_history
grep -RniE 'password|passwd|secret|api[_-]?key' /var/www /opt /home 2>/dev/null
env
```

Reuse every password you find on every user and service (`su`, SSH, databases).

## 7. Processes, services and network

```bash
ps aux
ss -tlnp                         # services listening only on localhost can be port-forwarded
```

Tools such as `pspy` show processes (and cron jobs) of other users without root.

## 8. Other classics

- NFS with `no_root_squash`: `cat /etc/exports` on the target, `showmount -e TARGET` from outside.
- Container breakouts when in group `docker` / `lxd`.
- Services running as root with known vulnerabilities (check versions).
- Kernel exploits: last resort. They can crash the box; match the exact kernel version first.

## Order of effort (fast to slow)

1. `sudo -l`  2. SUID/capabilities  3. cron  4. creds in files/history  5. services/ports  6. linpeas  7. kernel
