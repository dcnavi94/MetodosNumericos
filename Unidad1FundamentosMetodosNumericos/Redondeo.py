import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
import math


class CifrasSignificativasApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cifras Significativas y Redondeo")
        self.setGeometry(200, 200, 500, 600)

        layout = QVBoxLayout()

        # ==== TEORÍA INICIAL QUE SE MUESTRA ====
        layout.addWidget(QLabel("📘 ¿Qué son las cifras significativas?"))
        layout.addWidget(QLabel("Son los dígitos que aportan información útil sobre la precisión de un número."))
        layout.addWidget(QLabel("Regla: redondear manteniendo solo los dígitos significativos más importantes."))

        layout.addWidget(QLabel("🔢 Ingresa un número:"))
        self.input_numero = QLineEdit("3.1415926535")  # valor por defecto
        layout.addWidget(self.input_numero)

        layout.addWidget(QLabel("🔢 Cantidad de cifras significativas:"))
        self.input_cifras = QLineEdit("4")
        layout.addWidget(self.input_cifras)

        # Botón para redondear
        self.btn_redondear = QPushButton("Redondear")
        self.btn_redondear.clicked.connect(self.redondear)
        layout.addWidget(self.btn_redondear)

        # Campo de salida
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def redondear(self):
        try:
            # Leer entradas
            numero = float(self.input_numero.text())
            cifras = int(self.input_cifras.text())

            if numero == 0:
                redondeado = 0.0
            else:
                # Cálculo matemático para redondeo a cifras significativas
                digitos = cifras - int(math.floor(math.log10(abs(numero)))) - 1
                redondeado = round(numero, digitos)

            # Mostrar resultados explicativos
            resultado = (
                f"Número original: {numero}\n"
                f"Cifras significativas solicitadas: {cifras}\n"
                f"Número redondeado: {redondeado}\n\n"
                "✅ Aplicando redondeo a cifras significativas se conservan únicamente "
                "los dígitos que más contribuyen al valor real del número."
            )
            self.output.setPlainText(resultado)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en entrada: {str(e)}")


# === EJECUCIÓN DE LA APP ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CifrasSignificativasApp()
    ventana.show()
    sys.exit(app.exec_())
