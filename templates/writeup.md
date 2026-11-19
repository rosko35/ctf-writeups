---
title: "Room Name"
platform: tryhackme
category: web
difficulty: easy
date: YYYY-MM-DD
tags: [tag1, tag2]
tools: [nmap, gobuster]
---

# Room Name

<!--
Before publishing, check:
- The room/machine/challenge is allowed to be written up (retired, or the platform permits it).
- No real flags, passwords, API keys, VPN files or session tokens anywhere (screenshots too).
- Delete every guidance comment like this one.
-->

## Summary

<!-- 3-5 sentences: what the target is, the vulnerability chain in one line, and the end result
(e.g. "user shell via X, root via Y"). A reader should know what happened without reading on. -->

## Reconnaissance

<!-- What you learned before touching anything. Show the exact commands and the relevant part of
their output (trim noise). Typical: nmap scan, service versions, OS guess, web technologies.
Explain WHY you ran each command, not only what it printed. -->

```bash
nmap -sC -sV -oA nmap/initial TARGET_IP
```

## Enumeration

<!-- Dig into the services you found: directories, parameters, users, shares, versions.
Write down dead ends briefly too; they show how you think. End with the finding that led
to the next step. -->

## Foothold / Exploitation

<!-- How you got the first access. Name the vulnerability class (and CVE if any), show the request
or command that triggers it, and explain why it works. Show the evidence (a short output
excerpt or a screenshot from img/). -->

![description](img/example.png)

## Privilege Escalation

<!-- Only if applicable (delete the section otherwise). What you checked, what stood out, and the
exact step from the low-privileged user to the higher one. Mention which enumeration
(sudo -l, SUID, cron, ...) revealed it. -->

## Flags

<!-- RULE: never publish real flags. Redact them, e.g. THM{...}, HTB{...}, picoCTF{...}.
Write where you found each flag (file path or location), not its value. -->

| Flag | Location | Value |
|------|----------|-------|
| user | `/home/user/user.txt` | `THM{...}` |
| root | `/root/root.txt` | `THM{...}` |

## What I learned

<!-- New concepts, tools or commands. Be concrete: "I learned that X works because Y",
not "it was fun". -->

## What I would do differently

<!-- Where you lost time, which assumption was wrong, what you would do faster next time,
and which enumeration step you skipped that would have saved you. -->

## Defensive takeaway

<!-- How a defender could prevent or detect each step of the chain. For every weakness give
(1) the fix, (2) a detection idea (log source, alert), and (3) the MITRE ATT&CK technique id
where relevant, e.g. T1190 Exploit Public-Facing Application, T1078 Valid Accounts,
T1548.003 Sudo and Sudo Caching. Look ids up at https://attack.mitre.org/ -->

| Step | Prevention | Detection | ATT&CK |
|------|------------|-----------|--------|
| e.g. initial access | patch / input validation | web server logs | T1190 |

## References

<!-- Links you actually used: docs, CVE pages, man pages, GTFOBins, other writeups you read
(credit them). One per line. -->

- <https://attack.mitre.org/>
