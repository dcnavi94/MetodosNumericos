import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox, QGridLayout
)
import numpy as np


class FactorizacionLUApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Factorización LU (Sistema 3x3 Formato ax + by + cz = d)")
        self.setGeometry(200, 200, 750, 700)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("🔢 Ingrese el sistema de ecuaciones en forma ax + by + cz = d"))

        # === Entradas organizadas como ecuaciones ===
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

        # Botón para resolver
        self.btn_resolver = QPushButton("Resolver con Factorización LU")
        self.btn_resolver.clicked.connect(self.factorizar)
        layout.addWidget(self.btn_resolver)

        # Área de resultados
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def factorizar(self):
        try:
            # Leer matriz A y vector b desde inputs
            A = np.zeros((3, 3))
            b = np.zeros(3)

            for i in range(3):
                for j in range(3):
                    A[i, j] = float(self.inputs_A[i][j].text())
                b[i] = float(self.inputs_b[i].text())

            salida = "📌 Matriz A:\n" + str(A) + "\n\n"
            salida += "📌 Vector b:\n" + str(b) + "\n\n"

            # Inicializar L y U
            n = 3
            L = np.identity(n)
            U = np.zeros((n, n))

            # === Factorización LU (sin pivoteo) ===
            for i in range(n):
                for j in range(i, n):
                    suma = sum(L[i][k] * U[k][j] for k in range(i))
                    U[i][j] = A[i][j] - suma

                for j in range(i + 1, n):
                    suma = sum(L[j][k] * U[k][i] for k in range(i))
                    if U[i][i] == 0:
                        raise ZeroDivisionError("División por cero en U.")
                    L[j][i] = (A[j][i] - suma) / U[i][i]

            salida += "🧮 Matriz L (triangular inferior):\n" + str(L) + "\n\n"
            salida += "🧮 Matriz U (triangular superior):\n" + str(U) + "\n\n"

            # === Sustitución hacia adelante: Ly = b ===
            y = np.zeros(n)
            for i in range(n):
                y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))

            salida += "📐 Solución intermedia (Ly = b):\n" + str(y) + "\n\n"

            # === Sustitución hacia atrás: Ux = y ===
            x = np.zeros(n)
            for i in reversed(range(n)):
                if U[i][i] == 0:
                    raise ZeroDivisionError("División por cero en U.")
                x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]

            salida += "✅ Solución del sistema Ax = b:\n"
            for i in range(n):
                salida += f"x{i + 1} = {x[i]:.6f}\n"

            self.resultado.setPlainText(salida)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")


# === Lanzar la aplicación ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FactorizacionLUApp()
    ventana.show()
    sys.exit(app.exec_())
