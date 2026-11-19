# CTF ve Güvenlik Lab Writeup'ları

🇬🇧 [English](README.md)

TryHackMe, HackTheBox ve picoCTF üzerinde çözdüğüm güvenlik challenge'larının writeup'ları ve
çalışma notlarım için bir repo. Bilerek boş başlıyor: her writeup, challenge'ı kendim çözdükten sonra eklenir.

## Writeup indeksi

Bu tablo, `tools/build_index.py` tarafından her writeup'ın front matter bilgisinden üretilir. Elle düzenleme.

<!-- INDEX:START -->
Henüz writeup yok. İlk writeup eklendiğinde bu indeks kendiliğinden dolacak.
<!-- INDEX:END -->

## Repo nasıl düzenlendi

```text
tryhackme/    TryHackMe odalarının writeup'ları
hackthebox/   HackTheBox makine ve challenge writeup'ları
picoctf/      picoCTF / picoGym challenge writeup'ları
other/        diğer her şey (başka platformlar, kendi laboratuvarım)
templates/    writeup şablonu (EN/TR) ve açıkça kurgusal bir örnek
tools/        new_writeup.py, build_index.py, check_flags.py
tests/        araçlar için pytest testleri
notes/        kopya kağıtları: metodoloji, komutlar, Linux privesc, web temelleri (EN/TR)
```

Her writeup `<platform>/YYYY-MM-DD-oda-adi/README.md` yolunda durur; ekran görüntüleri yanındaki `img/` klasöründedir.

`templates/example-fictional-writeup.tr.md` dosyası beklenen ayrıntı düzeyini gösterir. Bu dosya
**kurgusaldır**: dokümantasyon IP aralığında uydurma bir makine, gerçek bir oda değil ve içinde hiçbir şey çözülmedi.

Yeni başlayanlar için adım adım rehber: [GETTING_STARTED.tr.md](GETTING_STARTED.tr.md).

## Araçları kullanma

Python 3.11+, yalnızca standart kütüphane (pytest ve ruff geliştirme içindir).

```bash
python tools/new_writeup.py --platform tryhackme --name "Oda Adı" --lang tr --difficulty easy --category web
python tools/build_index.py          # yukarıdaki indeksi (ve İngilizce olanı) yeniden üret
python tools/check_flags.py          # gizlenmemiş flag varsa hata ver

python -m venv .venv && source .venv/Scripts/activate   # Windows'ta Git Bash; Linux/macOS'ta .venv/bin/activate
pip install -r requirements-dev.txt
pytest && ruff check .
```

CI (GitHub Actions) her push'ta ruff, pytest, `check_flags.py` ve `build_index.py --check` çalıştırır.

## Uyduğum kurallar

- Yalnızca yasal hedefler: kasıtlı olarak zafiyetli makineler, saldırmama izin veren platformlardaki
  challenge'lar veya kendi laboratuvarım. Başka hiçbir şey, asla.
- Canlı flag yok. Flag'ler gizlenir (`THM{...}`) ve `check_flags.py` bunu denetler.
- Platformların writeup yayınlama kuralları önce gelir:
  - **HackTheBox**, aktif makineler ve challenge'lar için writeup yayınlamayı yasaklar. Yalnızca emekli (retired) içerik yayınlarım.
  - **TryHackMe** ve **picoCTF**'in kendi kuralları var ve değişebiliyor. Yayınlamadan önce her oda
    veya yarışma için güncel şartları kontrol ederim; bir oda writeup yazılmamasını istiyorsa yazmam.
- Bana yardımcı olan her writeup'ı, yazıyı veya aracı kaynak olarak belirtirim.

## Bunu neden tutuyorum

Güvenliğe yeni başlayan bir üniversite öğrencisiyim. Bir challenge'ı kendi cümlelerimle yazmak,
her adımın neden çalıştığını anlamaya zorluyor, dönüp bakacak bir şey bırakıyor ve sırada neyi
çalışmam gerektiğini görmemi kolaylaştırıyor. Bu bir öğrenme günlüğüdür, skor tablosu değil.

## Lisans

Kod (`tools/`, `tests/` ve CI yapılandırması) [MIT Lisansı](LICENSE) altındadır.
Writeup metinleri ve notlar [CC BY 4.0](LICENSE-CONTENT.md) altındadır.
