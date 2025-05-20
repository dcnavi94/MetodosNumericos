import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
import numpy as np
import matplotlib.pyplot as plt


class SistemasEDOApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistemas de EDO - Runge-Kutta 4to Orden")
        self.setGeometry(200, 200, 750, 600)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("📌 Ingrese las derivadas (ej: y2, -y1):"))
        self.input_f1 = QLineEdit("y2")
        self.input_f2 = QLineEdit("-y1")
        layout.addWidget(QLabel("dy1/dx ="))
        layout.addWidget(self.input_f1)
        layout.addWidget(QLabel("dy2/dx ="))
        layout.addWidget(self.input_f2)

        layout.addWidget(QLabel("🔢 Valor inicial x0:"))
        self.input_x0 = QLineEdit("0")
        layout.addWidget(self.input_x0)

        layout.addWidget(QLabel("🔢 y1(0):"))
        self.input_y10 = QLineEdit("0")
        layout.addWidget(self.input_y10)

        layout.addWidget(QLabel("🔢 y2(0):"))
        self.input_y20 = QLineEdit("1")
        layout.addWidget(self.input_y20)

        layout.addWidget(QLabel("🔢 Valor final de x:"))
        self.input_xf = QLineEdit("10")
        layout.addWidget(self.input_xf)

        layout.addWidget(QLabel("📈 Número de pasos n:"))
        self.input_n = QLineEdit("100")
        layout.addWidget(self.input_n)

        self.btn_calcular = QPushButton("Resolver sistema con Runge-Kutta 4° orden")
        self.btn_calcular.clicked.connect(self.calcular_sistema)
        layout.addWidget(self.btn_calcular)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def calcular_sistema(self):
        try:
            f1_str = self.input_f1.text()
            f2_str = self.input_f2.text()
            x0 = float(self.input_x0.text())
            y10 = float(self.input_y10.text())
            y20 = float(self.input_y20.text())
            xf = float(self.input_xf.text())
            n = int(self.input_n.text())

            if n <= 0 or x0 >= xf:
                raise ValueError("Verifica los valores de x0, xf y n.")

            h = (xf - x0) / n
            x = [x0]
            y1 = [y10]
            y2 = [y20]

            f1 = lambda x, y1, y2: eval(f1_str, {"x": x, "y1": y1, "y2": y2, "np": np})
            f2 = lambda x, y1, y2: eval(f2_str, {"x": x, "y1": y1, "y2": y2, "np": np})

            for _ in range(n):
                xi, y1i, y2i = x[-1], y1[-1], y2[-1]

                k1_1 = h * f1(xi, y1i, y2i)
                k1_2 = h * f2(xi, y1i, y2i)

                k2_1 = h * f1(xi + h/2, y1i + k1_1/2, y2i + k1_2/2)
                k2_2 = h * f2(xi + h/2, y1i + k1_1/2, y2i + k1_2/2)

                k3_1 = h * f1(xi + h/2, y1i + k2_1/2, y2i + k2_2/2)
                k3_2 = h * f2(xi + h/2, y1i + k2_1/2, y2i + k2_2/2)

                k4_1 = h * f1(xi + h, y1i + k3_1, y2i + k3_2)
                k4_2 = h * f2(xi + h, y1i + k3_1, y2i + k3_2)

                y1.append(y1i + (k1_1 + 2*k2_1 + 2*k3_1 + k4_1) / 6)
                y2.append(y2i + (k1_2 + 2*k2_2 + 2*k3_2 + k4_2) / 6)
                x.append(xi + h)

            salida = "📈 Sistema de EDO - Runge-Kutta 4° Orden\n\n"
            salida += "x\ty1\ty2\n"
            for xi, y1i, y2i in zip(x, y1, y2):
                salida += f"{xi:.4f}\t{y1i:.6f}\t{y2i:.6f}\n"

            self.resultado.setPlainText(salida)

            plt.figure(figsize=(8, 5))
            plt.plot(x, y1, label='y1(x)', marker='o')
            plt.plot(x, y2, label='y2(x)', marker='s')
            plt.title('Solución del sistema de EDO')
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
    ventana = SistemasEDOApp()
    ventana.show()
    sys.exit(app.exec_())
