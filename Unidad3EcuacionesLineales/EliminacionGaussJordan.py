import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox, QGridLayout
)
import numpy as np


class GaussJordanApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gauss-Jordan con Análisis del Sistema")
        self.setGeometry(200, 200, 700, 700)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("🔢 Sistema de 3 ecuaciones (forma: ax + by + cz = d):"))

        # === Entradas organizadas: x, y, z, =, resultado ===
        self.inputs = []
        grid = QGridLayout()
        labels = ["x", "y", "z", "=", "resultado"]

        for j, label in enumerate(labels):
            grid.addWidget(QLabel(label), 0, j)

        for i in range(3):
            fila = []
            for j in range(4):  # 3 coeficientes + 1 resultado
                campo = QLineEdit()
                campo.setFixedWidth(60)
                grid.addWidget(campo, i + 1, j)
                fila.append(campo)
            self.inputs.append(fila)

        layout.addLayout(grid)

        # Botón para resolver
        self.btn_resolver = QPushButton("Resolver con Gauss-Jordan")
        self.btn_resolver.clicked.connect(self.resolver)
        layout.addWidget(self.btn_resolver)

        # Área de resultados explicativos
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def resolver(self):
        try:
            # === Leer la matriz aumentada 3x4 ===
            A = np.zeros((3, 4), dtype=float)
            for i in range(3):
                for j in range(4):
                    A[i, j] = float(self.inputs[i][j].text())

            salida = "📌 Matriz aumentada inicial:\n"
            salida += str(A) + "\n\n"

            # === Aplicar Gauss-Jordan ===
            n = 3
            for i in range(n):
                # Buscar el pivote
                if A[i, i] == 0:
                    for k in range(i+1, n):
                        if A[k, i] != 0:
                            A[[i, k]] = A[[k, i]]
                            salida += f"↔ Intercambio de filas {i+1} y {k+1}\n"
                            salida += str(A) + "\n\n"
                            break
                    else:
                        continue  # pivote sigue siendo 0, no operamos

                pivote = A[i, i]
                if pivote == 0:
                    continue  # no se puede normalizar

                # Normalizar fila
                A[i] = A[i] / pivote
                salida += f"➗ Fila {i+1} dividida entre {pivote:.4f} para hacer pivote 1:\n"
                salida += str(A) + "\n\n"

                # Eliminar elementos arriba y abajo
                for j in range(n):
                    if i != j:
                        factor = A[j, i]
                        A[j] = A[j] - factor * A[i]
                        salida += f"➖ Fila {j+1} menos {factor:.4f} * Fila {i+1}:\n"
                        salida += str(A) + "\n\n"

            # === Análisis del sistema ===
            salida += "🧠 Análisis del sistema:\n"
            sistema = "Compatible determinado (una única solución)"

            # Revisar filas con ceros
            for i in range(n):
                if np.allclose(A[i, :3], 0) and not np.isclose(A[i, 3], 0):
                    sistema = "❌ Incompatible (sin solución)"
                    break
                elif np.allclose(A[i, :3], 0) and np.isclose(A[i, 3], 0):
                    sistema = "⚠️ Compatible indeterminado (infinitas soluciones)"

            salida += f"📋 Clasificación: {sistema}\n\n"

            if sistema == "Compatible determinado (una única solución)":
                salida += "✅ Solución del sistema:\n"
                for i in range(n):
                    salida += f"x{i+1} = {A[i, 3]:.6f}\n"

            self.resultado.setPlainText(salida)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")


# === Ejecutar aplicación ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GaussJordanApp()
    ventana.show()
    sys.exit(app.exec_())
