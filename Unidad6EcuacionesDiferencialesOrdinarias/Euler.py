import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
import numpy as np
import matplotlib.pyplot as plt


class EulerMejoradoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Euler Mejorado (Heun)")
        self.setGeometry(200, 200, 700, 550)

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

        self.btn_calcular = QPushButton("Aplicar Método de Euler Mejorado")
        self.btn_calcular.clicked.connect(self.calcular_euler_mejorado)
        layout.addWidget(self.btn_calcular)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def calcular_euler_mejorado(self):
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
            x = [x0]
            y = [y0]

            salida = "🧮 Método de Euler Mejorado (Heun)\n\n"
            salida += "x\ty\n"
            salida += f"{x0:.4f}\t{y0:.6f}\n"

            for i in range(n):
                xi = x[-1]
                yi = y[-1]
                k1 = f(xi, yi)
                k2 = f(xi + h, yi + h * k1)
                yi_next = yi + (h / 2) * (k1 + k2)
                xi_next = xi + h

                x.append(xi_next)
                y.append(yi_next)
                salida += f"{xi_next:.4f}\t{yi_next:.6f}\n"

            self.resultado.setPlainText(salida)

            # Gráfica
            plt.figure(figsize=(8, 5))
            plt.plot(x, y, 'bo-', label='Aproximación de Heun')
            plt.title('Solución aproximada por Euler Mejorado')
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
    ventana = EulerMejoradoApp()
    ventana.show()
    sys.exit(app.exec_())
