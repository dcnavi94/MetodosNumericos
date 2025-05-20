import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
import numpy as np
import matplotlib.pyplot as plt


class RungeKuttaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Runge-Kutta de 2do y 4to Orden")
        self.setGeometry(200, 200, 700, 600)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("📌 Ingrese la derivada dy/dx = f(x, y) (ej: x + y):"))
        self.input_funcion = QLineEdit("x + y")
        layout.addWidget(self.input_funcion)

        layout.addWidget(QLabel("🔢 Valor inicial x0:"))
        self.input_x0 = QLineEdit("0")
        layout.addWidget(self.input_x0)

        layout.addWidget(QLabel("🔢 Valor inicial y0:"))
        self.input_y0 = QLineEdit("1")
        layout.addWidget(self.input_y0)

        layout.addWidget(QLabel("🔢 Valor final de x:"))
        self.input_xf = QLineEdit("2")
        layout.addWidget(self.input_xf)

        layout.addWidget(QLabel("📈 Número de pasos n:"))
        self.input_n = QLineEdit("10")
        layout.addWidget(self.input_n)

        self.btn_calcular = QPushButton("Aplicar Runge-Kutta 2do y 4to Orden")
        self.btn_calcular.clicked.connect(self.calcular_runge_kutta)
        layout.addWidget(self.btn_calcular)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def calcular_runge_kutta(self):
        try:
            funcion_str = self.input_funcion.text()
            x0 = float(self.input_x0.text())
            y0 = float(self.input_y0.text())
            xf = float(self.input_xf.text())
            n = int(self.input_n.text())

            if n <= 0 or x0 >= xf:
                raise ValueError("Verifica los valores de x0, xf y n.")

            f = lambda x, y: eval(funcion_str, {"x": x, "y": y, "np": np})
            h = (xf - x0) / n

            # RK2
            x2, y2 = [x0], [y0]
            x, y = x0, y0
            for _ in range(n):
                k1 = f(x, y)
                k2 = f(x + h, y + h * k1)
                y += h * (k1 + k2) / 2
                x += h
                x2.append(x)
                y2.append(y)

            # RK4
            x4, y4 = [x0], [y0]
            x, y = x0, y0
            for _ in range(n):
                k1 = f(x, y)
                k2 = f(x + h/2, y + h * k1 / 2)
                k3 = f(x + h/2, y + h * k2 / 2)
                k4 = f(x + h, y + h * k3)
                y += h * (k1 + 2*k2 + 2*k3 + k4) / 6
                x += h
                x4.append(x)
                y4.append(y)

            salida = "📈 Método de Runge-Kutta\n\n"
            salida += "x\tRK2\tRK4\n"
            for i in range(len(x2)):
                salida += f"{x2[i]:.4f}\t{y2[i]:.6f}\t{y4[i]:.6f}\n"

            self.resultado.setPlainText(salida)

            # Gráfica
            plt.figure(figsize=(8, 5))
            plt.plot(x2, y2, 'ro--', label='Runge-Kutta 2° orden')
            plt.plot(x4, y4, 'bo-', label='Runge-Kutta 4° orden')
            plt.title('Métodos de Runge-Kutta')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = RungeKuttaApp()
    ventana.show()
    sys.exit(app.exec_())
