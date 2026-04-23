"""
==================================================
  HISTOGRAM SPECIFICATION - Pengolahan Citra Digital
  Nama File : histogram_specification.py
  Deskripsi : Program peningkatan mutu citra dengan
              metode Histogram Specification
  Library   : tkinter, PIL, numpy, matplotlib
==================================================
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

def hitung_histogram(gray_img):
    """Menghitung histogram dari citra grayscale (0-255)."""
    hist = np.zeros(256, dtype=np.float64)
    for pixel in gray_img.flatten():
        hist[pixel] += 1
    return hist


def hitung_cdf(hist):
    """Menghitung Cumulative Distribution Function (CDF)."""
    total = hist.sum()
    cdf = np.cumsum(hist) / total
    return cdf


def generate_target_cdf(mode, mean=128, std=60):
    """
    Membuat target CDF sesuai distribusi yang dipilih.
    Mode: 'uniform', 'gaussian', 'rayleigh', 'exponential'
    """
    x = np.arange(256)
    
    if mode == 'Uniform':
        pdf = np.ones(256) / 256
        
    elif mode == 'Gaussian':
        pdf = np.exp(-0.5 * ((x - mean) / std) ** 2)
        pdf /= pdf.sum()
        
    elif mode == 'Rayleigh':
        sigma = std / 255.0
        xn = x / 255.0
        pdf = (xn / sigma**2) * np.exp(-xn**2 / (2 * sigma**2))
        pdf = np.nan_to_num(pdf)
        if pdf.sum() > 0:
            pdf /= pdf.sum()
        else:
            pdf = np.ones(256) / 256
            
    elif mode == 'Exponential':
        lam = 255 / max(mean, 1)
        pdf = lam * np.exp(-lam * (x / 255.0))
        pdf /= pdf.sum()
        
    else:
        pdf = np.ones(256) / 256

    cdf = np.cumsum(pdf)
    cdf = np.clip(cdf, 0, 1)
    return cdf

def histogram_specification(src_img_gray, target_cdf):
    """
    Melakukan Histogram Specification:
    1. Hitung CDF sumber
    2. Hitung CDF target
    3. Mapping: cari nilai t yang memiliki CDF paling dekat dengan CDF sumber
    """
    hist_src = hitung_histogram(src_img_gray)
    cdf_src  = hitung_cdf(hist_src)

    mapping = np.zeros(256, dtype=np.uint8)
    for s in range(256):
        diff = np.abs(target_cdf - cdf_src[s])
        mapping[s] = np.argmin(diff)

    hasil = mapping[src_img_gray]
    return hasil, cdf_src, mapping


class AppHistogramSpec:
    def __init__(self, root):
        self.root = root
        self.root.title("Histogram Specification — Pengolahan Citra Digital")
        self.root.configure(bg="#0f0f1a")
        self.root.geometry("1200x750")
        self.root.resizable(True, True)

        self.original_img  = None   
        self.gray_img      = None   
        self.hasil_img     = None   
        self.tk_orig       = None
        self.tk_hasil      = None

        self._build_ui()

    # ── BANGUN UI ──────────────────────────────────────────────────
    def _build_ui(self):
        # ── Header
        header = tk.Frame(self.root, bg="#1a1a2e", pady=12)
        header.pack(fill="x")
        tk.Label(header, text="📊  Histogram Specification",
                 font=("Courier New", 18, "bold"),
                 bg="#1a1a2e", fg="#7c6fff").pack()
        tk.Label(header, text="Peningkatan Mutu Citra — Pengolahan Citra Digital",
                 font=("Courier New", 10),
                 bg="#1a1a2e", fg="#555577").pack()

        # ── Main frame
        main = tk.Frame(self.root, bg="#0f0f1a")
        main.pack(fill="both", expand=True, padx=16, pady=10)

        left = tk.Frame(main, bg="#13131e", bd=0, relief="flat", width=260)
        left.pack(side="left", fill="y", padx=(0,10))
        left.pack_propagate(False)
        self._build_controls(left)

        right = tk.Frame(main, bg="#0f0f1a")
        right.pack(side="left", fill="both", expand=True)
        self._build_display(right)

    def _build_controls(self, parent):
        pad = {"padx": 12, "pady": 6}

        tk.Label(parent, text="⚙  KONTROL", font=("Courier New", 11, "bold"),
                 bg="#13131e", fg="#7c6fff").pack(pady=(16,4))

        # Upload
        tk.Button(parent, text="📁  Upload Gambar",
                  command=self.upload_gambar,
                  bg="#7c6fff", fg="white",
                  font=("Courier New", 10, "bold"),
                  relief="flat", cursor="hand2",
                  pady=8).pack(fill="x", **pad)

        self.lbl_file = tk.Label(parent, text="Belum ada gambar",
                                  font=("Courier New", 8),
                                  bg="#13131e", fg="#555577",
                                  wraplength=230)
        self.lbl_file.pack(**pad)

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=12, pady=8)

        # Target Distribution
        tk.Label(parent, text="Target Distribution:",
                 font=("Courier New", 9, "bold"),
                 bg="#13131e", fg="#aaaacc").pack(anchor="w", padx=12)

        self.var_dist = tk.StringVar(value="Uniform")
        distributions = ["Uniform", "Gaussian", "Rayleigh", "Exponential"]
        for d in distributions:
            tk.Radiobutton(parent, text=d, variable=self.var_dist,
                           value=d, command=self._update_params,
                           bg="#13131e", fg="#ccccee",
                           selectcolor="#2a2a4a",
                           font=("Courier New", 9),
                           activebackground="#13131e").pack(anchor="w", padx=20)

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=12, pady=8)

        # Mean
        tk.Label(parent, text="Mean (μ):", font=("Courier New", 9, "bold"),
                 bg="#13131e", fg="#aaaacc").pack(anchor="w", padx=12)
        self.var_mean = tk.IntVar(value=128)
        self.lbl_mean = tk.Label(parent, textvariable=self.var_mean,
                                  font=("Courier New", 9), bg="#13131e", fg="#6fffd4")
        self.lbl_mean.pack(anchor="e", padx=12)
        self.slider_mean = tk.Scale(parent, from_=10, to=245,
                                     variable=self.var_mean,
                                     orient="horizontal",
                                     bg="#13131e", fg="#aaaacc",
                                     troughcolor="#2a2a4a",
                                     highlightthickness=0,
                                     relief="flat")
        self.slider_mean.pack(fill="x", padx=12)

        # Std
        tk.Label(parent, text="Std Dev (σ):", font=("Courier New", 9, "bold"),
                 bg="#13131e", fg="#aaaacc").pack(anchor="w", padx=12)
        self.var_std = tk.IntVar(value=60)
        self.lbl_std = tk.Label(parent, textvariable=self.var_std,
                                 font=("Courier New", 9), bg="#13131e", fg="#6fffd4")
        self.lbl_std.pack(anchor="e", padx=12)
        self.slider_std = tk.Scale(parent, from_=10, to=120,
                                    variable=self.var_std,
                                    orient="horizontal",
                                    bg="#13131e", fg="#aaaacc",
                                    troughcolor="#2a2a4a",
                                    highlightthickness=0,
                                    relief="flat")
        self.slider_std.pack(fill="x", padx=12)

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=12, pady=8)

        # Proses
        tk.Button(parent, text="⚡  PROSES",
                  command=self.proses,
                  bg="#ff6f91", fg="white",
                  font=("Courier New", 11, "bold"),
                  relief="flat", cursor="hand2",
                  pady=10).pack(fill="x", padx=12, pady=4)

        # Simpan
        tk.Button(parent, text="💾  Simpan Hasil",
                  command=self.simpan_hasil,
                  bg="#1e1e30", fg="#6fffd4",
                  font=("Courier New", 9),
                  relief="flat", cursor="hand2",
                  pady=6).pack(fill="x", padx=12, pady=2)

        # Histogram chart
        tk.Button(parent, text="📈  Lihat Histogram Detail",
                  command=self.lihat_histogram,
                  bg="#1e1e30", fg="#7c6fff",
                  font=("Courier New", 9),
                  relief="flat", cursor="hand2",
                  pady=6).pack(fill="x", padx=12, pady=2)

        self.lbl_status = tk.Label(parent, text="",
                                    font=("Courier New", 8),
                                    bg="#13131e", fg="#6fffd4",
                                    wraplength=230)
        self.lbl_status.pack(pady=6, padx=12)

    def _build_display(self, parent):
        # Frame gambar
        img_frame = tk.Frame(parent, bg="#0f0f1a")
        img_frame.pack(fill="both", expand=True)

        # Original
        f_orig = tk.Frame(img_frame, bg="#13131e", bd=1, relief="solid")
        f_orig.pack(side="left", fill="both", expand=True, padx=(0,6))
        tk.Label(f_orig, text="ORIGINAL", font=("Courier New", 9, "bold"),
                 bg="#13131e", fg="#6fffd4").pack(pady=4)
        self.canvas_orig = tk.Label(f_orig, bg="#0a0a14", text="Upload gambar dulu",
                                     fg="#333355", font=("Courier New", 10))
        self.canvas_orig.pack(fill="both", expand=True, padx=4, pady=(0,4))

        # Hasil
        f_hasil = tk.Frame(img_frame, bg="#13131e", bd=1, relief="solid")
        f_hasil.pack(side="left", fill="both", expand=True, padx=(6,0))
        tk.Label(f_hasil, text="HASIL HISTOGRAM SPECIFICATION",
                 font=("Courier New", 9, "bold"),
                 bg="#13131e", fg="#7c6fff").pack(pady=4)
        self.canvas_hasil = tk.Label(f_hasil, bg="#0a0a14", text="Belum diproses",
                                      fg="#333355", font=("Courier New", 10))
        self.canvas_hasil.pack(fill="both", expand=True, padx=4, pady=(0,4))

        # Mini histogram
        fig_frame = tk.Frame(parent, bg="#0f0f1a")
        fig_frame.pack(fill="x", pady=(8,0))

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(9, 1.8),
                                                        facecolor="#0f0f1a")
        for ax, title, color in [(self.ax1, "Histogram Original", "#6fffd4"),
                                  (self.ax2, "Histogram Hasil", "#7c6fff")]:
            ax.set_facecolor("#13131e")
            ax.set_title(title, color=color, fontsize=8, fontfamily="monospace")
            ax.tick_params(colors="#555577", labelsize=7)
            for spine in ax.spines.values():
                spine.set_edgecolor("#2a2a4a")

        self.fig.tight_layout(pad=1.0)
        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=fig_frame)
        self.fig_canvas.get_tk_widget().pack(fill="x")

    # ── AKSI ──────────────────────────────────────────────────────────

    def _update_params(self):
        dist = self.var_dist.get()
        state = "normal" if dist != "Uniform" else "disabled"
        self.slider_mean.config(state=state)
        self.slider_std.config(state=state)

    def upload_gambar(self):
        path = filedialog.askopenfilename(
            title="Pilih Gambar",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif"), ("All", "*.*")]
        )
        if not path:
            return
        img_raw = Image.open(path).convert("RGB")
        MAX_SIZE = 800
        if img_raw.width > MAX_SIZE or img_raw.height > MAX_SIZE:
            img_raw.thumbnail((MAX_SIZE, MAX_SIZE), Image.LANCZOS)
        self.original_img = img_raw
        self.gray_img = np.array(self.original_img.convert("L"))
        self.hasil_img = None

        # Tampilkan original
        self._tampilkan_di_label(self.original_img, self.canvas_orig)
        self.canvas_hasil.config(image="", text="Belum diproses", fg="#333355")
        self.canvas_hasil.image = None

        fname = os.path.basename(path)
        self.lbl_file.config(text=f"✅ {fname}\n{self.original_img.width}×{self.original_img.height}px (sudah diresize)")
        self.lbl_status.config(text="")

        # Update histogram original
        self._plot_histogram(self.ax1, self.gray_img, "#6fffd4")
        self.ax2.clear()
        self.ax2.set_facecolor("#13131e")
        self.ax2.set_title("Histogram Hasil", color="#7c6fff", fontsize=8, fontfamily="monospace")
        self.fig_canvas.draw()

    def proses(self):
        if self.original_img is None:
            messagebox.showwarning("Peringatan", "Upload gambar terlebih dahulu!")
            return

        dist  = self.var_dist.get()
        mean  = self.var_mean.get()
        std   = self.var_std.get()

        target_cdf = generate_target_cdf(dist, mean, std)
        hasil_gray, cdf_src, mapping = histogram_specification(self.gray_img, target_cdf)

        # Terapkan ke gambar berwarna (per-channel ratio)
        orig_arr = np.array(self.original_img, dtype=np.float64)
        gray_f   = self.gray_img.astype(np.float64)
        ratio    = np.where(gray_f > 0, hasil_gray.astype(np.float64) / gray_f, 1.0)
        ratio    = np.clip(ratio, 0, 4)

        hasil_rgb = np.clip(orig_arr * ratio[:, :, np.newaxis], 0, 255).astype(np.uint8)
        self.hasil_img = Image.fromarray(hasil_rgb)

        # Tampilkan hasil
        self._tampilkan_di_label(self.hasil_img, self.canvas_hasil)

        # Update histogram
        self._plot_histogram(self.ax1, self.gray_img, "#6fffd4")
        self._plot_histogram(self.ax2, hasil_gray, "#7c6fff")
        self.ax2.set_title(f"Histogram Hasil ({dist})", color="#7c6fff",
                            fontsize=8, fontfamily="monospace")
        self.fig_canvas.draw()

        self.lbl_status.config(text=f"✅ Selesai!\nDistribusi: {dist}")

    def simpan_hasil(self):
        if self.hasil_img is None:
            messagebox.showwarning("Peringatan", "Proses gambar dulu sebelum menyimpan!")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")],
            initialfile="histogram_spec_hasil.png"
        )
        if path:
            self.hasil_img.save(path)
            messagebox.showinfo("Berhasil", f"Gambar disimpan:\n{path}")

    def lihat_histogram(self):
        if self.gray_img is None:
            messagebox.showwarning("Peringatan", "Upload gambar dulu!")
            return
        fig, axes = plt.subplots(1, 2 if self.hasil_img else 1,
                                  figsize=(12 if self.hasil_img else 6, 4),
                                  facecolor="#0f0f1a")
        if not self.hasil_img:
            axes = [axes]
        fig.suptitle("Detail Histogram", color="white", fontsize=13, fontfamily="monospace")

        axes[0].bar(range(256), hitung_histogram(self.gray_img),
                    color="#6fffd4", width=1, alpha=0.85)
        axes[0].set_title("Original", color="#6fffd4", fontfamily="monospace")
        axes[0].set_facecolor("#13131e")
        axes[0].tick_params(colors="#aaaacc")

        if self.hasil_img and len(axes) > 1:
            hasil_gray = np.array(self.hasil_img.convert("L"))
            axes[1].bar(range(256), hitung_histogram(hasil_gray),
                        color="#7c6fff", width=1, alpha=0.85)
            axes[1].set_title("Hasil", color="#7c6fff", fontfamily="monospace")
            axes[1].set_facecolor("#13131e")
            axes[1].tick_params(colors="#aaaacc")

        plt.tight_layout()
        plt.show()

    # ── HELPER ──────────────────────────────────────────────────────

    def _tampilkan_di_label(self, pil_img, label_widget):
        label_widget.update_idletasks()
        w = max(label_widget.winfo_width(), 300)
        h = max(label_widget.winfo_height(), 280)
        img_copy = pil_img.copy()
        img_copy.thumbnail((w - 8, h - 8), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img_copy)
        label_widget.config(image=tk_img, text="")
        label_widget.image = tk_img

    def _plot_histogram(self, ax, gray_arr, color):
        ax.clear()
        ax.set_facecolor("#13131e")
        hist = hitung_histogram(gray_arr)
        ax.bar(range(256), hist, color=color, width=1, alpha=0.8)
        ax.tick_params(colors="#555577", labelsize=7)
        for spine in ax.spines.values():
            spine.set_edgecolor("#2a2a4a")
        self.fig.tight_layout(pad=1.0)


# ─────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = AppHistogramSpec(root)
    root.mainloop()