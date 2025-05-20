import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
import numpy as np
import matplotlib.pyplot as plt


class ReglaSimpsonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Regla de Simpson 1/3 y 3/8 - Integración Numérica")
        self.setGeometry(200, 200, 700, 550)

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
        self.input_n = QLineEdit("6")
        layout.addWidget(self.input_n)

        self.btn_calcular = QPushButton("Aplicar Regla de Simpson")
        self.btn_calcular.clicked.connect(self.calcular_simpson)
        layout.addWidget(self.btn_calcular)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def calcular_simpson(self):
        try:
            funcion_str = self.input_funcion.text()
            a = float(self.input_a.text())
            b = float(self.input_b.text())
            n = int(self.input_n.text())

            if n <= 0 or a >= b:
                raise ValueError("Verifica los valores de a, b y n.")

            if n % 2 != 0 and n % 3 != 0:
                raise ValueError("Para aplicar Simpson, n debe ser par (1/3) o múltiplo de 3 (3/8).")

            f = lambda x: eval(funcion_str, {"x": x, "np": np})
            x = np.linspace(a, b, n + 1)
            y = f(x)
            h = (b - a) / n

            integral = 0
            metodo = ""
            if n % 2 == 0:
                # Simpson 1/3
                integral = y[0] + y[-1] + 4 * sum(y[1:-1:2]) + 2 * sum(y[2:-2:2])
                integral *= h / 3
                metodo = "Simpson 1/3"
            if n % 3 == 0:
                # Simpson 3/8 (más preciso si n % 3 == 0)
                integral = y[0] + y[-1] + 3 * sum(y[1:-1][::3] + y[1:-1][1::3]) + 2 * sum(y[3:-3:3])
                integral *= 3 * h / 8
                metodo = "Simpson 3/8"

            salida = f"📐 Integral aproximada usando la Regla de {metodo}:\n\n"
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
            plt.title(f'Aproximación por la Regla de {metodo}')
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
    ventana = ReglaSimpsonApp()
    ventana.show()
    sys.exit(app.exec_())