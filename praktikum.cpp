#include <iostream>
#include <cmath>
#include <iomanip>
#include <vector>
#include <limits>

using namespace std;

double f(double x) {
    return exp(-x * x);
}

double trapezoidal(double a, double b, int n) {
    double h = (b - a) / n;
    double sum = f(a) + f(b);
    for (int i = 1; i < n; ++i)
        sum += 2 * f(a + i * h);
    return (h / 2.0) * sum;
}

double romberg(double a, double b, int maxLevel) {
    vector<vector<double>> R(maxLevel + 1, vector<double>(maxLevel + 1, 0.0));

    for (int k = 0; k <= maxLevel; ++k) {
        int n = 1 << k;
        R[k][0] = trapezoidal(a, b, n);

        for (int j = 1; j <= k; ++j) {
            R[k][j] = (pow(4, j) * R[k][j - 1] - R[k - 1][j - 1]) / (pow(4, j) - 1);
        }
    }
    return R[maxLevel][maxLevel];
}

double relative_error(double approx, double exact) {
    if (exact == 0.0) return numeric_limits<double>::infinity();
    return fabs((approx - exact) / exact) * 100.0;
}

double input_double(const string& prompt) {
    double val;
    while (true) {
        cout << prompt;
        if (cin >> val) {
            return val;
        }
        else {
            cout << "Input tidak valid. Silakan masukkan angka.\n";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
    }
}

int main() {
    cout << "=====================================================\n";
    cout << "   PERBANDINGAN METODE TRAPEZOIDAL VS ROMBERG\n";
    cout << "=====================================================\n";
    cout << "Fungsi yang digunakan: f(x) = exp(-x^2)\n";
    cout << "Integral yang dihitung: integral f(x) dx\n";
    cout << "Catatan: Untuk metode Trapezoidal, akurasi meningkat jika jumlah interval besar.\n";
    cout << "-----------------------------------------------------\n";

    double a = input_double("Masukkan batas bawah (a): ");
    double b = input_double("Masukkan batas atas  (b): ");
    while (b <= a) {
        cout << "Batas atas harus lebih besar dari batas bawah. Silakan masukkan kembali.\n";
        b = input_double("Masukkan batas atas  (b): ");
    }

    const int exactMaxLevel = 12;
    cout << "\nMenghitung nilai acuan integrasi dengan akurasi tinggi, harap tunggu...\n";
    double exact = romberg(a, b, exactMaxLevel);

    const int maxLevel = 6;
    
    cout << fixed << setprecision(10);

    cout << "\n==============================================================\n";
    cout << " n\tTrapesium\tEr(%)   \tRomberg\t\tEr(%)\n";
    cout << "==============================================================\n";

    for (int i = 0; i <= maxLevel; ++i) {
        int n = 1 << i;
        double trap = trapezoidal(a, b, n);
        double romb = romberg(a, b, i);
        double err_trap = relative_error(trap, exact);
        double err_romb = relative_error(romb, exact);

        cout << setw(3) << n << "\t"<< setw(12) << trap << "\t"
            << setw(7) << err_trap << "\t"
            << setw(12) << romb << "\t"
            << setw(7) << err_romb << "\n";
    }

    cout << "==============================================================\n";
    cout << "Nilai acuan integrasi (dihitung dengan Romberg tingkat tinggi): " << exact << endl;
    cout << "Catatan: Trapezoidal memerlukan interval besar agar akurat; Romberg lebih cepat mencapai akurasi tinggi.\n";

    return 0;
}
