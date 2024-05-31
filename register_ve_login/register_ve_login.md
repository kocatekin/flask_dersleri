# Register ve Login


Geçtiğimiz derslerde öğrendiklerimizi şimdi deneme vakti geldi. İlk olarak veritabanı tablomuzu düşünelim.

Bir *user_id* olacak, *kullanıcı_adı* olacak, *sifre* olacak, ve *salt* olacak. Şimdilik en basit yöntem bu. Elbette ki buna *kayittarihi* vb. gibi şeyler de ekleyebiliriz, ancak amacımız nasıl yapıldığını anlamak. Çünkü 4 elemanlı bir tablo yaratabiliyorsak, altı elemanlı da yaratabiliriz.

Veritabanı şemamız cepte. Şimdi site düzenini düşünelim. İlk olarak *index* ekranı geliyor. Bu ekranda 2 tane link olsun şimdilik, bir tanesi **Kayıt Ol** diğeri de **Giriş Yap** olsun.

O halde, 3 tane *html* dosyası gerekiyor:
* index.html
* kayitol.html
* girisyap.html

Bunları yapmaya başlamadan önce de sistemimizi düşünelim. Kullanıcı *kayitol.html* adresine geldiği zaman, orada bir form karşılayacak. Bu form nereye *submit* edecek? Verileri hangi *endpoint* e gönderecek? Bu işlem için `/register` endpointini kuralım. 

Aynı şekilde, *girisyap.html* icin de bir form yaratacağız ve bunun *submit*'i de `/login` endpoint'ine gidecek.

O zaman ilk olarak html dosyalarını yazalım. Burada hiç *css* yazmayacağız şimdilik.

```html
<!-- index.html -->
<a href='/kayitol'>Kayıt Ol</a>
<a href='/girisyap'>Giriş Yap</a>
```
```html
<!-- kayitol.html -->
<form action="/register" method="post">
    kullanıcı adı:<input type="text" name="username" required> <br>
    şifre: <input type="password" name="sifre" required> <br>
    <input type="submit">
</form>
``` 

```html
<!-- girisyap.html -->
<form action="/login" method="post">
    kullanıcı adı:<input type="text" name="username" required> <br>
    şifre: <input type="password" name="sifre" required> <br>
    <input type="submit">
</form>
```

HTML sayfalarımızı hazırladık. Bunları **templates** klasörünün içerisine koyacağız. 

Bu klasörleri ve kodu repo içerisinde bulabilirsiniz.
    

