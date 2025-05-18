import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QTextEdit, QMessageBox
)


class PropagacionErroresApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Propagación y Acumulación de Errores")
        self.setGeometry(200, 200, 550, 700)

        layout = QVBoxLayout()

        # ==== Instrucciones iniciales ====
        layout.addWidget(QLabel("📘 Propagación de errores en operaciones numéricas"))
        layout.addWidget(QLabel("Fórmulas usadas:"))
        layout.addWidget(QLabel("Suma/Resta: Δz = Δx + Δy"))
        layout.addWidget(QLabel("Multiplicación/División: Δz/z = Δx/x + Δy/y"))

        # ==== Entradas para valores y errores ====
        layout.addWidget(QLabel("🔢 Valor x:"))
        self.input_x = QLineEdit("10.0")
        layout.addWidget(self.input_x)

        layout.addWidget(QLabel("± Error absoluto de x:"))
        self.input_ex = QLineEdit("0.2")
        layout.addWidget(self.input_ex)

        layout.addWidget(QLabel("🔢 Valor y:"))
        self.input_y = QLineEdit("5.0")
        layout.addWidget(self.input_y)

        layout.addWidget(QLabel("± Error absoluto de y:"))
        self.input_ey = QLineEdit("0.1")
        layout.addWidget(self.input_ey)

        # ==== Selección de operación ====
        layout.addWidget(QLabel("🧮 Operación:"))
        self.combo_operacion = QComboBox()
        self.combo_operacion.addItems(["Suma", "Resta", "Multiplicación", "División"])
        layout.addWidget(self.combo_operacion)

        # ==== Botón para calcular ====
        self.btn_calcular = QPushButton("Calcular propagación de error")
        self.btn_calcular.clicked.connect(self.calcular_error)
        layout.addWidget(self.btn_calcular)

        # ==== Área de resultados ====
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def calcular_error(self):
        try:
            # Leer entradas
            x = float(self.input_x.text())
            ex = float(self.input_ex.text())
            y = float(self.input_y.text())
            ey = float(self.input_ey.text())
            op = self.combo_operacion.currentText()

            if op == "Suma":
                z = x + y
                ez = ex + ey
                formula = "Δz = Δx + Δy"
            elif op == "Resta":
                z = x - y
                ez = ex + ey
                formula = "Δz = Δx + Δy"
            elif op == "Multiplicación":
                z = x * y
                ez = abs(z) * ((ex / abs(x)) + (ey / abs(y)))
                formula = "Δz/z = Δx/x + Δy/y → Δz = |z| * (Δx/|x| + Δy/|y|)"
            elif op == "División":
                z = x / y
                ez = abs(z) * ((ex / abs(x)) + (ey / abs(y)))
                formula = "Δz/z = Δx/x + Δy/y → Δz = |z| * (Δx/|x| + Δy/|y|)"
            else:
                raise ValueError("Operación no válida")

            # Mostrar resultados
            salida = (
                f"🔢 Operación: {op}\n"
                f"Fórmula usada: {formula}\n\n"
                f"Resultado numérico: z = {z:.6f}\n"
                f"Error absoluto propagado: Δz = ±{ez:.6f}\n"
                f"Intervalo de confianza: [{z - ez:.6f}, {z + ez:.6f}]"
            )
            self.resultado.setPlainText(salida)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Entrada inválida: {str(e)}")


# ==== EJECUTAR LA APP ====
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PropagacionErroresApp()
    ventana.show()
    sys.exit(app.exec_())
