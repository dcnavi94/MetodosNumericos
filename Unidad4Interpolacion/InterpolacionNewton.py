import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
import numpy as np
import matplotlib.pyplot as plt


def diferencias_divididas(x, y):
    n = len(x)
    coef = np.copy(y).astype(float)
    for j in range(1, n):
        coef[j:n] = (coef[j:n] - coef[j - 1:n - 1]) / (x[j:n] - x[0:n - j])
    return coef


def polinomio_newton(coef, x_data, x):
    n = len(coef) - 1
    p = coef[n]
    for k in range(1, n + 1):
        p = coef[n - k] + (x - x_data[n - k]) * p
    return p


class InterpolacionNewtonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interpolación de Newton")
        self.setGeometry(200, 200, 600, 500)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("📌 Ingrese los puntos x separados por coma (ej: 1,2,3):"))
        self.input_x = QLineEdit()
        layout.addWidget(self.input_x)

        layout.addWidget(QLabel("📌 Ingrese los puntos y correspondientes (ej: 2,4,6):"))
        self.input_y = QLineEdit()
        layout.addWidget(self.input_y)

        layout.addWidget(QLabel("🔍 Punto a interpolar:"))
        self.input_eval = QLineEdit()
        layout.addWidget(self.input_eval)

        self.btn_calcular = QPushButton("Calcular Interpolación")
        self.btn_calcular.clicked.connect(self.interpolar)
        layout.addWidget(self.btn_calcular)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def interpolar(self):
        try:
            x = np.array([float(i.strip()) for i in self.input_x.text().split(',')])
            y = np.array([float(i.strip()) for i in self.input_y.text().split(',')])
            x_eval = float(self.input_eval.text())

            if len(x) != len(y):
                raise ValueError("Los vectores x e y deben tener la misma longitud.")

            coef = diferencias_divididas(x, y)
            y_interp = polinomio_newton(coef, x, x_eval)

            salida = "📋 Coeficientes de Newton:\n"
            for i, c in enumerate(coef):
                salida += f"a{i} = {c:.6f}\n"

            salida += f"\n🎯 Valor interpolado en x = {x_eval}: {y_interp:.6f}\n"
            self.resultado.setPlainText(salida)

            # Gráfica
            x_graf = np.linspace(min(x), max(x), 100)
            y_graf = [polinomio_newton(coef, x, xi) for xi in x_graf]
            plt.figure(figsize=(8, 5))
            plt.plot(x, y, 'ro', label='Datos')
            plt.plot(x_graf, y_graf, label='Polinomio de Newton')
            plt.axvline(x_eval, color='gray', linestyle='--', label=f'x = {x_eval}')
            plt.axhline(y_interp, color='blue', linestyle='--')
            plt.scatter([x_eval], [y_interp], color='green', label='Interpolación')
            plt.title('Interpolación de Newton')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = InterpolacionNewtonApp()
    ventana.show()
    sys.exit(app.exec_())