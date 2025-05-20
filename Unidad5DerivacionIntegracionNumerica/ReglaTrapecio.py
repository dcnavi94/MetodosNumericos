import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
import numpy as np
import matplotlib.pyplot as plt


class ReglaTrapecioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Regla del Trapecio - Integración Numérica")
        self.setGeometry(200, 200, 650, 500)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("📌 Ingrese la función f(x) (ej: x**2 + 3*x):"))
        self.input_funcion = QLineEdit("x**2")
        layout.addWidget(self.input_funcion)

        layout.addWidget(QLabel("🔢 Límite inferior a:"))
        self.input_a = QLineEdit("0")
        layout.addWidget(self.input_a)

        layout.addWidget(QLabel("🔢 Límite superior b:"))
        self.input_b = QLineEdit("1")
        layout.addWidget(self.input_b)

        layout.addWidget(QLabel("📈 Número de subintervalos n:"))
        self.input_n = QLineEdit("4")
        layout.addWidget(self.input_n)

        self.btn_calcular = QPushButton("Aplicar Regla del Trapecio")
        self.btn_calcular.clicked.connect(self.calcular_trapecio)
        layout.addWidget(self.btn_calcular)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def calcular_trapecio(self):
        try:
            funcion_str = self.input_funcion.text()
            a = float(self.input_a.text())
            b = float(self.input_b.text())
            n = int(self.input_n.text())

            if n <= 0 or a >= b:
                raise ValueError("Verifica los valores de a, b y n.")

            f = lambda x: eval(funcion_str, {"x": x, "np": np})
            x = np.linspace(a, b, n + 1)
            y = f(x)
            h = (b - a) / n

            integral = h * (y[0] / 2 + np.sum(y[1:-1]) + y[-1] / 2)

            salida = f"📐 Integral aproximada usando la Regla del Trapecio:\n\n"
            salida += f"Valor = {integral:.6f}\n\n"
            salida += "x\ty\n"
            for xi, yi in zip(x, y):
                salida += f"{xi:.4f}\t{yi:.6f}\n"

            self.resultado.setPlainText(salida)

            # Gráfica
            plt.figure(figsize=(8, 5))
            plt.plot(x, y, 'ro-', label='Puntos evaluados')
            for i in range(n):
                plt.fill_between(x[i:i+2], y[i:i+2], alpha=0.3)
            plt.title('Aproximación por la Regla del Trapecio')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = ReglaTrapecioApp()
    ventana.show()
    sys.exit(app.exec_())