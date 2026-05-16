# 🏪 OpenShop RESTful API

**Author:** Rifki Firmansyah

Sebuah RESTful API sederhana yang dibangun menggunakan Django dan Django REST Framework, dirancang khusus untuk memenuhi kriteria kelulusan kelas **"Belajar Back-End Pemula dengan Python"** di Dicoding.

---

## 🚀 Fitur Utama

- **CRUD Produk**: Menyediakan endpoint lengkap untuk *Create, Read, Update,* dan *Delete* entitas produk.
- **Pencarian & Filtering**: Mendukung filter pencarian produk berdasarkan `name` (Nama Produk) dan `location` (Lokasi Toko) yang bersifat *case-insensitive*.
- **Soft Delete**: Menerapkan arsitektur *Soft Delete* di mana produk yang dihapus tidak benar-benar dihapus dari *database*, melainkan hanya diubah status `is_delete`-nya menjadi `True`.
- **HATEOAS**: Implementasi objek `_links` (URL mandiri) pada respons API agar sesuai dengan prinsip arsitektur REST.
- **Format JSON Presisi**: Struktur *response body* (termasuk membungkus data *list* ke dalam properti `"products"`) telah disesuaikan secara amat ketat agar lulus pada pengetesan Postman *Collection* dari Dicoding.

---

## 🛠️ Technology Stack

- **Framework:** Django 4.2+ & Django REST Framework (DRF)
- **Database:** SQLite
- **Bahasa:** Python 3.10+

---

## 🏃‍♂️ Cara Menjalankan Proyek (Lokal)

### 1. Instalasi Dependensi
Pastikan Python sudah terinstal, lalu instal *library* yang dibutuhkan:
```bash
pip install -r requirements.txt
```
*(Atau Anda bisa menggunakan `pipenv` / `virtualenv` sesuai kebiasaan Anda).*

### 2. Migrasi Database
Siapkan skema database awal:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Nyalakan Server Django
```bash
python manage.py runserver
```
Server akan langsung menyala dan API siap diakses melalui `http://127.0.0.1:8000/`.

---

## 📚 API Endpoints

Seluruh rute API berpusat pada entitas tunggal yaitu `/products/` tanpa memerlukan otentikasi (wajib terbuka untuk *reviewer*).

| Endpoint | HTTP Method | Keterangan |
|----------|--------|------------|
| `/products/` | `GET` | Mengambil seluruh daftar produk yang masih aktif (belum di-soft delete). Bisa ditambah query `?name=...` atau `?location=...`. |
| `/products/` | `POST` | Menambahkan produk baru dengan *payload* lengkap. |
| `/products/{id}/` | `GET` | Mengambil detail spesifik satu produk berdasarkan ID (UUID). |
| `/products/{id}/` | `PUT` | Memperbarui data produk. |
| `/products/{id}/` | `DELETE` | Menghapus produk secara *soft delete* (mengubah nilai field `is_delete` menjadi `True`). |

---

## ✅ Status Pengetesan Postman

Proyek ini telah dites secara ketat baik secara manual maupun otomatis menggunakan *Newman* (CLI Postman) dan **Lulus 100% (0 Failed)** pada pengujian skenario **[743] OpenShop API Test With Soft Delete**.

---

**Author**: Rifki Firmansyah  
**Kelas**: Belajar Back-End Pemula dengan Python (Dicoding)  
**Status**: Lolos Uji Postman ✅
