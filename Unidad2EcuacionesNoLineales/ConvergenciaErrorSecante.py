import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sympy import Symbol, sympify, lambdify
import numpy as np


class SecanteConvergenciaApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Método de la Secante con Análisis de Convergencia")
        self.setGeometry(200, 200, 800, 750)

        layout = QVBoxLayout()

        # Entrada de la función
        layout.addWidget(QLabel("Función f(x):"))
        self.input_funcion = QLineEdit("x**3 - x - 2")
        layout.addWidget(self.input_funcion)

        # Valores iniciales
        layout.addWidget(QLabel("x₀ inicial:"))
        self.input_x0 = QLineEdit("1")
        layout.addWidget(self.input_x0)

        layout.addWidget(QLabel("x₁ inicial:"))
        self.input_x1 = QLineEdit("2")
        layout.addWidget(self.input_x1)

        # Tolerancia
        layout.addWidget(QLabel("Tolerancia:"))
        self.input_tol = QLineEdit("0.0001")
        layout.addWidget(self.input_tol)

        # Botón de ejecución
        self.btn_calcular = QPushButton("Calcular raíz y analizar convergencia")
        self.btn_calcular.clicked.connect(self.calcular_raiz)
        layout.addWidget(self.btn_calcular)

        # Tabla de iteraciones
        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        # Gráfica de errores
        self.figura = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figura)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def calcular_raiz(self):
        try:
            x = Symbol('x')
            f_expr = sympify(self.input_funcion.text())
            f = lambdify(x, f_expr, "numpy")

            x0 = float(self.input_x0.text())
            x1 = float(self.input_x1.text())
            tol = float(self.input_tol.text())

            max_iter = 100
            contador = 0
            iteraciones = []
            errores = []

            # Método de la secante
            while contador < max_iter:
                f_x0 = f(x0)
                f_x1 = f(x1)

                if f_x1 - f_x0 == 0:
                    raise ValueError("División entre cero en f(x₁) - f(x₀)")

                x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
                error = abs(x2 - x1)

                iteraciones.append((contador + 1, x0, x1, f_x0, f_x1, x2, error))
                errores.append(error)

                if error < tol:
                    break

                x0, x1 = x1, x2
                contador += 1

            # Tabla de resultados
            self.tabla.setRowCount(len(iteraciones))
            self.tabla.setColumnCount(7)
            self.tabla.setHorizontalHeaderLabels([
                "Iter", "x₀", "x₁", "f(x₀)", "f(x₁)", "x₂", "Error |x₂ - x₁|"
            ])

            for i, fila in enumerate(iteraciones):
                for j, valor in enumerate(fila):
                    self.tabla.setItem(i, j, QTableWidgetItem(f"{valor:.6f}"))

            # Gráfica de convergencia del error
            self.figura.clear()
            ax = self.figura.add_subplot(111)
            ax.plot(range(1, len(errores)+1), errores, marker='o', color='purple')
            ax.set_title("Análisis de Convergencia del Método de la Secante")
            ax.set_xlabel("Iteración")
            ax.set_ylabel("Error |x₂ - x₁|")
            ax.grid(True)
            ax.set_yscale("log")  # Escala logarítmica para mejor visualización

            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# Ejecución de la app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SecanteConvergenciaApp()
    ventana.show()
    sys.exit(app.exec_())
