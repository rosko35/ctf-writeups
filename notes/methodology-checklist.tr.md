# Metodoloji kontrol listesi

🇬🇧 [English](methodology-checklist.md)

Çalışma notlarıdır, deneyim iddiası değildir. Öğrendikçe genişlet. Yalnızca test etmene izin
verilen hedeflerde kullan (CTF platformları, kendi laboratuvarın).

## 0. Başlamadan önce

- [ ] Oda/challenge açıklamasını ve platform kurallarını oku. Kapsamı (hangi IP'ler) not al.
- [ ] Writeup klasörünü hemen oluştur (`python tools/new_writeup.py ...`) ve komutları giderken oraya yapıştır.
- [ ] VPN'e bağlan (platform kullanıyorsa) ve hedefe ulaştığını doğrula (`ping`, `nc -vz`).
- [ ] Her hedef için bir terminal kaydı tut (`script session.log` veya kopyala-yapıştır).

## 1. Keşif (Reconnaissance)

- [ ] Tam TCP port taraması, sonra açık portlara hedefli sürüm/script taraması.
- [ ] En çok kullanılan UDP portlarına hızlı tarama (SNMP 161, TFTP 69, DNS 53).
- [ ] İşletim sistemi, servisler, sürümler, host adlarını not al (oda söylüyorsa `/etc/hosts`'a ekle).
- [ ] Sürümleri bilinen zafiyetler için ara (`searchsploit`, üretici duyuruları).

## 2. Numaralandırma (servis servis)

- [ ] Web: kaynak kodu, `robots.txt`, teknoloji, dizinler/dosyalar, vhost'lar, parametreler (web kontrol listesine bak).
- [ ] SSH/FTP/Telnet: banner, anonim giriş (FTP), bilinen zayıf sürümler.
- [ ] SMB: paylaşımlar, null session (`smbclient -L //HEDEF -N`).
- [ ] DNS, SNMP, NFS, veritabanları: açık olan ne varsa.
- [ ] Kullanıcı adları, parolalar, anahtarlar, e-postalar, sürüm bilgilerini tek bir not dosyasında topla.

## 3. Sömürü / ilk erişim

- [ ] Numaralandırmadan en olası yolu seç, en gösterişli exploit'i değil.
- [ ] Varsayılan/zayıf kimlik bilgilerini yalnızca kurallar izin veriyorsa dene.
- [ ] Exploit'i çalıştırmadan önce anla; herkese açık PoC kodunu oku.
- [ ] Shell aldıktan sonra stabilize et, sonra `id`, `whoami`, `hostname`, `uname -a` çalıştır.

## 4. Yetki yükseltme

- [ ] Linux yetki yükseltme kontrol listesini izle (`linux-privesc-checklist.tr.md`).
- [ ] Topla: yapılandırma dosyaları, geçmiş, anahtarlar, yedekler, diğer kullanıcıların ev dizinleri.
- [ ] Yeni kullanıcı olarak tekrar numaralandır; yeni erişim, bakılacak yeni yerler demektir.

## 5. Flag'ler ve kanıt

- [ ] Flag'leri platformda gönder. Gerçek flag'leri bu repoda asla saklama (gizle).
- [ ] Her adımı kanıtlayan ekran görüntüleri al (flag'leri, token'ları, istersen IP'ni gizle).

## 6. Raporlama (writeup)

- [ ] Şablonu doldur; gerçekte yaptığın sırayı koru, çıkmaz sokaklar dahil.
- [ ] Her adımın neden çalıştığını açıkla.
- [ ] Savunma bölümünü ekle: çözüm, tespit ve ATT&CK kimliği.
- [ ] `python tools/check_flags.py` ve `python tools/build_index.py` çalıştır.
- [ ] Platformun writeup yayınlama kurallarını kontrol et (emekli/aktif içerik).

## Takıldın mı? Kendine sor

1. Tüm port/servisleri eksiksiz numaralandırdım mı (65535 TCP portun hepsi)?
2. Her sayfayı, kaynak dosyasını ve hata mesajını dikkatlice okudum mu?
3. Bulduğum kimlik bilgilerini/anahtarları her serviste denedim mi?
4. Oda metninde veya görev adlarında ipucu var mı?
5. Ara ver, sonra notları baştan oku.
