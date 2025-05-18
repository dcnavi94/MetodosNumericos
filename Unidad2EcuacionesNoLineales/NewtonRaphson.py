import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sympy import Symbol, sympify, lambdify, diff
import numpy as np

class NewtonRaphsonApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Método de Newton-Raphson")
        self.setGeometry(200, 200, 800, 700)

        # Layout vertical principal
        layout = QVBoxLayout()

        # Campo para la función
        layout.addWidget(QLabel("Función f(x):"))
        self.input_funcion = QLineEdit("x**3 - 2*x + 1")
        layout.addWidget(self.input_funcion)

        # Campo para el valor inicial x0
        layout.addWidget(QLabel("Valor inicial x₀:"))
        self.input_x0 = QLineEdit("0")
        layout.addWidget(self.input_x0)

        # Tolerancia deseada
        layout.addWidget(QLabel("Tolerancia (ej. 0.0001):"))
        self.input_tol = QLineEdit("0.0001")
        layout.addWidget(self.input_tol)

        # Botón de cálculo
        self.btn_calcular = QPushButton("Calcular raíz")
        self.btn_calcular.clicked.connect(self.calcular_raiz)
        layout.addWidget(self.btn_calcular)

        # Tabla de iteraciones
        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        # Gráfica
        self.figura = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figura)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def calcular_raiz(self):
        try:
            x = Symbol('x')
            f_expr = sympify(self.input_funcion.text())        # Convertimos la entrada a función simbólica
            f_prime_expr = diff(f_expr, x)                     # Derivamos automáticamente

            f = lambdify(x, f_expr, "numpy")                   # Función evaluable
            f_prime = lambdify(x, f_prime_expr, "numpy")       # Derivada evaluable

            x0 = float(self.input_x0.text())
            tol = float(self.input_tol.text())

            iteraciones = []
            max_iter = 100
            contador = 0

            while contador < max_iter:
                fx = f(x0)
                fpx = f_prime(x0)

                if fpx == 0:
                    raise ValueError("La derivada es cero. No se puede continuar.")

                x1 = x0 - fx / fpx
                error = abs(x1 - x0)

                iteraciones.append((contador+1, x0, fx, fpx, x1, error))

                if error < tol:
                    break

                x0 = x1
                contador += 1

            # Mostrar en tabla
            self.tabla.setRowCount(len(iteraciones))
            self.tabla.setColumnCount(6)
            self.tabla.setHorizontalHeaderLabels(["Iteración", "x", "f(x)", "f'(x)", "x nuevo", "Error"])

            for i, fila in enumerate(iteraciones):
                for j, valor in enumerate(fila):
                    self.tabla.setItem(i, j, QTableWidgetItem(f"{valor:.6f}"))

            # Graficar función y puntos
            self.figura.clear()
            ax = self.figura.add_subplot(111)

            x_vals = np.linspace(x0 - 5, x0 + 5, 400)
            y_vals = f(x_vals)
            ax.plot(x_vals, y_vals, label='f(x)', color='blue')
            ax.axhline(0, color='black', linewidth=0.5)

            puntos_x = [fila[1] for fila in iteraciones]
            puntos_y = [f(xi) for xi in puntos_x]
            ax.scatter(puntos_x, puntos_y, color='red', label='Aproximaciones')

            ax.set_title("Método de Newton-Raphson")
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid(True)
            ax.legend()
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# Ejecución
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = NewtonRaphsonApp()
    ventana.show()
    sys.exit(app.exec_())
