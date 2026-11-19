# Web temelleri kontrol listesi

🇬🇧 [English](web-basics-checklist.md)

Yalnızca kasıtlı olarak zafiyetli veya yetkili hedefler için çalışma notları.

## 1. İlk bakış

- [ ] Siteyi tarayıcıda geliştirici araçları (F12) açık şekilde aç. Sayfa kaynağını ve yorumları oku.
- [ ] `/robots.txt`, `/sitemap.xml`, `/.git/`, `/admin`, `/backup`, `/login`.
- [ ] Teknoloji yığınını belirle: cevap başlıkları (`curl -I URL`), hata sayfaları, cookie adları, dosya uzantıları.
- [ ] JavaScript dosyalarına ve Network sekmesindeki API çağrılarına bak; endpoint ve parametreleri listelerler.

## 2. İçerik keşfi

- [ ] Dizin ve dosya brute force (gobuster / ffuf), yığına uygun uzantılarla.
- [ ] Alan adı varsa virtual host'lar ve alt alan adları.
- [ ] Dinamik görünen sayfalarda parametre keşfi.

## 3. Kimlik doğrulama ve oturumlar

- [ ] Belirlediğin ürünün varsayılan kimlik bilgileri (yalnızca kurallar izin veriyorsa).
- [ ] Kullanıcı numaralandırma: "kullanıcı yok" ile "yanlış parola" için farklı mesajlar.
- [ ] Cookie'ler: bayraklar (`HttpOnly`, `Secure`), tahmin edilebilir değerler, JWT'ler (çöz, `alg` ve imza işlemeyi kontrol et).
- [ ] Parola sıfırlama mantığı, kayıt, "beni hatırla".

## 4. Erişim kontrolü

- [ ] IDOR: URL/gövdedeki ID'leri değiştir (`/user?id=1` yerine `2`). Başkalarının verisini okuyabiliyor musun?
- [ ] Normal kullanıcı admin sayfalarına veya admin API'lerine doğrudan erişebiliyor mu?
- [ ] HTTP metodu değiştirme (GET / POST / PUT).

## 5. Girdi işleme (her parametreyi, başlığı ve cookie'yi test et)

| Test | Hızlı deneme | Başarılı olunca görünen |
|------|--------------|--------------------------|
| SQL injection | `'` veya `' OR '1'='1` | SQL hatası, değişen sonuçlar |
| XSS | `<script>alert(1)</script>` | script çalışır / kaçışsız yansır |
| Path traversal / LFI | `../../../../etc/passwd` | dosya içeriği döner |
| Komut enjeksiyonu | `; id` veya `\| id` | komut çıktısı görünür |
| SSRF | kendi sunucuna işaret eden URL parametresi | isteğin dinleyicine gelir |
| SSTI | `{{7*7}}` | `49` görüntülenir |
| Dosya yükleme | uzantısı/türü değiştirilmiş zararsız test dosyası yükle | dosya saklanır ve erişilebilir |

Her seferinde tek şeyi test et ve sadece sayfayı değil, tüm cevabı (durum, uzunluk, süre) izle.

## 6. Araçlar

- Burp Suite Community veya OWASP ZAP: istekleri yakala ve tekrar oynat.
- `curl -i`, `curl -X POST -d 'a=b'`, `curl -H 'Header: value'`, `curl -b 'name=value'`.
- `sqlmap` yalnızca kurallar otomatik araçlara izin veriyorsa; önce elle enjeksiyonu anla.

## 7. Referans

OWASP Top 10, nelere bakacağın için iyi bir haritadır: bozuk erişim kontrolü, kriptografik
hatalar, enjeksiyon, güvensiz tasarım, güvenlik yanlış yapılandırması, zafiyetli bileşenler,
kimlik doğrulama hataları, bütünlük hataları, loglama hataları, SSRF.
