import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial


class RegresionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Regresión Lineal y Polinómica")
        self.setGeometry(200, 200, 650, 550)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("📌 Ingrese los puntos x separados por coma (ej: 1,2,3):"))
        self.input_x = QLineEdit()
        layout.addWidget(self.input_x)

        layout.addWidget(QLabel("📌 Ingrese los puntos y correspondientes (ej: 2,4,6):"))
        self.input_y = QLineEdit()
        layout.addWidget(self.input_y)

        layout.addWidget(QLabel("🎯 Grado del polinomio (1 para lineal):"))
        self.input_grado = QLineEdit("1")
        layout.addWidget(self.input_grado)

        self.btn_calcular = QPushButton("Calcular Regresión")
        self.btn_calcular.clicked.connect(self.calcular_regresion)
        layout.addWidget(self.btn_calcular)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def calcular_regresion(self):
        try:
            x = np.array([float(i.strip()) for i in self.input_x.text().split(',')])
            y = np.array([float(i.strip()) for i in self.input_y.text().split(',')])
            grado = int(self.input_grado.text())

            if len(x) != len(y):
                raise ValueError("Los vectores x e y deben tener la misma longitud.")

            coef = np.polyfit(x, y, grado)
            p = np.poly1d(coef)

            salida = "📋 Coeficientes de la regresión:\n"
            for i, c in enumerate(coef):
                salida += f"a{i} = {c:.6f}\n"

            y_pred = p(x)
            r2 = 1 - np.sum((y - y_pred) ** 2) / np.sum((y - np.mean(y)) ** 2)
            salida += f"\n📈 Coeficiente de determinación R² = {r2:.6f}\n"

            self.resultado.setPlainText(salida)

            # Gráfica
            x_graf = np.linspace(min(x), max(x), 200)
            y_graf = p(x_graf)

            plt.figure(figsize=(8, 5))
            plt.plot(x, y, 'ro', label='Datos')
            plt.plot(x_graf, y_graf, 'b-', label=f'Regresión (grado {grado})')
            plt.title('Regresión Lineal / Polinómica')
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
    ventana = RegresionApp()
    ventana.show()
    sys.exit(app.exec_())
