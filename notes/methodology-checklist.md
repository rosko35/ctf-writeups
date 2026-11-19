# Methodology checklist

🇹🇷 [Türkçe](methodology-checklist.tr.md)

Study notes, not a claim of experience. Extend it as you learn. Only use it against targets you
are allowed to test (CTF platforms, your own lab).

## 0. Before you start

- [ ] Read the room/challenge description and the platform rules. Note the scope (which IPs).
- [ ] Create the writeup folder now (`python tools/new_writeup.py ...`) and paste commands into it as you go.
- [ ] Connect the VPN (if the platform uses one) and confirm you can reach the target (`ping`, `nc -vz`).
- [ ] Keep one terminal log per target (`script session.log` or copy-paste).

## 1. Reconnaissance

- [ ] Full TCP port scan, then targeted version/script scan on the open ports.
- [ ] Quick UDP scan of top ports (SNMP 161, TFTP 69, DNS 53).
- [ ] Note OS, services, versions, hostnames (add to `/etc/hosts` if the room says so).
- [ ] Search versions for known vulnerabilities (`searchsploit`, vendor advisories).

## 2. Enumeration (per service)

- [ ] Web: view source, `robots.txt`, tech stack, directories/files, vhosts, parameters (see the web checklist).
- [ ] SSH/FTP/Telnet: banner, anonymous login (FTP), known-weak versions.
- [ ] SMB: shares, null session (`smbclient -L //TARGET -N`).
- [ ] DNS, SNMP, NFS, databases: whatever is exposed.
- [ ] Collect usernames, passwords, keys, emails, version strings in one notes file.

## 3. Exploitation / foothold

- [ ] Pick the most likely path from the enumeration, not the flashiest exploit.
- [ ] Try default/weak credentials only where the rules allow it.
- [ ] Understand the exploit before running it; read public PoC code.
- [ ] After a shell: stabilise it, then run `id`, `whoami`, `hostname`, `uname -a`.

## 4. Privilege escalation

- [ ] Follow the Linux privesc checklist (`linux-privesc-checklist.md`).
- [ ] Loot: config files, history, keys, backups, other users' home folders.
- [ ] Re-enumerate as the new user; new access means new places to look.

## 5. Flags and proof

- [ ] Submit flags on the platform. Never store real flags in this repo (redact them).
- [ ] Take screenshots that prove each step (hide flags, tokens, your IP if you prefer).

## 6. Reporting (the writeup)

- [ ] Fill in the template; keep the order of what you actually did, including dead ends.
- [ ] Explain why each step worked.
- [ ] Add the defensive section: fix, detection and ATT&CK id.
- [ ] Run `python tools/check_flags.py` and `python tools/build_index.py`.
- [ ] Check the platform's rules about publishing writeups (retired/active content).

## Stuck? Ask yourself

1. Did I enumerate every port/service fully (all 65535 TCP ports)?
2. Did I read every page, source file and error message carefully?
3. Did I try the credentials/keys I already found on every service?
4. Is there a hint in the room text or task names?
5. Take a break, then re-read the notes from the top.
