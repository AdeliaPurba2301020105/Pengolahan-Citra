# Histogram Specification — Pengolahan Citra Digital

## Disusun Oleh

* **Nama**:
* Adelia Kristianti Purba 2301020105
* Widuri Eka Febrianti

Program Studi Teknik Informatika
Fakultas Teknik
Universitas Maritim Raja Ali Haji
2025

---


## Latar Belakang

Citra digital merupakan representasi visual dari suatu objek yang diperoleh dari perangkat seperti kamera atau sensor. Dalam praktiknya, citra sering mengalami penurunan kualitas seperti terlalu gelap, terlalu terang, atau kontras rendah.

Salah satu metode peningkatan kualitas citra adalah **Histogram Specification (Histogram Matching)**, yaitu teknik yang memungkinkan distribusi histogram citra disesuaikan dengan distribusi tertentu.

---

## Rumusan Masalah

* Apa itu Histogram Specification?
* Bagaimana algoritmanya?
* Bagaimana implementasinya dalam Python?
* Bagaimana hasil sebelum dan sesudah proses?

---

## Tujuan

* Memahami konsep Histogram Specification
* Mengimplementasikan dalam Python
* Menganalisis hasil citra

---
## Deskripsi Program

Program GUI Python dengan fitur:

* Upload gambar
* Pilih distribusi
* Slider parameter
* Tampilkan histogram
* Simpan hasil

---

## Algoritma

1. Upload gambar
2. Konversi ke grayscale
3. Hitung histogram
4. Hitung CDF sumber
5. Generate CDF target
6. Mapping intensitas
7. Tampilkan hasil

# 🧪 HASIL PENGUJIAN

| No | Distribusi  | Hasil                |
| -- | ----------- | -------------------- |
| 1  | Uniform     | Kontras merata       |
| 2  | Gaussian    | Natural              |
| 3  | Rayleigh    | Terang di area gelap |
| 4  | Exponential | Kontras tinggi       |

---

#CARA MENJALANKAN PROGRAM

```bash
pip install numpy pillow matplotlib
python histogram_specification.py
```

