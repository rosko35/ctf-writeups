---
title: "Oda Adı"
platform: tryhackme
category: web
difficulty: easy
date: YYYY-MM-DD
tags: [etiket1, etiket2]
tools: [nmap, gobuster]
---

# Oda Adı

<!--
Yayınlamadan önce kontrol et:
- Oda/makine/challenge için writeup yayınlamak serbest mi? (emekli olmuş mu, platform izin veriyor mu?)
- Hiçbir yerde gerçek flag, parola, API anahtarı, VPN dosyası veya oturum token'ı yok (ekran görüntüleri dahil).
- Bu tür rehber yorumlarının hepsini sil.
-->

## Özet

<!-- 3-5 cümle: hedef nedir, zafiyet zinciri tek cümlede, sonuç ne oldu
(ör. "X ile kullanıcı shell'i, Y ile root"). Okuyan devamını okumadan ne olduğunu anlamalı. -->

## Keşif (Reconnaissance)

<!-- Hedefe dokunmadan önce öğrendiklerin. Tam komutları ve çıktının ilgili kısmını göster
(gürültüyü kırp). Tipik: nmap taraması, servis sürümleri, işletim sistemi, web teknolojileri.
Her komutu neden çalıştırdığını da yaz, sadece çıktısını değil. -->

```bash
nmap -sC -sV -oA nmap/initial HEDEF_IP
```

## Numaralandırma (Enumeration)

<!-- Bulduğun servisleri derinlemesine incele: dizinler, parametreler, kullanıcılar, paylaşımlar,
sürümler. Çıkmaz sokakları da kısaca yaz; nasıl düşündüğünü gösterir. Bir sonraki adıma
götüren bulguyla bitir. -->

## İlk Erişim / Sömürü (Foothold / Exploitation)

<!-- İlk erişimi nasıl elde ettin? Zafiyet türünü (varsa CVE'yi) yaz, tetikleyen isteği veya
komutu göster ve neden çalıştığını açıkla. Kanıt ekle (kısa çıktı veya img/ içinden
ekran görüntüsü). -->

![açıklama](img/ornek.png)

## Yetki Yükseltme (Privilege Escalation)

<!-- Sadece geçerliyse (değilse bölümü sil). Neleri kontrol ettin, neyi fark ettin ve düşük yetkili
kullanıcıdan yükseğe geçtiğin tam adım. Hangi numaralandırmanın (sudo -l, SUID, cron, ...)
bunu ortaya çıkardığını belirt. -->

## Flag'ler

<!-- KURAL: Gerçek flag'leri asla yayınlama. Gizle: THM{...}, HTB{...}, picoCTF{...}.
Değerini değil, nerede bulduğunu (dosya yolu veya konum) yaz. -->

| Flag | Konum | Değer |
|------|-------|-------|
| user | `/home/user/user.txt` | `THM{...}` |
| root | `/root/root.txt` | `THM{...}` |

## Ne öğrendim

<!-- Yeni kavramlar, araçlar veya komutlar. Somut ol: "X, Y yüzünden çalışıyor öğrendim";
"eğlenceliydi" değil. -->

## Neyi farklı yapardım

<!-- Nerede zaman kaybettin, hangi varsayımın yanlıştı, bir dahaki sefere neyi daha hızlı
yaparsın, atladığın hangi numaralandırma adımı zaman kazandırırdı. -->

## Savunma açısından çıkarımlar

<!-- Bir savunmacı zincirin her adımını nasıl önleyebilir veya tespit edebilir? Her zayıflık için
(1) çözüm, (2) tespit fikri (log kaynağı, alarm) ve (3) uygunsa MITRE ATT&CK teknik kimliğini yaz;
ör. T1190 Exploit Public-Facing Application, T1078 Valid Accounts,
T1548.003 Sudo and Sudo Caching. Kimlikleri https://attack.mitre.org/ adresinden bul. -->

| Adım | Önleme | Tespit | ATT&CK |
|------|--------|--------|--------|
| ör. ilk erişim | yama / girdi doğrulama | web sunucu logları | T1190 |

## Kaynaklar

<!-- Gerçekten kullandığın bağlantılar: dokümanlar, CVE sayfaları, man sayfaları, GTFOBins,
okuduğun diğer writeup'lar (kaynak göster). Satır başına bir tane. -->

- <https://attack.mitre.org/>
