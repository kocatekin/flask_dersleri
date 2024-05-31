# Sqlite

İstemci tarafından, sunucu tarafına veri aktarımını gördük. Bunun elbette tek yolu form kullanmak değil, ancak şimdilik bu şekilde ilerleyelim. Bu verileri aktardıktan sonra eğer ekrana yazdırabiliyorsak, onun üzerinde işlemler de yapabiliriz demektir. Bu işlemlerin en yaygınlarından bir tanesi de veritabanı işlemleri. 

Genellikle tüm tutorialların ilk başladığı yer **CRUD** uygulamalarıdır. Bu kısaltma aslında şu kelimelerin kısaltması: Create, Read, Update ve Delete. Yani oluştur, oku, güncelle ve sil. Çünkü veritabanı içeren temel bir uygulamanın yaptığı en atomik işlemler bunlardır. Örneğin bir Todo uygulaması düşünelim. Yeni bir Todo ekleriz, okuruz, güncelleriz ve silebiliriz. Yeni başlarken, işlemlerinizde çoğunlukla *silme* işlemini ikinci planda bırakmanızı öneriyorum. Eğer kod mantığında bir hata yaparsanız, o zaman geri dönülemeyecek bir şey yapma ihtimaliniz yüksek. O yüzden şimdilik örneklerimizde *silme* işlemini ikinci planda bırakacağız.

Todo uygulamasına geçmeden önce az da olsa veritabanı ile ilgili konuşalım ve bir veritabanı oluşturmayı görelim. Python, *Sqlite3* ile birlikte geliyor. Sqlite, sunucu gerektirmeyen bir ilişkisel veritabanı yönetim sistemidir (RDBMS). C programlama dilinde yazılmıştır. Çoğunlukla *yerel depolama* ya da küçük ölçekli web siteleri için kullanılmaktadır, ancak teknolojinin ilerlemesi ve disklerin de hızlanmasıyla artık *production* seviyesinde de kullanım örnekleri bulabilmektedir. (Ek bilgi için bkz. https://highperformancesqlite.com/)

Sqlite, her platformda çalışabilir ve veritabanını `*.db` uzantılı tek bir dosyada saklar. Bu şekilde erişim çok daha hızlı ve basit olur, kurulumu da aynı şekilde kolaydır. Basit, kişisel uygulamalar için kullanışlı olduğu için prototipler için de kullanışlı olacaktır. 

Python ile sqlite kullanmak gayet kolay. `import sqlite3` diyerek gerekli kütüphaneleri ekleyerek başlayabiliriz. İlk olarak bir Todo uygulaması yapalım demiştik, o halde tek kullanıcıya sahip olan bu Todo uygulamasının veritabanı şemasını düşünelim. Bu arada, bu programları yazarken ORM (Object Relation Model) kullanmayacağız, *raw* SQL komutları ile ilerleyeceğiz.

Çok basit bir todo uygulaması düşünelim, zamanla bunları başka programlarda geliştirerek de kullanacağız. Öncelikle tablomuzda nelere ihtiyacımız var? Bir `id`, `icerik`, `yapildimi` seklinde uc tane sütun bizim için yeterli olacaktır. Sqlite, basit bir veritabanı olduğu için sütunların veri türleri de aynı şekilde çok komplike olmayacak. Bunlar RDBMS'e göre değişkenlik gösterebilirler. Detaylar için kullandığınız RDBMS'i iyi öğrenmeniz gerekir. Ancak bizim amacımız şu an Flask öğrenmek.

Sqlite içerisinde kullanabildiğimiz veri türleri NULL, INTEGER, REAL, TEXT ve BLOB. (bkz. https://www.sqlite.org/draft/datatype3.html)

O halde biz `id` için INTEGER, `icerik` icin TEXT ve ayni zamanda `yapildimi` icin de INTEGER kullanacağız. Normal şartlarda bu `yapildimi` alanı bir flag olacağı için BOOLEAN olacaktı, ancak elimizde BOOLEAN mevcut değil.

O halde, bir Sqlite veritabanı oluşturan bir Python kodu yazalım.

```python
import sqlite3

def db_olustur():
  conn = sqlite3.connect("todo.db")
  c = conn.cursor()
  c.execute('CREATE TABLE IF NOT EXISTS todo(id INTEGER PRIMARY KEY AUTOINCREMENT, icerik TEXT NOT NULL, yapildimi INTEGER NOT NULL DEFAULT 0)')

  conn.commit()
  conn.close()

if __name__ == "__main__":
  db_olustur()
```

Şimdi kodun üstünden geçelim. İlk olarak `sqlite3` kütüphanesini ekledik. Ardından, `db_olustur()` adında bir fonksiyon tanımladık. Bu fonksiyon, `sqlite3.connect()` fonksiyonunu çağırıyor. Bu fonksiyonun içine de yaratmak istediğimiz veritabanının adını yazdık. 

İlk olarak bir bağlantı oluşturuyoruz `connect()` komutuyla. Ardından, veritabanı ile iletişime geçebilmek için bir *interface* (arayüz) olan `cursor` objesini oluşturuyoruz. Veritabanı ile bağlantıyı bu obje sayesinde kuracağız. Artık örnekteki `c` objemiz bizim cursor'ımız. Ardından, bunu kullanarak veritabanına bir komut veriyoruz. Bu komut, `CREATE TABLE` komutu. Burada da gördüğümüz gibi aslında raw SQL yazmış olduk.

Bu programı çalıştırdıktan sonra, göreceğimiz üzere artık bir veritabanımız olacak. Bu veritabanına da bağlanıp bir şeyler yapmak istediğimizde, Flask kodumuzun içerisinde bu veritabanına aynı şekilde bağlanacak, bir cursor oluşturacak ve ardından komutlar gireceğiz.

Şimdi, bu yazdığımız dosyanın içerisine birkaç tane de Todo ekleyelim. Sonra da yeni bir Python dosyası yaratıp, bu veritabanını okumayı öğreneceğiz. İleride de bunun aynısını Flask üzerinde yapacağız. 

İlk yapacağımız şey, yukarıdaki koda `insert` komutları ekleyerek birkaç tane Todo yaratmak. Ardından da, yazdıklarımızı okuyalım diye yeni bir fonksiyon ekleyeceğiz.

```python
import sqlite3

def db_olustur():
  conn = sqlite3.connect("todo.db")
  c = conn.cursor()
  c.execute('CREATE TABLE IF NOT EXISTS todo(id INTEGER PRIMARY KEY AUTOINCREMENT, icerik TEXT NOT NULL, yapildimi INTEGER NOT NULL DEFAULT 0)')

  conn.commit()

  c.execute('INSERT INTO todo(icerik, yapildimi) values (?,?)', ("ekmek al", 0))
  c.execute('INSERT INTO todo(icerik, yapildimi) values (?,?)', ("icecek al", 0))
  conn.commit() #eger commit etmezsek, bunlar islem gormex
  conn.close()

def db_oku():
  conn = sqlite.connect("todo.db")
  c = conn.cursor()
  c.execute("select * from todo")
  rows = c.fetchall() #tum donen degerleri al
  print(rows)


if __name__ == "__main__":
  db_olustur()
  db_oku() #olusturduktan sonra o fonksiyon bitince, buna gececek.
```

Burada dikkat edilmesi gereken birkaç nokta var. Örneğin, `select` komutundan sonra bir `commit` yapmadık, çünkü aslında veritabanı üzerinde bir değişiklik yapmıyoruz. Bu yüzden o aşamada gerek yok.

Bununla birlikte, bu kod *refactoring*e açık. Örneğin veritabanı adını elle veriyoruz, bunu yukarıda global bir değişken olarak verebiliriz. Ya da veritabanı bağlantısını ve cursor oluşturma işlemini iki kez yapıyoruz, keza bunu da ayrı bir fonksiyon içerisinde verebiliriz `db_baglan()` gibi. 

Bunun yanısıra, `id` ile ilgili herhangi bir işlem yapmadık. Çünkü **AUTOINCREMENT** olduğu için, onu vermesek bile veritabanı onu artırıp, gerekli olan `id` atamasını yapacak.

Şimdi bu kodu biraz refactor edelim, ve Flask çalışmalarına devam edelim. Final kodu repository içerisinde bulabilirsiniz.
