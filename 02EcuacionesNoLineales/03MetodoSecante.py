import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sympy import Symbol, sympify, lambdify
import numpy as np


class SecanteApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Método de la Secante")
        self.setGeometry(200, 200, 800, 700)

        # Layout principal
        layout = QVBoxLayout()

        # Entrada de la función f(x)
        layout.addWidget(QLabel("Función f(x):"))
        self.input_funcion = QLineEdit("x**3 - x - 2")
        layout.addWidget(self.input_funcion)

        # Entradas de los valores iniciales x0 y x1
        layout.addWidget(QLabel("Valor inicial x₀:"))
        self.input_x0 = QLineEdit("1")
        layout.addWidget(self.input_x0)

        layout.addWidget(QLabel("Valor inicial x₁:"))
        self.input_x1 = QLineEdit("2")
        layout.addWidget(self.input_x1)

        # Entrada de la tolerancia
        layout.addWidget(QLabel("Tolerancia:"))
        self.input_tol = QLineEdit("0.0001")
        layout.addWidget(self.input_tol)

        # Botón para ejecutar el método
        self.btn_calcular = QPushButton("Calcular raíz")
        self.btn_calcular.clicked.connect(self.calcular_raiz)
        layout.addWidget(self.btn_calcular)

        # Tabla para mostrar resultados por iteración
        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        # Área de gráfica
        self.figura = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figura)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def calcular_raiz(self):
        try:
            # Convertir la función a simbólica y luego evaluable
            x = Symbol('x')
            f_expr = sympify(self.input_funcion.text())
            f = lambdify(x, f_expr, "numpy")

            # Leer entradas
            x0 = float(self.input_x0.text())
            x1 = float(self.input_x1.text())
            tol = float(self.input_tol.text())

            max_iter = 100
            contador = 0
            iteraciones = []

            # Método de la secante: iteración principal
            while contador < max_iter:
                f_x0 = f(x0)
                f_x1 = f(x1)

                if f_x1 - f_x0 == 0:
                    raise ValueError("División entre cero: f(x₁) - f(x₀) = 0")

                # Fórmula de la secante
                x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
                error = abs(x2 - x1)

                iteraciones.append((contador + 1, x0, x1, f_x0, f_x1, x2, error))

                if error < tol:
                    break

                x0, x1 = x1, x2
                contador += 1

            # Mostrar resultados en tabla
            self.tabla.setRowCount(len(iteraciones))
            self.tabla.setColumnCount(7)
            self.tabla.setHorizontalHeaderLabels(["Iter", "x₀", "x₁", "f(x₀)", "f(x₁)", "x₂", "Error"])

            for i, fila in enumerate(iteraciones):
                for j, valor in enumerate(fila):
                    self.tabla.setItem(i, j, QTableWidgetItem(f"{valor:.6f}"))

            # Graficar la función y los puntos
            self.figura.clear()
            ax = self.figura.add_subplot(111)

            # Rango para graficar f(x)
            x_vals = np.linspace(x0 - 3, x1 + 3, 400)
            y_vals = f(x_vals)
            ax.plot(x_vals, y_vals, label='f(x)', color='blue')
            ax.axhline(0, color='black', linewidth=0.5)

            # Puntos generados
            puntos_x = [fila[2] for fila in iteraciones]
            puntos_y = [f(px) for px in puntos_x]
            ax.scatter(puntos_x, puntos_y, color='red', label='Aproximaciones')

            ax.set_title("Método de la Secante")
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid(True)
            ax.legend()

            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# Lanzar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SecanteApp()
    ventana.show()
    sys.exit(app.exec_())
