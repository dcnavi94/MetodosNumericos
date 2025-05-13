import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)

class FormulaGeneralApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fórmula General")
        self.setGeometry(100, 100, 300, 250)

        self.layout = QVBoxLayout()

        self.label = QLabel("Ingresa los coeficientes a, b y c de ax² + bx + c = 0:")
        self.layout.addWidget(self.label)

        self.a_input = QLineEdit()
        self.a_input.setPlaceholderText("a")
        self.layout.addWidget(self.a_input)

        self.b_input = QLineEdit()
        self.b_input.setPlaceholderText("b")
        self.layout.addWidget(self.b_input)

        self.c_input = QLineEdit()
        self.c_input.setPlaceholderText("c")
        self.layout.addWidget(self.c_input)

        self.calc_button = QPushButton("Calcular")
        self.calc_button.clicked.connect(self.solve_quadratic)
        self.layout.addWidget(self.calc_button)

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

    def solve_quadratic(self):
        try:
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            c = float(self.c_input.text())

            discriminante = b**2 - 4*a*c

            if discriminante < 0:
                self.result_label.setText("No hay soluciones reales.")
            else:
                x1 = (-b + math.sqrt(discriminante)) / (2*a)
                x2 = (-b - math.sqrt(discriminante)) / (2*a)
                self.result_label.setText(f"Soluciones: x₁ = {x1:.2f}, x₂ = {x2:.2f}")
                self.plot_quadratic(a, b, c, x1, x2)
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingresa valores numéricos válidos.")

    def plot_quadratic(self, a, b, c, x1, x2):
        x = np.linspace(x1 - 5, x2 + 5, 400)
        y = a * x**2 + b * x + c

        plt.figure(figsize=(6, 4))
        plt.plot(x, y, label=f'{a}x² + {b}x + {c}')
        plt.axhline(0, color='gray', linestyle='--')
        plt.axvline(x1, color='red', linestyle='--', label=f'x₁ = {x1:.2f}')
        plt.axvline(x2, color='blue', linestyle='--', label=f'x₂ = {x2:.2f}')
        plt.title("Gráfica de la parábola")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormulaGeneralApp()
    window.show()
    sys.exit(app.exec_())
