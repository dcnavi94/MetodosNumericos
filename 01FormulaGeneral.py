# Importamos las bibliotecas necesarias
import sys  # Para acceder a los argumentos del sistema
import math  # Para operaciones matemáticas como la raíz cuadrada
import numpy as np  # Para operaciones numéricas con vectores
import matplotlib.pyplot as plt  # Para graficar

# Importamos widgets de PyQt5 para crear la interfaz gráfica
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)

# Creamos la clase principal que hereda de QWidget (una ventana básica de PyQt)
class FormulaGeneralApp(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Fórmula General")
        self.setGeometry(100, 100, 300, 250)  # Posición y tamaño

        # Diseño vertical
        self.layout = QVBoxLayout()

        # Etiqueta de instrucciones
        self.label = QLabel("Ingresa los coeficientes a, b y c de ax² + bx + c = 0:")
        self.layout.addWidget(self.label)

        # Campo de entrada para 'a'
        self.a_input = QLineEdit()
        self.a_input.setPlaceholderText("a")
        self.layout.addWidget(self.a_input)

        # Campo de entrada para 'b'
        self.b_input = QLineEdit()
        self.b_input.setPlaceholderText("b")
        self.layout.addWidget(self.b_input)

        # Campo de entrada para 'c'
        self.c_input = QLineEdit()
        self.c_input.setPlaceholderText("c")
        self.layout.addWidget(self.c_input)

        # Botón para calcular las soluciones
        self.calc_button = QPushButton("Calcular")
        self.calc_button.clicked.connect(self.solve_quadratic)
        self.layout.addWidget(self.calc_button)

        # Etiqueta para mostrar el resultado
        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        # Aplicamos el diseño a la ventana
        self.setLayout(self.layout)

    # Método para resolver la ecuación cuadrática
    def solve_quadratic(self):
        try:
            # Obtenemos los valores de entrada como flotantes
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            c = float(self.c_input.text())

            # Calculamos el discriminante
            discriminante = b**2 - 4*a*c

            # Si el discriminante es negativo, no hay soluciones reales
            if discriminante < 0:
                self.result_label.setText("No hay soluciones reales.")
            else:
                # Calculamos las raíces reales usando la fórmula general
                x1 = (-b + math.sqrt(discriminante)) / (2*a)
                x2 = (-b - math.sqrt(discriminante)) / (2*a)

                # Mostramos el resultado en la interfaz
                self.result_label.setText(f"Soluciones: x₁ = {x1:.2f}, x₂ = {x2:.2f}")

                # Dibujamos la gráfica
                self.plot_quadratic(a, b, c, x1, x2)

        # Si ocurre un error al convertir los datos
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingresa valores numéricos válidos.")

    # Método para graficar la parábola
    def plot_quadratic(self, a, b, c, x1, x2):
        # Generamos valores de x alrededor de las soluciones
        x = np.linspace(x1 - 5, x2 + 5, 400)
        y = a * x**2 + b * x + c

        # Configuración del gráfico
        plt.figure(figsize=(6, 4))
        plt.plot(x, y, label=f'{a}x² + {b}x + {c}')
        plt.axhline(0, color='gray', linestyle='--')  # Eje X
        plt.axvline(x1, color='red', linestyle='--', label=f'x₁ = {x1:.2f}')  # Raíz 1
        plt.axvline(x2, color='blue', linestyle='--', label=f'x₂ = {x2:.2f}')  # Raíz 2
        plt.title("Gráfica de la parábola")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.grid(True)
        plt.show()

# Código que ejecuta la app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormulaGeneralApp()
    window.show()
    sys.exit(app.exec_())
