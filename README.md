# rey_inventory

## Pengimplementasian checklist secara step-by-step
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
1. Jalankan perintah `python manage.py startapp main`
2. Mendaftarkan aplikasi **main** ke dalam proyek dengan membuka berkas `settings.py`, lalu masukkan **main** ke dalam variable **INSTALLED_APPS**

### 3. Melakukan _routing_ pada proyek agar dapat menjalankan **main**
1. Buka berkas `urls.py` pada **direktori proyek rey_inventory** lalu import fungsi `include` dari `django.urls`
   `from django.urls import path, include`
2. Tambahkan rute url di dalam variabel **urlpatterns**

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

##  Bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya
