# Sqlite

İstemci tarafından, sunucu tarafına veri aktarımını gördük. Bunun elbette tek yolu form kullanmak değil, ancak şimdilik bu şekilde ilerleyelim. Bu verileri aktardıktan sonra eğer ekrana yazdırabiliyorsak, onun üzerinde işlemler de yapabiliriz demektir. Bu işlemlerin en yaygınlarından bir tanesi de veritabanı işlemleri. 

Genellikle tüm tutorialların ilk başladığı yer **CRUD** uygulamalarıdır. Bu kısaltma aslında şu kelimelerin kısaltması: Create, Read, Update ve Delete. Yani oluştur, oku, güncelle ve sil. Çünkü veritabanı içeren temel bir uygulamanın yaptığı en atomik işlemler bunlardır. Örneğin bir Todo uygulaması düşünelim. Yeni bir Todo ekleriz, okuruz, güncelleriz ve silebiliriz. Yeni başlarken, işlemlerinizde çoğunlukla *silme* işlemini ikinci planda bırakmanızı öneriyorum. Eğer kod mantığında bir hata yaparsanız, o zaman geri dönülemeyecek bir şey yapma ihtimaliniz yüksek. O yüzden şimdilik örneklerimizde *silme* işlemini ikinci planda bırakacağız.

Todo uygulamasına geçmeden önce az da olsa veritabanı ile ilgili konuşalım ve bir veritabanı oluşturmayı görelim. Python, *Sqlite3* ile birlikte geliyor. Sqlite, sunucu gerektirmeyen bir ilişkisel veritabanı yönetim sistemidir (RDBMS). C programlama dilinde yazılmıştır. Çoğunlukla *yerel depolama* ya da küçük ölçekli web siteleri için kullanılmaktadır, ancak teknolojinin ilerlemesi ve disklerin de hızlanmasıyla artık *production* seviyesinde de kullanım örnekleri bulabilmektedir. (Ek bilgi için bkz. https://highperformancesqlite.com/)

Sqlite, her platformda çalışabilir ve veritabanını `*.db` uzantılı tek bir dosyada saklar. Bu şekilde erişim çok daha hızlı ve basit olur, kurulumu da aynı şekilde kolaydır. Basit, kişisel uygulamalar için kullanışlı olduğu için prototipler için de kullanışlı olacaktır. 

Python ile sqlite kullanmak gayet kolay. `import sqlite3` diyerek gerekli kütüphaneleri ekleyerek başlayabiliriz. İlk olarak bir Todo uygulaması yapalım demiştik, o halde tek kullanıcıya sahip olan bu Todo uygulamasının veritabanı şemasını düşünelim. Bu arada, bu programları yazarken ORM (Object Relation Model) kullanmayacağız, *raw* SQL komutları ile ilerleyeceğiz.

Çok basit bir todo uygulaması düşünelim, zamanla bunları başka programlarda geliştirerek de kullanacağız. Öncelikle tablomuzda nelere ihtiyacımız var? Bir `id`, `icerik`, `yapildimi` seklinde uc tane sütun bizim için yeterli olacaktır. Sqlite, basit bir veritabanı olduğu için sütunların veri türleri de aynı şekilde çok komplike olmayacak. Bunlar RDBMS'e göre değişkenlik gösterebilirler. Detaylar için kullandığınız RDBMS'i iyi öğrenmeniz gerekir. Ancak bizim amacımız şu an Flask öğrenmek.

Sqlite içerisinde kullanabildiğimiz veri türleri NULL, INTEGER, REAL, TEXT ve BLOB. (bkz. https://www.sqlite.org/draft/datatype3.html)

