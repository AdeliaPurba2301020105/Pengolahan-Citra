# 📊 Histogram Specification — Pengolahan Citra Digital

## 👩‍💻 Disusun Oleh

* **Nama**: [NAMA LENGKAP]
* **NIM**: [NIM]

## 👨‍🏫 Dosen Pengampu

* [NAMA DOSEN]

## 🏫 Institusi

Program Studi Teknik Informatika
Fakultas Teknik
Universitas Maritim Raja Ali Haji
2025

---

# 📌 BAB I PENDAHULUAN

## 1.1 Latar Belakang

Citra digital merupakan representasi visual dari suatu objek yang diperoleh dari perangkat seperti kamera atau sensor. Dalam praktiknya, citra sering mengalami penurunan kualitas seperti terlalu gelap, terlalu terang, atau kontras rendah.

Salah satu metode peningkatan kualitas citra adalah **Histogram Specification (Histogram Matching)**, yaitu teknik yang memungkinkan distribusi histogram citra disesuaikan dengan distribusi tertentu.

---

## 1.2 Rumusan Masalah

* Apa itu Histogram Specification?
* Bagaimana algoritmanya?
* Bagaimana implementasinya dalam Python?
* Bagaimana hasil sebelum dan sesudah proses?

---

## 1.3 Tujuan

* Memahami konsep Histogram Specification
* Mengimplementasikan dalam Python
* Menganalisis hasil citra

---

# 📚 BAB II TINJAUAN PUSTAKA

## 2.1 Citra Digital

Citra digital terdiri dari piksel dengan nilai intensitas:

* Grayscale: 0 – 255
* RGB: (R, G, B)

---

## 2.2 Histogram Citra

Histogram menyatakan distribusi intensitas piksel:

[
h(r_k) = n_k
]

Keterangan:

* ( r_k ) = intensitas ke-k
* ( n_k ) = jumlah piksel

---

## 2.3 Histogram Equalization

Transformasi:

[
T(r_k) = (L-1) \sum_{j=0}^{k} \frac{h(r_j)}{MN}
]

Keterangan:

* ( L ) = jumlah level (256)
* ( M,N ) = ukuran citra

---

## 2.4 Histogram Specification

Mapping dilakukan dengan:

[
t = \arg\min_t \left| CDF_{target}(t) - CDF_{source}(s) \right|
]

---

## 2.5 Cumulative Distribution Function (CDF)

[
CDF(k) = \sum_{i=0}^{k} \frac{h(i)}{MN}
]

---

## 2.6 Distribusi Target

### 🔹 Uniform

[
p(x) = \frac{1}{256}
]

### 🔹 Gaussian

[
p(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}
]

### 🔹 Rayleigh

[
p(x) = \frac{x}{\sigma^2} e^{-\frac{x^2}{2\sigma^2}}
]

### 🔹 Exponential

[
p(x) = \lambda e^{-\lambda x}
]

---

# 🧠 BAB III PEMBAHASAN

## 3.1 Deskripsi Program

Program GUI Python dengan fitur:

* Upload gambar
* Pilih distribusi
* Slider parameter
* Tampilkan histogram
* Simpan hasil

---

## 3.2 Algoritma

1. Upload gambar
2. Konversi ke grayscale
3. Hitung histogram
4. Hitung CDF sumber
5. Generate CDF target
6. Mapping intensitas
7. Tampilkan hasil

---

## 3.3 Contoh Kode Inti

```python
mapping = np.zeros(256, dtype=np.uint8)
for s in range(256):
    diff = np.abs(target_cdf - cdf_src[s])
    mapping[s] = np.argmin(diff)
```

---

# 🖼️ HASIL PROGRAM

## 📷 Original

![Original](images/original.png)

## 📷 Hasil Histogram Specification

![Hasil](images/hasil.png)

## 📊 Histogram

![Histogram](images/histogram.png)

---

# 🧪 HASIL PENGUJIAN

| No | Distribusi  | Hasil                |
| -- | ----------- | -------------------- |
| 1  | Uniform     | Kontras merata       |
| 2  | Gaussian    | Natural              |
| 3  | Rayleigh    | Terang di area gelap |
| 4  | Exponential | Kontras tinggi       |

---

# 🧾 BAB IV PENUTUP

## 4.1 Kesimpulan

* Histogram Specification lebih fleksibel dari Equalization
* Mapping berbasis CDF
* Distribusi mempengaruhi hasil

## 4.2 Saran

* Tambah PSNR & MSE
* Support RGB per channel
* Tambah fitur zoom

---

# 📚 DAFTAR PUSTAKA

* Gonzalez & Woods (2018)
* Pratt (2007)
* Szeliski (2022)
* https://numpy.org
* https://pillow.readthedocs.io

---

# ⚙️ CARA MENJALANKAN PROGRAM

```bash
pip install numpy pillow matplotlib
python histogram_specification.py
```

---

# 📁 STRUKTUR PROJECT

```
PengolahanCitra/
│
├── histogram_specification.py
├── images/
│   ├── original.png
│   ├── hasil.png
│   └── histogram.png
```

---

# 🚀 AUTHOR

Adelia Purba
