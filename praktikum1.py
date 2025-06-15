import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# Metode Regula Falsi
def regula_falsi(f, x1, x2, tol, max_iter):
    history = []
    for i in range(1, max_iter + 1):
        f1, f2 = f(x1), f(x2)
        if f1 == f2:
            raise ValueError("f(x1) dan f(x2) sama, metode tidak bisa dilanjutkan.")
        x3 = x2 - f2 * (x1 - x2) / (f1 - f2)
        f3 = f(x3)
        history.append((i, x1, x2, x3, f1, f2, f3))
        if abs(f3) < tol:
            break
        # Tentukan interval berikutnya
        if f1 * f3 < 0:
            x2 = x3
        else:
            x1 = x3
    return x3, history

# Mencari interval otomatis jika tidak diberikan
def find_interval(f, x0, step=0.1, limit=100):
    for i in range(1, limit + 1):
        a = x0 - i * step
        b = x0 + i * step
        if f(a) * f(b) < 0:
            return a, b
    return None, None

# === Input User ===
fx_str = input("Masukkan fungsi f(x) (misal: sin(x) - 5*x + 2): ").replace('^', '**')
x0 = float(input("Masukkan tebakan awal x0: "))

# Batas bawah (x1) hanya jika manual
x1_input = input("(Opsional) Masukkan batas bawah x1, atau Enter untuk auto: ")
manual = (x1_input.strip() != '')
if manual:
    x1 = float(x1_input)
    x2 = float(input("Masukkan batas atas x2: "))

decimals = int(input("Masukkan jumlah desimal presisi (misal: 4): "))
tol = 10 ** (-decimals)
max_iter = int(input("Masukkan iterasi maksimum: "))

# Parse fungsi
x = sp.Symbol('x')
try:
    expr = sp.sympify(fx_str)
    f = sp.lambdify(x, expr, 'numpy')
except Exception as e:
    print(f"Error pada fungsi: {e}")
    exit(1)

# Tentukan interval jika tidak manual
if not manual:
    x1, x2 = find_interval(f, x0)
    if x1 is None:
        print("❌ Gagal menemukan interval perubahan tanda di sekitar x0.")
        exit(1)
    print(f"✅ Interval otomatis: x1 = {x1:.{decimals}f}, x2 = {x2:.{decimals}f}")
else:
    print(f"📌 Interval manual: x1 = {x1:.{decimals}f}, x2 = {x2:.{decimals}f}")

# Jalankan Regula Falsi
root, hist = regula_falsi(f, x1, x2, tol, max_iter)

# Tampilkan hasil iterasi dengan f(x1), f(x2), f(x3)
print(f"\n{'It':<4}{'x1':>10}{'x2':>10}{'x3':>10}{'f(x1)':>12}{'f(x2)':>12}{'f(x3)':>12}")
for it, a, b, c, f1, f2, f3 in hist:
    print(f"{it:<4}{a:>10.{decimals}f}{b:>10.{decimals}f}{c:>10.{decimals}f}{f1:>12.{decimals}f}{f2:>12.{decimals}f}{f3:>12.{decimals}f}")

print(f"\n🎯 Akar ≈ {root:.{decimals}f} setelah {len(hist)} iterasi.")

# Plot fungsi dan titik iterasi
all_x3 = [h[3] for h in hist]
range_min = min(x1, x2, *all_x3) - 1
range_max = max(x1, x2, *all_x3) + 1
xs = np.linspace(range_min, range_max, 500)
ys = f(xs)

plt.figure(figsize=(8, 5))
plt.plot(xs, ys, label='f(x)')
plt.axhline(0, color='black', linewidth=1)
plt.scatter(all_x3, [f(val) for val in all_x3], marker='o', label='Iterasi x3')
plt.axvline(root, linestyle='--', label=f'Akar ≈ {root:.{decimals}f}')
plt.title(f'Metode Regula Falsi (Presisi: {decimals} desimal)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()
plt.show()