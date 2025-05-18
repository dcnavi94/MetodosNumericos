import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox, QGridLayout
)
import numpy as np


class JacobiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Jacobi - Sistema 3x3")
        self.setGeometry(200, 200, 750, 700)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("🔢 Ingrese el sistema (forma: ax + by + cz = d)"))

        # Campos organizados en forma de ecuación
        self.inputs_A = []
        self.inputs_b = []
        grid = QGridLayout()

        etiquetas = ["x", "y", "z", "=", "resultado"]
        for j, label in enumerate(etiquetas):
            grid.addWidget(QLabel(label), 0, j)

        for i in range(3):
            fila = []
            for j in range(3):
                campo = QLineEdit()
                campo.setFixedWidth(60)
                grid.addWidget(campo, i + 1, j)
                fila.append(campo)
            self.inputs_A.append(fila)

            grid.addWidget(QLabel("="), i + 1, 3)
            campo_res = QLineEdit()
            campo_res.setFixedWidth(60)
            grid.addWidget(campo_res, i + 1, 4)
            self.inputs_b.append(campo_res)

        layout.addLayout(grid)

        # Parámetros del método iterativo
        layout.addWidget(QLabel("🔁 Tolerancia (ej. 0.0001):"))
        self.input_tol = QLineEdit("0.0001")
        layout.addWidget(self.input_tol)

        layout.addWidget(QLabel("🔁 Máximo de iteraciones:"))
        self.input_max = QLineEdit("50")
        layout.addWidget(self.input_max)

        # Botón de ejecución
        self.btn_resolver = QPushButton("Resolver con método de Jacobi")
        self.btn_resolver.clicked.connect(self.jacobi)
        layout.addWidget(self.btn_resolver)

        # Área de resultados
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def jacobi(self):
        try:
            A = np.zeros((3, 3))
            b = np.zeros(3)

            for i in range(3):
                for j in range(3):
                    A[i, j] = float(self.inputs_A[i][j].text())
                b[i] = float(self.inputs_b[i].text())

            tol = float(self.input_tol.text())
            max_iter = int(self.input_max.text())

            x = np.zeros(3)  # solución inicial
            x_prev = np.copy(x)

            salida = "📘 Iteraciones del método de Jacobi:\n"
            salida += f"Iter\t x1\t x2\t x3\t Error\n"

            for iteracion in range(1, max_iter + 1):
                for i in range(3):
                    suma = sum(A[i, j] * x_prev[j] for j in range(3) if j != i)
                    x[i] = (b[i] - suma) / A[i, i]

                error = np.linalg.norm(x - x_prev, ord=np.inf)

                salida += f"{iteracion}\t {x[0]:.6f}\t {x[1]:.6f}\t {x[2]:.6f}\t {error:.6f}\n"

                if error < tol:
                    salida += "\n✅ Método convergió con la tolerancia indicada.\n"
                    break

                x_prev = np.copy(x)
            else:
                salida += "\n⚠️ No se alcanzó la convergencia en las iteraciones máximas.\n"

            self.resultado.setPlainText(salida)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")


# Ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = JacobiApp()
    ventana.show()
    sys.exit(app.exec_())
