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

# TINJAUAN PUSTAKA

## Citra Digital

Citra digital terdiri dari piksel dengan nilai intensitas:

* Grayscale: 0 – 255
* RGB: (R, G, B)

---

## Histogram Citra

Histogram menyatakan distribusi intensitas piksel:

[
h(r_k) = n_k
]

Keterangan:

* ( r_k ) = intensitas ke-k
* ( n_k ) = jumlah piksel

---

## Histogram Equalization

Transformasi:

[
T(r_k) = (L-1) \sum_{j=0}^{k} \frac{h(r_j)}{MN}
]

Keterangan:

* ( L ) = jumlah level (256)
* ( M,N ) = ukuran citra

---

## Histogram Specification

Mapping dilakukan dengan:

[
t = \arg\min_t \left| CDF_{target}(t) - CDF_{source}(s) \right|
]

---

## Cumulative Distribution Function (CDF)

[
CDF(k) = \sum_{i=0}^{k} \frac{h(i)}{MN}
]

---

## Distribusi Target

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

---

## Contoh Kode Inti

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

#CARA MENJALANKAN PROGRAM

```bash
pip install numpy pillow matplotlib
python histogram_specification.py
```

