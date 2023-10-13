# rey_inventory
[Application Link](https://rey-inventory.adaptable.app/main/)
# TUGAS 6
## Perbedaan asynchronous programming dan synchronous programming
Perbedaan asynchronous programming dan synchronous programming terletak pada urutan dieksekusinya. Synchronous programming diekesuksi secara berurutan dari atas ke bawah. Asynchronous programming diekesuksi dari atas ke bawah juga, namun bila terdapat fungsi asynchronous, maka fungsi tersebut akan dieksekusi secara independent dengan kode yang ada.

## Paradigma _event-driven programming_
Paradigma event-driven programming adalah cara pemrogaman di mana input dari user akan di handle oleh event handler, yang berarti input dari user akan mempengaruhi jalan kerja dari program yang dibuat. Program yang dibuat tidak berjalan secara linear, melainkan akan merespons input-input dari user. Input dari user inilah yang dinamakan `event`, dan fungsi yang menerima event tersebut dinamakan `event-handler`.
<br>

Contoh penerapannya pada aplikasi `rey_inventory` terletak pada script yang ada di `main.html`. Pada main.html, terdapat baris kode `document.getElementById("button_add").onclick = addProduct`, yang berarti program akan mencari button dengan id berupa **button_add**, lalu ketika tombol tersebut di klik (**on_click**), maka fungsi `addProduct` akan dijalankan

## Penerapan asynchronous programming pada AJAX
Asynchronous programming pada AJAX memungkinkan kita untuk mengirim request ke server tanpa menghentikan / menghalangi eksekusi dari kode utama kita. Salah satu penerapan asynchronous programming pada AJAX adalah dengan menggunakan metode `fetch`. Metode fetch akan mengembalikan `promises` yang kemudian akan di handle oleh event-listener `then`. Selama menunggu respons dari server, program akan tetap berjalan dan menjalankan tugas lain dan akan tetap responsif.

## Perbandingan Fetch API dengan library jQuery
|       **Fetch API**    |    **jQuery**    |
|    :-----------:   |    :-----------:     |
|Merupakan native JavaScript API yang modern dan merupakan bagian dari standar Web Platform API| JavaScript library yang sudah ada dari lama dan digunakan untuk mengsimplify AJAX request, namun bukan merupakan fitur native dari browser|
| Ringan dan tidak memerlukan library atau dependencies tambahan | Merupakan library yang luas yang memungkinkan fitur lain di luar AJAX request |
| Menyediakan lower-level control pada HTTP Request, sehingga membuatnya lebih fleksibel dalam menerapkan request headers, configure requests, dan menghandle responses | jQuery menyediakan interface yang lebih simpel untuk diterapkan, namun kurang pada segi fleksibilitas |

## Pengimplementasian checklist 
1. Saya mengimplementasikan AJAX GET pada cards data item dengan menambah fungsi addProduct pada script seperti berikut
```
    function addProduct() {
        fetch("{% url 'main:add_product_ajax' %}", {
            method: "POST",
            body: new FormData(document.querySelector('#form'))
        }).then(refreshProducts)

        document.getElementById("form").reset()
        return false
    }
    document.getElementById("button_add").onclick = addProduct
```
<br>

2. Lalu, saya membuat fungsi asynchronous bernama refreshProducts yang akan menunggu hasil dari fungsi asynchronous lain bernama getProducts untuk menambah _cards_ baru bila sudah melakukan add Item, dan memasukan _cards_ tersebut ke dalam container dengan id="inventory"
```
  async function getProducts() {
      return fetch("{% url 'main:get_product_json' %}").then((res) => res.json())
  }
  async function refreshProducts() {
        const products = await getProducts()

        let htmlString = "";

        products.forEach(item => {
        htmlString +=
          `<div class='nft'><div class='main'><p class='name'>${item.fields.name}</p><p class='description'>Description: ${item.fields.description} </p><div class='d-flex justify-content-between align-items-center'><div class='btn-group'><a href="add-amount/${item.pk}"> <button type="button" class="btn btn-sm btn-outline-secondary">+</button></a><a href="sub-amount/${item.pk}"> <button type="button" class="btn btn-sm btn-outline-secondary">-</button></a><a href="delete_item/${item.pk}"> <button type="button" class="btn btn-sm btn-outline-secondary">Delete</button></a><a href="edit-product/${item.pk}"> <button type="button" class="btn btn-sm btn-outline-secondary">Edit</button></a></div></div><div class='tokenInfo'><div class='price'><ins>◘</ins><p class='description'>Amount : ${item.fields.amount}</p></div></div><hr /></div></div>`
          console.log(item.pk)
        })
        
        document.getElementById("inventory").innerHTML = htmlString
    }
```
<br>

3. Untuk pengimplementasian AJAK POST, saya membuat fungsi baru pada views.py untuk menambahkan item baru
```
@csrf_exempt
def add_product_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        user = request.user

        new_product = Item(name=name, amount=amount, description=description, user=user)
        new_product.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()
```
<br>

4. Lalu, melakukan routing untuk menghubungkan fungsi tersebut pada urls.py dengan mengimport fungsi tersebut dan menambahkan ke urlpatterns
```
path('create-product-ajax/', add_product_ajax, name='add_product_ajax'),
```
<br>

5. Buat modal yang akan ter-trigger ketika tombol "Add Product by AJAX" ditekan pada main.html
```
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
      <div class="modal-content">
          <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">Add New Product</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
              <form id="form" onsubmit="return false;">
                  {% csrf_token %}
                  <div class="mb-3">
                      <label for="name" class="col-form-label">Name:</label>
                      <input type="text" class="form-control" id="name" name="name"></input>
                  </div>
                  <div class="mb-3">
                      <label for="amount" class="col-form-label">Amount:</label>
                      <input type="number" class="form-control" id="amount" name="amount"></input>
                  </div>
                  <div class="mb-3">
                      <label for="description" class="col-form-label">Description:</label>
                      <textarea class="form-control" id="description" name="description"></textarea>
                  </div>
              </form>
          </div>
          <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="button" class="btn btn-primary" id="button_add" data-bs-dismiss="modal">Add Product</button>
          </div>
      </div>
  </div>
</div>
```

6. Button untuk add product diberikan id="button_add" agar dapat dihubungkan dengan fungsi addProduct() yang ada pada script di main.html

## Melakukan perintah `collectstatic`
Masuk ke virtual environment, kemudian jalankan perintah `python manage.py collectstatic`
# TUGAS 5
## Element selector dan kapan menggunakannya
Selector pada CSS digunakan untuk memilih _tag_ mana yang mau di-_style_. Saat menggunakan CSS, urutan prioritas pemilihan _style_ dari yang tertinggi ke yang terendah adalah inline, internal, dan external. Namun, terkadang kita bisa memiliki lebih dari satu tag yang sama saat menggunakan CSS namun kita ingin tag tersebut memiliki style yang berbeda. CSS Selectors inilah yang memili peran yang sangat penting bila terjadi kasus seperti itu. Contoh CSS Selectors :


```
h1, h2, h3{
    color: red
}
```
ini berarti kita ingin memilih semua h1, h2, dan h3 untuk memiliki warna merah

<br>

```
div > p{
    color: blue
}
```
Ini berarti kita ingin memilih semua elemen p yang mana parentnya adalah div, dan mewarnai semua p tersebut dengan warna biru. Elemen p yang berada di luar div tidak akan terpengaruh

<br>

```
p.class{
    color: red
}
```
Ini berarti kita ingin memilih semua p dengan class: class untuk berwarna merah. Elemen p lain yang tidak memiliki class: class tidak akan terpengaruh

<br>

Selain dari ketiga ini, masih sangat banyak CSS Selectors lainnya, dan setiap CSS Selectors tersebut memiliki fungsinya masing masing agar kita dapat memilih dengan tepat element mana yang mau kita style

<br>

## HTML5 Tag
HTML Tag adalah sejenis _keyword_ yang mendefinisikan bagaimana web browser kita akan menampilkan data yang ingin kita tampilkan. Untuk dokumentasi lengkap dari HTML5 Tags, bisa dibuka pada [link ini](https://www.w3schools.com/TAGS/default.asp).
Beberapa contoh dan kegunaan HTML Tags yang sering digunakan adalah:
1. \<h1>, \<h2>, \<h3>, dst
<br>

    Tags di atas adalah tag Header. Good practice nya, setiap halaman HTML hanya boleh memiliki 1 \<h1>, biasanya sebagai judul utama.

2. \<p>
<br>

    Tag ini digunakan untuk menampilkan paragraf.

3. \<ol>, \<ul>, \<li>
<br>
   Ketiga tag di atas digunakan untuk menampilkan list item. \<ol> untuk menampilkan list yang berurutan (ordered list), dan \<ul> untuk menampilkan list yang tidak berurutan (unordered list) 

<br>

## Perbedaan margin dan padding
Margin dan padding adalah element yang terdapat pada box layout CSS. Kedua element ini sangat berguna untuk menentukan posisi dari container yang kita buat. Padding adalah jarak dari elemen di dalam container ke arah border![padding foto](https://github.com/reyhanwiyasa/rey_inventory/assets/119433464/3877e067-a4a5-49b9-a3f1-3e24b57c4946).

<br>

Margin adalah jarak dari container yang kita buat ke arah luar![margin foto](https://github.com/reyhanwiyasa/rey_inventory/assets/119433464/546f4472-9e09-482e-b5f8-5c9dc935440e).

<br>

## Perbedaan _framework_ CSSS `tailwind` dan `bootstrap` dan kapan menggunakannya
Tailwind dan bootstrap adalah framework CSS yang mempermudah front-end developer dalam membuat komponen-komponen CSS. Perbedaannya terletak pada kemudahan implementasi dan kustomisasi.
Tailwind lebih sulit diimplementasi dibanding bootstrap. Namun, tailwind memungkinkan kustomisasi yang lebih luas dibanding bootstrap. Hal ini membuat tailwind lebih cocok digunakan bila pembuatan website memiliki jangka waktu yang lama. Sebaliknya, bootstrap lebih mudah diimplementasi namun memiliki kekurangan dalam kustomisasi. Hal ini membuat bootstrap lebih cocok digunakan bila pembuatan website memiliki jangka waktu yang pendek.

<br>

## Pengimplementasian checklist
1. Awalnya, saya mencoba untuk menggunakan external CSS dalam tugas kali ini. Namun entah kenapa masih ada problem pada bagian static nya, jadi untuk sekarang saya masih menggunakan internal CSS dalam proses _styling_ nya
2. Untuk kustomisasi halaman register dan login, saya mencari di Google. Lalu saya _copy-paste_ CSS dan HTML nya, dan saya lakukan kustomisasi agar dapat menyesuaikan dengan website yang saya buat
3. Untuk halaman main.html, saya mencari di bootstrap. Sama seperti sebelumnya, saya lakukan _copy-paste_ lalu kemudian saya kustomisasi agar dapat menyesuaikan website.

<br> 
<hr>

# TUGAS 4
## Apa itu Django `UserCreationForm`?
`UserCreationForm` adalah modul bawaan dari Django yang meng-_inherits_ kelas `ModelForm`. Guna dari `UserCreationForm` ini adalah untuk memudahkan pembuatan `form` user, sehingga kita tidak perlu membuat kode agar user dapat register dan login dari awal. Kekurangannya adalah karena modul ini merupakan modul bawaan, jadi modul ini akan mengikuti _customization_ dari Django sendiri. Namun, komponen dari `UserCreationForm` sebenarnya dapat di _break-down_ menjadi komponen kecil jika kita ingin mengkustomisasinya

## Perbedaan `autentikasi` dan `otorisasi` dalam konteks Django
Autentikasi adalah proses memverifikasi _user_, seperti siapa yang sedang _login_. Otorisasi adalah proses menentukan _user_ yang telah di autentikasi dapat melakukan apa saja pada program. Kedua hal ini penting karena tentunya kita perlu sebuah langkah untuk menentukan siapa yang bisa masuk program kita (dengan autentikasi), dan apa saja yang bisa ia lakukan pada program kita (otorisasi). Bayangkan bila kita membiarkan siapa saja yang masuk pada program kita dapat melakukan apa saja karena tidak melewati otorisasi. Program yang kita buat dapat menjadi kacau karena diotak-atik orang luar.

## Cookies
`Cookies` adalah _text file_ berukuran kecil yang disimpan pada sisi _client_. `Cookies` secara singkat bisa dibilang berguna untuk mengubah HTTP yang _stateless protocol_ menjadi _stateful protocol_ (_user_ yang pernah _login_ datanya akan tersimpan dalam bentuk `cookies`).
<br>
Kita dapat menggunakan `Cookies` di Django dengan meng-_import_ HttpResponse, lalu menggunakan method `.set_cookie`, lalu kita bisa mengakses cookie tersebut dengan method `request.COOKIES`

## Apakah Cookies itu aman?
Cookies membuat _user_ lebih nyaman dalam menggunakan aplikasi karena _user_ tidak perlu melakukan _login_ setiap kali masuk aplikasi. Namun, biasanya kenyamanan berbanding terbalik dengan keamanan. Cookies secara transparan dapat dilihat oleh _user_ pada browsernya. Karena ketransparannya ini, Cookies dapat mudah di-_copy_. Terdapat berbagai jenis serangan yang berhubungan dengan Cookies, misalnya `Cookies poisoning`

## Pengimplementasian _step-by-step_
**1. Pembuatan _register_, _login_, dan _logout_**
Pertama, buat fungsi-fungsi  _register_, _login_, dan _logout_ tersebut pada `views.py`

Register :
```
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)
```
<br>

Login :
```
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)
```
<br>

Logout :
```
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
```

Pada kode di atas, fungsi `Login` dan `Logout` sudah kita terapkan penggunaan `Cookies` karena terdapat method `.set_cookie` untuk menerapkan Cookies dan method  `.delete_cookie` untuk menghapus Cookies ketika Logout

**2. Pembuatan halaman `Register` dan `Login`**
Setelah membuat fungsi pada `views.py`, kita membuat halaman `Register` dan `Login` agar fungsi tersebut ketika diletakan pada `urls.py` dapat membawa kita ke halaman yang dimaksud

register.html:

```
{% extends 'base.html' %}

{% block meta %}
    <title>Register</title>
{% endblock meta %}

{% block content %}  

<div class = "login">
    
    <h1>Register</h1>  

        <form method="POST" >  
            {% csrf_token %}  
            <table>  
                {{ form.as_table }}  
                <tr>  
                    <td></td>
                    <td><input type="submit" name="submit" value="Daftar"/></td>  
                </tr>  
            </table>  
        </form>

    {% if messages %}  
        <ul>   
            {% for message in messages %}  
                <li>{{ message }}</li>  
                {% endfor %}  
        </ul>   
    {% endif %}

</div>  

{% endblock content %}
```
<br>

login.html:
```
{% extends 'base.html' %}

{% block meta %}
    <title>Login</title>
{% endblock meta %}

{% block content %}

<div class = "login">

    <h1>Login</h1>

    <form method="POST" action="">
        {% csrf_token %}
        <table>
            <tr>
                <td>Username: </td>
                <td><input type="text" name="username" placeholder="Username" class="form-control"></td>
            </tr>
                    
            <tr>
                <td>Password: </td>
                <td><input type="password" name="password" placeholder="Password" class="form-control"></td>
            </tr>

            <tr>
                <td></td>
                <td><input class="btn login_btn" type="submit" value="Login"></td>
            </tr>
        </table>
    </form>

    {% if messages %}
        <ul>
            {% for message in messages %}
                <li>{{ message }}</li>
            {% endfor %}
        </ul>
    {% endif %}     
        
    Don't have an account yet? <a href="{% url 'main:register' %}">Register Now</a>

</div>

{% endblock content %}
```
**3. Membuat 2 akun pengguna**
<br>
![ezgif com-video-to-gif](https://github.com/reyhanwiyasa/rey_inventory/assets/119433464/9a8857d7-55df-48a3-a97b-f86c67871aff)

<br>

**4. Menghubungkan model `Item` dengan `User`**
Menghubungkan model ke user pada Django dapat dilakukan dengan mengimport kode berikut
```
from django.contrib.auth.models import User
```
Lalu, pada model yang telah dibuat, ditambahkan potongan kode berikut

```
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```

Penghubungan Item dengan User merupakan sebuah _Relationship_. Jenis Relationship ada empat, yaitu one-to-one, one-to-many, many-to-one, dan many-to-many. Pada kasus ini, kita menggunakan Relationship one-to-one, dimana kita menghubungkan satu user kepada satu item.
<hr>

# TUGAS 3
## Perbedaan antara form **POST** dan form **GET** dalam Django
**POST** dan **GET** adalah method HTTP yang digunakan ketika kita berurusan dengan *forms*.

Pengiriman data yang melalui **POST** akan di encode terlebih dahulu untuk *transmission*, lalu dikirim ke *server*, baru kita menerima *response* dari *server*. Hal ini membuat pengiriman data melalui **POST** tidak mudah terlihat dan tidak akan muncul pada *url*. Karena sifatnya yang tersembunyi, **POST** cocok digunakan untuk mengisi password form, upload file, dan sebagainya.

Berbeda dengan **POST**, **GET** adalah method HTTP yang fokus pada simplisitas. Data yang dikirim akan disimpan pada *url* yang dituju. Hal ini membuat **GET** cocok untuk digunakan pada *web search form*, karena *URL* nya dapat mudah di *bookmark*, *shared*, dan *resubmitted*.
## Apa perbedaan utama antara XML, JSON, dan HTML dalam konteks pengiriman data?
Perbedaan utama antara **XML**, **JSON**, dan **HTML** terletak pada *format* dan *syntax* yang mereka gunakan.

* **HTML** jauh lebih *human-readable* dibandingkan JSON dan HTML, namun susah dipahami oleh *machine* karena sebuah halaman **HTML** berisi bukan hanya data, namun terdapat *design*, konten, script, dan lain-lain.


* **XML** adalah format yang *machine* dan *human-readable*. Struktur yang dimiliki **XML** mirip dengan struktur pada **HTML**, di mana terdapat *tree* yang memiliki satu *root*, dan terdapat *tags* yang ditandai dengan tanda <>, mirip seperti **HTML**

* **JSON** adalah format yang *machine* dan *human-readable*. **JSON** menggunakan *key-value pairs*, di mana *Key* nya berupa *String*. Format yang digunakan **JSON** ini mirip seperti yang digunakan oleh *Dictionary* dan *Map*.

##  Mengapa JSON sering digunakan dalam pertukaran data antara aplikasi web modern?
*JSON** dikembangkan setelah adanya **XML**, membuat **JSON** lebih modern dibanding **XML**. **JSON** sering digunakan dalam pertukaran data antara aplikasi web modern karena sifatnya yang *machine* dan *human-readable*. Penggunaan struktur data berupa *Dictiornary* dan *List* yang digunakan **JSON** juga lebih membuatnya lebih *compact* dan lebi hmudah untuk dibaca dibandingkan **XML**.
## Pengimplementasian _checklist_ di atas secara _step-by-step_
**1. Membuat kerangka *Views* <br>**
Kerangka ini berguna agar kode kita konsisten dan memperkecil terjadinya redundansi kode

**2. Membuat Forms `forms.py`**
buat file *forms.py* pada direktori app yang berguna untuk membuat form. Seluruh HTML sudah di-handle oleh library `django.forms`. Contoh isi `forms.py` :
```
from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "amount", "description"]
```
**3. Merender Forms**<br>
Buat file pada directory `templates` bernama `create_product` dengan kode berikut:
```
{% extends 'base.html' %} 

{% block content %}
<h1>Add New Product</h1>

<form method="POST">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
        <tr>
            <td></td>
            <td>
                <input type="submit" value="Add Product"/>
            </td>
        </tr>
    </table>
</form>

{% endblock %}
```
baris `form.as_table` akan merender form secara keseluruhan

**4. Menambahkan fungsi-fungsi `views` serializer JSON dan XML**<br>
Serializer digunakan untuk mengirim data dalam bentuk JSON dan XML. Serializer diimplementasikan dalam `views.py` di mana ia akan mengreturn `HTTPResponse`
```
from django.core import serializers

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```
**5 Membuat routing URL untuk masing-masing views**<br>
Kita taruh fungsi-fungsi yang telah dibuat di `views.py` tadi ke `urls.py` yang terdapat pada direktori aplikasi agar kita dapat melakukan *routing* ke URLs yang dituju.
```
from django.urls import path
from main.views import show_main, create_product, show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'main'

urlpatterns = [
   . . .,
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),  
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'), 
]
```
<br>
<hr>

## Mengakses data menggunakan *postman*
1. Data HTML![data html](https://github.com/reyhanwiyasa/rey_inventory/assets/119433464/d5ded678-df1b-42e7-bd87-baf71b04cef6)
2. Data XML![data xml](https://github.com/reyhanwiyasa/rey_inventory/assets/119433464/aaaa2249-0738-4a27-b605-ed0d00e68854)
3. Data XML by ID![data xml by id](https://github.com/reyhanwiyasa/rey_inventory/assets/119433464/199fba33-49e4-4d44-b107-b619a338504b)
4. Data JSON![data json](https://github.com/reyhanwiyasa/rey_inventory/assets/119433464/f9d51776-bd2a-47b7-80d1-3f189a7eb54b)
5. Data JSON by ID![data json by id](https://github.com/reyhanwiyasa/rey_inventory/assets/119433464/e8d7cbb9-220f-44cf-a1ca-67cf175f8dcd)





# TUGAS 2
## **Pengimplementasian checklist secara step-by-step**
### 1. Membuat proyek Django baru
1. Masuk ke dalam repo utama, lalu jalankan _command prompt_ dan buat virtual environment dengan menjalankan 	`python -m venv env`  (***penjelasan kegunaan virtual environment ada di bagian bawah***)
2. Aktifkan virtual environment dengan menjalankan `env\Scripts\activate.bat`
3. Buat berkas `requirements.txt` yang berisi beberapa dependencies yaitu <br/>
```
django
gunicorn
whitenoise
psycopg2-binary
requests
urllib3
```

lalu, jalankan perintah `pip install -r requirements.txt` untuk menginstall requirements
4. Buat proyek django dengan nama **rey_inventory** dengan menjalankan perintah `django-admin startproject rey_inventory .`

### 2. Membuat aplikasi dengan nama **main** di proyek tersebut
1. Jalankan perintah `python manage.py startapp main` untuk membuat aplikasi `main`
2. Mendaftarkan aplikasi **main** ke dalam proyek dengan membuka berkas `settings.py`, lalu masukkan **main** ke dalam variable **INSTALLED_APPS**

### 3. Melakukan _routing_ pada proyek agar dapat menjalankan **main**
1. Buka berkas `urls.py` pada **direktori proyek rey_inventory** lalu import fungsi `include` dari `django.urls`
   `from django.urls import path, include`
2. Tambahkan rute url di dalam variabel **urlpatterns**
Berkas ini berguna untuk mengatur URL yang terkait pada aplikasi `main`

### 4. Membuat model pada aplikasi `main` dengan nama `Item` dengan beberapa atribut wajib
1. Isi berkas `models.py` pada direktori aplikasi `main` lalu isi dengan kode berikut
   ```
   class Product(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)
    amount = models.IntegerField()
    description = models.TextField()
   ```
2. Membuat migrasi model untuk melacak perubahan yang terjadi pada _database_ dengan menjalankan perintah
   `python manage.py makemigrations`
3. Menerapkan migrasi ke _datatbase_ lokal dengan menjalankan perintah
   `python manage.py migrate`

### 5. Membuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML
1. Membuat direktori baru bernama `templates` di dalam direktori aplikasi `main`, lalu membuat berkas bernama `main.html` pada direktori `templates` tersebut
2. Buka  berkas `views.py` pada direktori aplikasi `main`, lalu buat fungsi berikut
   ```
   from django.shortcuts import render

    def show_main(request):
        context = {
            'name': 'Reyhan Wiyasa P',
            'class': 'PBP A',
            'amount' : 100,
            'description' : 'Peppermint\'s storage'
    }

    return render(request, "main.html", context)
   ```

### 6. Membuat sebuah routing pada `urls.py` aplikasi main untuk memetakan fungsi yang telah dibuat pada `views.py`
1. Buka berkas `urls.py` yang terdapat di dalam direktori aplikasi `main`, lalu tambahkan kode berikut
   ```
    from django.urls import path
    from main.views import show_main
    
    app_name = 'main'
    
    urlpatterns = [
        path('', show_main, name='show_main'),
    ]
   ```
   Kode di atas akan menampilkan laman `main.html` pada `http://localhost:8000/main/`

### 7.  Melakukan deployment ke Adaptable terhadap aplikasi yang sudah dibuat
1. Login ke Adaptable menggunakan akun github, lalu pilih `New App` dan `Connect to an existing repository`
2. Pilih repo `rey_inventory` sebagai basis aplikasi yang ingin di deploy
3. Pilih Python App Template sebagai template deployment
4. Pilih PostgreSQL sebagai tipe basis data yang akan digunakan
5. Pada bagian Start Command masukkan perintah `python manage.py migrate && gunicorn rey_inventory.wsgi`

##  **Bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya**
![MVT django](https://github.com/reyhanwiyasa/rey_inventory/assets/119433464/1721da89-91c9-4e6c-adbc-fa75bc6b55e2)
> Source : How Django Works (MVT Pattern) - Code Stack
1. User mengirim request, di mana request tersebut akan dihandle oleh controller (views.py)
2. Views.py akan mengirim QuerySets kepada Models untuk diproses
3. Database akan melakukan Read dari Models, lalu melakukan Write untuk mengupdate Models.
4. Models.py akan mengirim ResultSet ke Views.py
5. Views.py akan menampilkan response ke Templates untuk ditampilkan kepada user


## **Mengapa menggunakan Virtual Environment?**
Virtual environment memungkinkan kita untuk mengisolasi package serta dependencies dari aplikasi sehingga tidak bertabrakan dengan versi lain yang ada di komputer. Hal ini memungkinkan kita untuk bekerja pada proyek yang berbeda yang menggunakan versi yang berbeda tanpa konflik sehingga memudahkan kita untuk mengelola proyek-proyek tersebut. Virtual environment juga membuat proyek kita lebih _resource efficient_ karena kita hanya menggunakan package dan library yang diperlukan, bukan menggunakan semua library yang ada.

### Apakah tetap dapat membuat tanpa Virtual Environment?
Ya, tetap bisa. Namun kelebihan-kelebihan di atas tidak akan didapatkan.

## **MVC, MVT, MVVM**
MCT, MVT, dan MVVM adalah pola design yang digunakan pada software development untuk memisahkan hal-hal yang diperlukan dalam pembuatan aplikasi sehingga proses pembuatan dapat lebih mudah diatur dan dikelola. Perbedaan dari MVC, MVT, dan MVVM adalah berikut
1. MVC
   Model  : Berisi tentang data dan logika aplikasi. Berfungsi sebagai tempat penyimpanan, penerimaan, dan pengelolaan data
   View   : Berfungsi sebagai tempat penyajian data kepada user
   Control : Berfungsi sebagai perantara antara Model dan View. Control menerima input user dari View, lalu diproses, kemudian dikirim ke Model untuk di-update, lalu dikirim ke View lagi untuk di-update

2. MVT
   Model dan View pada MVC mirip dengan MVC, yang membedakan hanya Template
   Template   : Mendefinisikan struktur dari View dan bagaimana data pada Model disajikan kepada user

3. MVVM
   Model dan View pada MVVM mirip dengan MVC dan MVT, yang membedakan adalah MVVM memiliki ViewModel
   ViewModel   : Berfungsi sebagai perantara antara Model dan View. ViewModel mengeluarkan data dari Model dalam bentuk yang dapat dengan mudah di _bind_ dan di-_display_ oleh View.
