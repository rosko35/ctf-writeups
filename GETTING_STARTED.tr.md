# Başlangıç Rehberi

Bu rehber, güvenliğe yeni başlayanlar için. Amaç: bir challenge çöz, notlarını al, writeup'a
dönüştür, GitHub'a gönder. Hepsi küçük adımlarla.

## 1. Nereden başlamalı

- **TryHackMe**: ücretsiz başlangıç yolları (ör. "Pre Security", "Complete Beginner" gibi
  başlangıç seviyesi öğrenme yolları). Güncel listeyi sitede kontrol et; ücretsiz/ücretli durumu değişebiliyor.
  Tarayıcı içinde çalışan AttackBox ile kurulum yapmadan başlayabilirsin.
- **picoCTF picoGym**: <https://play.picoctf.org/practice> adresindeki alıştırma challenge'ları.
  Hesap ücretsiz; kategoriler (Web Exploitation, Cryptography, Forensics, Reverse Engineering,
  General Skills) kolaydan zora ilerlemek için iyi. "General Skills" ile başla.
- **HackTheBox**: başlangıç için "Starting Point" ve Academy var. Kurallara dikkat: aktif
  makineler için writeup yayınlamak yasak (aşağıda).
- Önce temelleri çalış: Linux komut satırı, ağ temelleri (IP, port, TCP/HTTP), temel Python/Bash.

Önemli: yalnızca bu platformlardaki, saldırmana izin verilen hedeflere dokun. Başka hiçbir sisteme değil.

## 2. Çözerken not alma

Çözmeye başlamadan önce writeup klasörünü oluştur (aşağıda 3. bölüm) ve notları doğrudan oraya yaz.
Sonradan hatırlamaya çalışmak zordur.

Çözerken şunları kaydet:

1. Çalıştırdığın **her komut** ve çıktının ilgili kısmı (kopyala-yapıştır).
2. Neden o komutu çalıştırdığın (tek cümle yeter).
3. Çıkmaz sokaklar: neyi denedin, işe yaramadı. Bunlar değerlidir.
4. Önemli bulgular: kullanıcı adı, sürüm, dosya yolu, bulduğun parola (parolaları writeup'ta gizleyeceksin).
5. Zaman kaybettiğin yer ve nedeni ("Neyi farklı yapardım" bölümünün hammaddesi).

İpucu: terminalde `script oturum.log` yazarsan her şey bir dosyaya kaydedilir (`exit` ile durdur).
Bu dosyayı repoya koyma; yalnızca bakıp ilgili kısımları kopyala.

## 3. `new_writeup.py` kullanımı

Repo klasöründeyken (Python 3.11 veya üstü gerekir):

```bash
python tools/new_writeup.py --platform tryhackme --name "Oda Adı" --lang tr --difficulty easy --category web
```

Seçenekler:

- `--platform`: `tryhackme`, `hackthebox`, `picoctf` veya `other`
- `--name`: odanın adı (klasör adı otomatik oluşur, Türkçe karakterler dönüştürülür)
- `--lang`: `tr` veya `en` (şablonun dili)
- `--difficulty`: `easy`, `medium`, `hard`, `insane`
- `--category`: `web`, `crypto`, `forensics`, `pwn`, `reverse`, `misc` gibi

Bu komut `tryhackme/2026-11-19-oda-adi/README.md` dosyasını (tarih o günün tarihi olur) ve boş bir
`img/` klasörünü oluşturur. Aynı klasör zaten varsa hiçbir şeyi ezmez, hata verir.

Sonra README.md dosyasını aç, başlıktaki `tags` ve `tools` satırlarını düzenle, bölümleri doldur ve
rehber yorumlarını (`<!-- ... -->`) sil. Nasıl görünmesi gerektiği için
`templates/example-fictional-writeup.tr.md` dosyasına bak (kurgusal bir örnektir).

## 4. Flag'leri gizleme

Gerçek flag'leri **asla** yayınlama. Yayınlanmış flag'ler başkalarının çözümünü bozar ve
platform kurallarını ihlal edebilir.

- Yanlış: bir `THM{` ile başlayan gerçek bir değeri aynen yazmak.
- Doğru: `THM{...}`, `HTB{...}`, `picoCTF{...}` gibi gizli hâl.
- Flag'in değerini değil, **nerede bulduğunu** yaz (ör. `/root/root.txt`).
- Ekran görüntülerinde de flag, parola ve token'ları gizle (bir resim düzenleyicide siyah kutuyla kapat;
  bulanıklaştırma yerine tamamen kapat).

Kontrol için commit'ten önce çalıştır:

```bash
python tools/check_flags.py
```

Gizlenmemiş flag bulursa dosya ve satır numarasını gösterir ve hata koduyla çıkar. GitHub'daki CI de
aynı kontrolü her push'ta yapar.

## 5. Ekran görüntüsü ekleme

1. Görüntüyü writeup klasöründeki `img/` içine kaydet. Kısa, küçük harfli adlar kullan:
   `nmap-sonuc.png`, `login-sayfasi.png`. (Windows'ta `Win + Shift + S` ile alan seçip kaydedebilirsin.)
2. README.md içinde şöyle ekle:

   ```markdown
   ![nmap sonucu](img/nmap-sonuc.png)
   ```

3. Görüntüde gerçek flag, parola, kişisel bilgi veya VPN bilgisi olmadığından emin ol.
4. Mümkünse küçük tut (PNG veya JPG); gerekmedikçe büyük videolar ekleme.

## 6. Commit ve push

İlk kez, repo klasöründe (zaten yapıldıysa atla):

```bash
git remote -v          # origin görünüyorsa tamam
```

Her writeup'tan sonra:

```bash
python tools/check_flags.py     # gizlenmemiş flag var mı?
python tools/build_index.py     # indeksi güncelle
git status                      # ne değişti?
git add tryhackme/2026-11-19-oda-adi README.md README.tr.md
git commit -m "Add writeup: Oda Adı (TryHackMe)"
git push origin main
```

Notlar:

- `git add` ile hangi dosyaları eklediğini bilerek ekle; `git status` ile kontrol et.
- İlk push'ta GitHub kimlik doğrulaması isteyebilir (tarayıcıdan giriş veya kişisel erişim token'ı).
  Token'ı asla repoya yazma.
- Hata yaptıysan ve henüz push etmediysen: `git restore --staged DOSYA` ile ekleneni geri al.
- Yanlışlıkla gerçek bir flag push ettiysen: dosyayı düzelt, yeni commit at; ve flag'i geçersiz
  saymaya (platformda sıfırlamaya) çalış. Geçmişte kalır.

## 7. Önerilen ritim: haftada bir writeup

- **Pazartesi-Çarşamba**: bir oda/challenge seç ve çöz, notları al.
- **Perşembe**: writeup taslağını şablona dök, eksik adımları tamamla.
- **Cuma**: "Ne öğrendim", "Neyi farklı yapardım" ve savunma bölümünü yaz.
- **Hafta sonu**: flag ve ekran görüntülerini kontrol et, `check_flags.py` ve `build_index.py` çalıştır, commit ve push.
- Haftada bir tane yetiyor; sayı değil, her yazıda bir şeyi gerçekten anlamak önemli. Bir hafta
  atlarsan sorun değil, devam et.
- Ayda bir `notes/` klasörünü gözden geçir ve öğrendiklerinle genişlet.

## Kontrol listesi (yayınlamadan önce)

- [ ] Oda/makine için yayın serbest (HackTheBox'ta emekli mi? TryHackMe/picoCTF kuralları kontrol edildi mi?)
- [ ] Gerçek flag, parola, token yok (metinde ve ekran görüntülerinde)
- [ ] Rehber yorumları silindi
- [ ] `check_flags.py` geçti
- [ ] Kaynaklar ve yardım alınan yazılar belirtildi
