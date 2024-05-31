# Şifre saklama

Bir web sitesinde kullanıcıların giriş bilgilerini saklamak önemli bir konu, ancak çoğu zaman görmezden geliniyor. Özellikle büyük frameworkler ile çalışıldığı zaman, bu problemler otomatik olarak çözülse de, bunların nasıl çalıştığını anlamak bir developer için önemli. O yüzden bu yazıda, şifre saklama işlemlerinin nasıl yapılacağından bahsedeceğim.

Öncelikle yanlış olanlardan başlayalım. Şifreler, *plaintext* yani açık metin olarak saklanmamalıdır. Çünkü bu şekilde saklanırsa, hem o site yöneticisi bu şifreleri rahatlıkla görebilir, hem de olası bir saldırıda veritabanı eğer çalınırsa, şifreler saldırganlar tarafından otomatik olarak görülebilir. Eğer kullanıcılar, aynı şifreyi birden fazla sistem üzerinde kullanıyorlarsa, bu da ciddi bir sorun teşkil eder. Özellikle eskiden, *şifremi unuttum* seçeneğine tıkladıktan sonra, şifremiz bize mail yoluyla gelirdi. Bu, şifrenin aslında *plaintext* olarak saklandığını gösterir ve böyle bir siteden koşarak uzaklaşmak gerekir. Başka yazılarda, web güvenliği ile ilgili ayrıca bahsedeceğim.

Şifreleri saklamak için akla ilk gelen teknik *şifrelemek* olsa da, şifreleme işlemi beraberinde ek sorunlar da getirir. Örneğin *anahtar belirleme*, *anahtar saklama* (key establishment, key management) gibi. 

Bu yüzden, şifre saklamak için şifreleme tekniklerini değil, **hashleme** (özetleme) fonksiyonlarını kullanırız. 

## Hash Fonksiyonları

Eğer bilgisayar bilimleri eğitimi aldıysanız, o zaman hash fonksiyonlarını duymuşsunuzdur. Örneğin *hash map* yapısı bu fonksiyonlara dayanır. Ancak bizim kriptografik işlemler için kullanacağımız hash fonksiyonları, daha özel fonksiyonlar. Bunlara kısaca CHF (*Cryptographic Hash Function*) adı veriliyor. Bu fonksiyonlar belli özellikleri sağlamalılar.

```
todo
```

Hash fonksiyonları, değişken boyutlu bir girdiyi alır ve sabit boyutlu bir çıktı geri döner. Yani, hash fonksiyonuna hangi metni verirseniz verin, ne kadar uzun ya da kısa olursa olsun, fonksiyonun çıktısı hep aynı uzunlukta olacaktır. Bu uzunluk, kullandığımız hash fonksiyonuna göre değişiklik gösterir. Bu çıktıya da *hash*, *digest* ya da *hash değeri* isimleri verilebilir. 

Bundan sonra hash fonksiyonu dediğimde, aslında CHF'den bahsediyor olacağım.

Hash fonksiyonlarının temel özelliği, **tek yönlü** fonksiyonlar olmalarıdır. Bahsettiğimiz gibi, *hash değeri* bir çıktıdır. Bu çıktıya bakarak, girdiyi tahmin etmek **imkansızdır**. Dolayısıyla, bir *hash* e sahip olmanız, girdi hakkında size hiçbir bilgi sunmaz. Biz, hash fonksiyonlarının bu özelliğini kullanarak şifreleri saklayacağız. Peki bunun için hangi hash algoritmasını kullanabiliriz?

Neyse ki, NIST (National Institute of Standards & Technologies) isimli kurulum, tüm dünyanın kullanabilmesi için kriptografik standartlar belirliyor. Örneğin *simetrik şifreleme* için **AES**'i belirlediği gibi, CHF için de **SHA**'yı seçmiş durumda. SHA, yani *Secure Hash Algorithm* aslında bir **aile** olarak geçiyor. Yani SHA ailesi. Bunlar, SHA-0, SHA-1, SHA-2 ve SHA-3 olarak temelde dörde ayrılırlar. Bunlar arasında detaya girmeden, SHA2 nin (SHA256 ve SHA512) nin kullanıldığını söyleyebiliriz. Bu algoritma **TLS**, **SSH** ve **IPSec** alanlarında ve hatta Bitcoin kriptosisteminde de *Proof of Work* için kullanılmaktadır. 

İsminden de anlaşılabileceği gibi, SHA256 algoritması çıktı olarak 256 bit verir, SHA512 algoritması da çıktı olarak 512 bit verir. Bunları da hexadecimal olarak düşünürsek, çıkan *string* uzunluğu `256/4` yani 64 olacaktır. 

---

Şu aşamaya kadar, şifrelerin *plaintext* olarak saklanmayacağını, yani hiçbir şekilde açık durmaması gerektiğini öğrendik. Bunun ardından, bu şifrelerin aslında **tek yönlü** bir hash fonksiyonundan geçip, çıktısının saklanması gerektiğini öğrendik. Bu aslında yeterli değil, ve şimdi neden yeterli olmadığından bahsedelim.

Diyelim ki 3 adet kullanıcımız var: Ahmet, Mehmet ve Ayşe. Bu üç kullanıcının da şifresi 123456 olsun. Biz, *güvenli* olması amacıyla bu şifreleri önce bir hash fonksiyonundan geçirdik `SHA256('123')` ve çıktısını veritabanına yazdık. Bu aşamada, bu işlemlerin Python ile nasıl yapılacağını da örneklerle gösterelim.

```python
import hashlib

sifre = "123456"
araform = hashlib.sha256(sifre.encode('utf-8'))
digest = araform.hexdigest()
print(digest)
# 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
```

Kodu çalıştırdığınızda da göreceğiniz gibi, artık elimizde bir *hash* ya da *digest* değeri mevcut. Biz, `123456` yerine, veritabanımızda bu `8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92` değeri tutacağız. Ancak, hash fonksiyonlarının yerinde bir özelliği de şu ki, **aynı** girdiyi verdiğinizde, **aynı** sonucu dönmesini bekleriz. Yani, ben bu fonksiyona hangi makinede, hangi dilde, hangi implementasyonda olursa olsun, `123456` değerini verirsem, çıktısı hep `8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92` olmalıdır.

O halde, veritabanında her kullanıcı için aynı *digest* duracak. Peki bu nasıl bir sorun yaratabilir?

Bir kişi veritabanını çaldığı zaman, eğer aynı hash görüyorsa, otomatik olarak bu kullanıcıların **aynı** şifreye sahip olduğunu anlayabilir. Hala matematiksel olarak geri dönemez, ancak bunu kırmak için bir saldırı yapacaksa, artık deneyeceği potansiyel şifrelerin sayısı ciddi anlamda azalacaktır. Yani aslında bu hashleri kırmak için (daha sonra nasıl yapılacağından bahsedeceğiz) harcayacağı zaman ciddi şekilde azalacaktır. 

Güvenlik açısından unutmamamız gereken önemli bir konu şu; hiçbir zaman karşı tarafa gereğinden fazla bilgi vermemeliyiz. Örneğin şu an, bu kullanıcıların şifrelerinin **aynı** olduğu bilgisini fark etmeden verdik. O halde, buna bir önlem almalıyız. Bu önlemin adı **tuzlama** (salting).

Her kullanıcı sisteme kayıt olurken (*register*), her kullanıcı için rastgele bir **tuz** belirleyeceğiz. Bu aslında random olarak seçtiğimiz bir string olacak. Ardından, kullanıcının verdiği şifreye bu tuzu ekleyeceğiz, ve *hashleme* işlemini bu yeni veri üzerine yapacağız. Yani `sha256(sifre)` yerine, `sha256(sifre+tuz)` şeklinde oluşturacağız yeni *hash* değerimizi ve bunu saklayacağız. Bu şekilde, kullanıcılar *aynı* şifreye sahip olsalar bile, artık veritabanında aynı şifre gözükmeyecek.

Peki, tuz bilgisi nerede duracak? Tuz bilgisi, *gizli* bir bilgi değil. Veritabanında yeni bir sütun oluşturarak, onu orada açık şekilde saklayabiliriz. Veriler eğer çalınırsa, saldırgan ona sahip olacak ve denemelerini yine yapabilecek evet, ancak ciddi bir zaman dezavantajına uğradığı gibi, artık bir önceki durumda sahip olduğu avantajları da kaybetmiş olacak. Çünkü tuzları görse bile, şifrelerin aynı olup olmadığını anlayamaz.

Bu aşamada, biraz opsiyonel olarak görülebilen bir ek aşama daha var. O da **biberleme** aşaması. Şimdi tuzlamayı anlattık, amacını da söyledik. Her kullanıcı için ayrı bir *tuz* belirleniyor, ve bunlar veritabanında o kullanıcının satırında saklanıyor. Ancak, bir de veritabanında saklamadığımız bir **biber** oluşturup, bunu da `şifre+tuz` a ekleyebiliriz. Ancak bu biber, veritabanında saklanmayacak, belki bir *ortam değişkeni* ya da server üzerindeki bir *dosyada* ya da güvenliğe aşırı önem veriyorsanız *şifrelenmiş* bir şekilde saklanacak. Böylelikle, veritabanı çalınsa bile, saldırgan **biber** nedir bilmediği için kırma işlemine başlayamayacak.

Burada şunu yapıyoruz, kullanıcı kayıt olurken tuz oluşturduk ve şifreye ekledik ya; şimdi bir de biberi alıp onu ekliyoruz. Yani veritabanındaki hash, `sifre+tuz+biber` in hashlenmiş hali olacak.



---

Şu aşamada, artık şifrelerimiz açık şekilde veritabanında durmuyor, ve aynı şifreye sahip olan kullanıcıların da şifreleri farklı gözüküyor. Bu güvenlik için gayet iyi. Ancak, SHA algoritması NIST tarafından seçilirken, *hızlı* olmasına dikkat edildi. Çünkü bu SHA, sadece *şifre saklama* amacıyla kullanılmıyor, kendisi kriptografik bir hash fonksiyonu. Bu yüzden, ek bazı önlemler almamız gerekiyor. Ancak bu önlemleri **neden** aldığımızı anlamak için, şimdi bu hashlerin nasıl kırılabileceğini görmeliyiz.

## Saldırı metodları

Eğer elimizde hashlenmiş metodlar varsa, temel olarak üç adet saldırı yöntemimiz var. Tuzlama işlemi yaptığımız için bu saldırı metodları 2'ye düşecek. Kaybettiğimiz tekniğe biz *rainbow table* adı veriyoruz. 

### Rainbow tables

SHA2, kapalı bir algoritma değil. Nasıl çalıştığı biliniyor. Tek yönlü bir fonksiyon olması nedeniyle, eğer elimizde bir *digest* varsa, onu orjinaline döndüremiyoruz. Ancak, eğer yeterince zamanımız varsa, insanların *şifre* olarak kullanması muhtemelen tüm verilerin hepsini *hashleyebilir* ve bunları bir veritabanında saklayabiliriz. 

Örneğin, 123456 çok yaygın kullanılan bir şifre olsun. O halde ben bunu hashlerim ve: `123456 -> 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92` olarak tutabilirim. Bunu, potansiyel her şifre için yaptığımı düşünün. O zaman, bu fonksiyon **tek yönlü** olsa bile, benim elimde tüm hashlerin karşılık geldiği orijinal verilerin tablosu olduğu için, direkt olarak bir *lookup* yapabilirim. 

Şu an literatürde sıklıkla kullanılan şifrelerin listesi var. Bu listeyi alıp, çok basit bir Python programı kullanarak hepsini hashleyebilir ve bir veritabanında saklayabilirsiniz. Ardından, eğer size gelen *digest* bu listedeki bir şifrenin *digest*i ise, bunu da rahatlıkla o veritabanından bakıp bulabilirsiniz. 

Tuzlama işleminin yararlarından biri de budur. Şifreniz `123456` olsa bile, artık `123456sf040g2` olarak hashleneceği için, bunu öngörerek o tabloya eklemek zor olacaktır.

## Brute-Force saldırıları

Kısaca tüm şifre kombinasyonlarını tek tek deneme işlemidir. Bu daha akıllıca bir şekilde de yapılabilir, böyle yapıldığı zaman ona **dictionary attack** ya da **sözlük atakları** ismini veriyoruz. Diyelim ki veritabanını ele geçirdik, elimizde *hash* değerleri ve *tuz* değerleri var. O zaman, daha önce sıklıkla kullanılmış şifrelerin hepsini alıyoruz, bunlara *tuz* ekliyoruz ve aynı hash'i bulmaya çalışıyoruz. 

En primitif yöntemi bu. Bunun bir gelişmiş hali, spesifik olarak bir kullanıcının şifresini kırmak istiyorsak, o kullanıcıya ait kişisel bilgilerden bir sözlük oluşturmak. Bu sefer belirli programlar, tüm bu sözlük içerisindeki verilerle türlü kombinasyonlar oluşturup, bunları şifre olarak deneyebiliyorlar. Örneğin doğumgünü, aile bilgisi, tuttuğu takım, evcil hayvan gibi bilgilerin hepsini türlü kombinasyonlar oluşturup deneyebiliyorlar. 

O halde, bu deneme işlemleri ne kadar hızlıysa, saldırganın işi o kadar kolay demektir. Bu, elbette kullanıcı için bir dezavantaj. Dediğim gibi, SHA256 hızlı bir algoritma olduğu için, denemesi de gayet hızlı oluyor. İşte bu yüzden, aslında yukarıda anlattığımız metod zamanla yetersiz hale geldi, bunu yeterli hale getirmek için, bu işlemi defalarca yapmaya başladılar. Biz, örneğimizde 1 kere hash işlemi yaptık. Bunu 100.000 kere yaparsak?

İşte bunu yapmak için, artık KDF (*Key Derivation Function*) ler kullanacağız. Bunlar, *anahtar üretme fonksiyonlarıdır*. Bu fonksiyonların temel amacı, **simetrik şifreleme** için kullanılacak anahtarları üretmektir. Ancak şimdi, daha farklı bir şekilde, şifre saklamak için kullanacağız. 

KDF'ler, kullanıcıların şifrelerini kullanarak bir şifreleme anahtarı üretirler. Özelliklerinden bir tanesi, çıktının uzunluğunu ayarlayabiliyor olmamızdır. KDF'e örnekler **PBKDF2**, **scrpyt** ve **argon2** olarak gösterilebilir. Şifre saklamak için yaygınlıkla kullandığımız **bcrypt**, teknik olarak bir KDF değildir, çünkü çıktı uzunluğu ayarlanamaz.

Örneğin, PBKDF2'ye göz atalım. Bu fonksiyon, 4 tane input alır: kullanıcı şifresi *pwd*, tuz *S*, istenen çıktı uzunluğu *len* ve sayaç *c*. Aslında gördüğümüz gibi, yine bir tuz var, yine şifre var. Ancak 2 tane yeni parametre geldi. Bunlar, çıktının uzunluğu ile (çünkü hash fonksiyonunda bu fiks bir sayıydı), *iterasyon* sayısı. Yukarıda sadece 1 kere döndük, ancak 100000 kere de dönebiliriz. 

İşte, KDF'ler, developer'a bu konuda kolaylık sağlıyorlar. Aynı zamanda da hashleme işlemini *CPU-intensive* bir hale getiriyorlar. Yani, bu işlemi yapmak için kullanılan *işlem sayısını* arttırıyorlar. Bu şekilde de saldırganın işi daha da zorlaşıyor.

Ancak burada bir *tradeoff* söz konusu. Eğer şifreyi hashleme işlemi çok uzun sürerse, bu sefer kullanıcının *login* süreci de uzayacaktır. Burada iterasyon sayısını belirlerken buna dikkat etmek gerekir.

---

### bcrypt

Şifre saklama amacıyla, yukarıda belirttiğimiz KDF'lerden herhangi birini kullanabiliriz. Ancak, *bcrypt* bir KDF olmasa bile, şifre saklamak için özel üretilmiş fonksiyonlardan bir tanesidir. Biz, örneklerimizde *bcrypt* kullanacağız ve şimdi bunun nedenlerinden bahsedelim.

Bcrypt, 3 adet parametre alır. Bunlar bir *cost* parametresi, *sifre* parametresi ve *tuz* parametresidir. Şifre ve tuz parametreleri aşikar, cost parametresi ise aslında *maliyet* parametresidir. Bcrypt, 192-bitlik bir hash çıktısı verir.

Peki, SHA256 bile 256bitlik bir çıktı veriyordu. Ben istersem SHA'yı 100bin kez çalıştırabilirim. Neden bcrypt kullanmalıyım? 

Çünkü bcrypt **özellikle** şifre saklamak için tasarlanmış bir algoritma. Hatırlarsanız, SHA'nın *hızlı* olduğunu söylemiştik. İşte bcrypt, bilinçli olarak yavaş işlem yapmaktadır. Bu da saldırı süresini uzatmakta yardımcı olur.

---

    Ek bilgi olarak şunu da söylemeliyim. Bu yukarıda en son eklediklerimiz aslında dediğim gibi *CPU-intensive* yöntemler. Artık işlemciler ucuzladığı için, bu sistemlerin kırılması yine kolaylaştı. O yüzden **memory hard** fonksiyonlar dediğimiz fonksiyonlar ortaya çıktı. Artık, şifre saklama konusunda altın standart **Argon2** dir. 

---

Biz, her şeyi sıfırdan yapmayı planladığımız için basit bir *salt* işlemi ile *sha256* kullanacağız. Burada bunları nasıl oluşturacağımızın bir örneğini yaptıktan sonra, başka bir derste bir kullanıcı tablosu oluşturup oraya kullanıcı kaydı yapacağız.

```python
import hashlib
import secrets

def tuz_olustur(uzunluk=12):
    return secrets.token_hex(uzunluk // 2)

username = input("\n kullanici adi girin: ")
sifre = input("\n sifre girin: ")

tuz = tuz_olustur()
digest = hashlib.sha256((sifre+tuz).encode('utf-8')).hexdigest()
print(digest)
```

Burada, bir tuz oluşturma fonksiyonu yaptık, ardından kullanıcıdan *username* ve *sifre* aldık. Şifreye rastgele tuzumuzu ekledik, ardından onu *byte* formatına çevirip en sonunda da *digest*e ulaştık. Bu arada, yukarıdak işlemi sürekli yapmamak için, `hash_olustur(sifre,tuz)` diye bir fonksiyon yapabiliriz. Hatta, Python'da bunu ayrı bir dosya olarak yapıp *import* edebiliriz de. Örneklerde bunu kullanacağız.

Burada `secrets` kütüphanesini kullandık, çünkü bu şekilde bir *rastgelelik* gerekiyorsa `random` yerine onu kullanmamız gerekiyor. Bunun için başka bir derse yönlenebiliriz. (todo)

Bir sonraki derste, artık bir **register** ve **login** sistemi yapacağız.












