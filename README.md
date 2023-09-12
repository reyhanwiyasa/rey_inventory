# rey_inventory
[Application Link](https://rey-inventory.adaptable.app/)
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
