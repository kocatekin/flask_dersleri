# Formlar

Bir önceki derste, sunucu tarafından istemciye nasıl bilgi aktarılacağını gördük. Biz sunucu tarafında istediğimiz işlemleri yapıp, kullanıcının neler göreceğini kontrol edebiliyoruz.

Ancak web sistemlerindeki bir diğer önemli şey ise, istemci tarafından sunucu tarafına bilgi göndermek. Bunu iki şekilde yapabiliriz: **form** ya da **ajax**.

Bu dersler içerisinde **ajax** yaklaşımını görmeyeceğiz. Ancak en kısa şekilde bahsedersek, Javascript kullanarak (`fetch()` API) sunucudan veri çekebilir ve sunucuya veri gönderebiliriz. Biz ise şimdi **form** yaklaşımını göreceğiz.

```html
<form action='/gonder' method="post">
    <input type="text" name="metin">
    <input type="submit">
</form>
```

Bu, bize sadece bir tane *text input* sağlayan bir form. Bir tane de *submit* butonu olacak, yani **gönder** butonu. 

Bu butona bastığımız zaman, `action` attribute'una bağlı olan endpoint'e istek gidecek. O endpoint, bu örnekte `/gonder`. Bu isteği de **POST** metodu ile gönderecek. Bunu **GET** olarak da yapabiliriz, ancak şimdilik POST örneklerini görelim. İleride **GET** örneklerini de göreceğiz.

Ancak sunucu tarafında bir kod yazmasanız bile, bu method'u değiştirerek denerseniz aralarındaki fark ile ilgili fikir elde edinebilirsiniz. Biz bu farkları daha sonra konuşacağız.

## Sunucu tarafı

Ön tarafın kodunu hallettik. Bu kodu `form.html` diye kaydederek, `templates` klasörünün içine koyalım. Şimdilik bu tam bir HTML değil ancak önemli değil, isterseniz tam teşekküllü bir HTML sayfası da yapabilirsiniz.

Şimdi ise, sunucu tarafında gereken kodu yazalım. Burada yapmamız gereken, istemcinin *form*a yazdığı veriyi almak ve ekrana yazdırmak. Eğer bunu yapabilirsek, o veriyi alabiliyoruz ve işlem yapabiliyoruz demektir. Yani aslında bunu yapabildiğimiz an, o veriyi bir fonksiyona parametre olarak da verebiliriz, onunla oynayabiliriz, vb. 

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("form.html")

@app.route('/gonder', methods=['POST'])
def gonder():
    metin = request.form['metin']
    return metin

if __name__ == "__main__":
    app.run(debug=True)
```

Kodun üstünden geçelim. İlk olarak import ettiğimiz şeylerin sayısı arttı. Çünkü artık `render_template` ve `request` modüllerini de kullanıyoruz. Bunlar bize **Flask** tarafından sağlanıyor.

İlk olarak, bunu çalıştırdığımızda `localhost:5000` adresine gidildiğinde, ilk `app.route` a gideceğiz. Orada, `form.html` çalıştırmak istediğimiz için, ve o da **templates** klasörümüzde olduğu için, `render_template` metodunu çağırıyoruz.

Ardından, yeni bir endpoint ayarladık. Form'dan gönderilen veri nereye gidecek? `/gonder` isminde bir endpoint'e. O zaman, sunucu tarafında buna hazır olmalıyız. Burada, *index* üzerinde olmayan yeni bir şey de görüyoruz: `methods=['POST']`. Aslında bu çok yeni değil, çünkü hiçbir şey yazmadığımızda da aslında `methods=['GET']` yazmışız gibi çalışıyordu. Yani başka bir deyişle, eğer POST metodu ile bir şey gönderiyorsak, bu şekilde dinlemeliyiz. Eğer bu şekilde dinlemezsek, **GET** metodunu dinliyoruz demektir, ve POST ile gönderilen şeye yanıt veremeyiz.

Ardından, `request.form` ile veriyi alıyoruz. Burada `metin` yazdık, çünkü gönderen HTML üzerindeki form input'unda `name=metin` yazıyordu. Yani aslında biz orada yazan şeyi koymalıyız ki, sunucu tarafı ne olduğunu anlasın. Çünkü form üzerinde birden fazla veri gönderebiliyoruz, ve göndereceğiz de.

Örneğin biz bu veriyi geri döndürürken, sadece uzunluğunu da döndürebiliriz, ya da onun üstüne bazı şeyler ekleyebiliriz, ya da sonra göreceğimiz gibi kullanıcı girişleri ve çıkışları yapabiliriz.
