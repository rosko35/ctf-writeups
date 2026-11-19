# Linux yetki yükseltme kontrol listesi

🇬🇧 [English](linux-privesc-checklist.md)

Yalnızca yetkili hedefler için çalışma notları. Önce elle kontroller, sonra otomatik scriptler (linpeas).
Bulduğun her binary'yi [GTFOBins](https://gtfobins.github.io/) üzerinde ara.

## 1. Ben kimim?

```bash
id; whoami; hostname; uname -a; cat /etc/os-release
```

İlginç gruplar: `sudo`, `docker`, `lxd`, `disk`, `adm`, `shadow`.

## 2. sudo

```bash
sudo -l
```

- `NOPASSWD` girdisi var mı? Binary GTFOBins'te mi (find, vim, awk, python, less, ...)?
- `env_keep` içinde `LD_PRELOAD` veya izin verilen komutta joker karakter (wildcard) de kötüye kullanılabilir.

## 3. SUID / SGID ve capabilities

```bash
find / -perm -4000 -type f 2>/dev/null          # SUID
find / -perm -2000 -type f 2>/dev/null          # SGID
getcap -r / 2>/dev/null                         # dosya yetenekleri (ör. python üzerinde cap_setuid)
```

Listeyi varsayılan kurulumla karşılaştır. Standart olmayan binary'ler ilginç olanlardır.

## 4. Zamanlanmış görevler

```bash
cat /etc/crontab; ls -la /etc/cron.*; crontab -l
systemctl list-timers
```

Root tarafından çalıştırılan ve senin yazabildiğin scriptlere, başka programları tam yol vermeden
çağıranlara (PATH hijacking) veya joker karakter kullananlara bak.

## 5. Yazılabilir yerler ve hassas dosyalar

```bash
find / -writable -type f 2>/dev/null | grep -v -E '^/(proc|sys|dev)'
ls -la /etc/passwd /etc/shadow /etc/sudoers
ls -la ~ ~/.ssh /home /root 2>/dev/null
```

- Yazılabilir `/etc/passwd` veya okunabilir `/etc/shadow` (hash'i çevrimdışı kır).
- Özel SSH anahtarları, yedekler (`*.bak`, `*.old`), `.git` klasörleri, veritabanı dosyaları.

## 6. Ortada duran kimlik bilgileri

```bash
cat ~/.bash_history
grep -RniE 'password|passwd|secret|api[_-]?key' /var/www /opt /home 2>/dev/null
env
```

Bulduğun her parolayı her kullanıcıda ve serviste dene (`su`, SSH, veritabanları).

## 7. Süreçler, servisler ve ağ

```bash
ps aux
ss -tlnp                         # yalnızca localhost'ta dinleyen servislere port yönlendirme yapılabilir
```

`pspy` gibi araçlar root olmadan diğer kullanıcıların süreçlerini (ve cron işlerini) gösterir.

## 8. Diğer klasikler

- `no_root_squash` ile NFS: hedefte `cat /etc/exports`, dışarıdan `showmount -e TARGET`.
- `docker` / `lxd` grubundayken konteyner kaçışları.
- Root olarak çalışan, bilinen zafiyetli servisler (sürümleri kontrol et).
- Kernel exploit'leri: son çare. Makineyi çökertebilirler; önce kernel sürümünü tam eşleştir.

## Çaba sırası (hızlıdan yavaşa)

1. `sudo -l`  2. SUID/capabilities  3. cron  4. dosyalarda/geçmişte kimlik bilgisi  5. servisler/portlar  6. linpeas  7. kernel
