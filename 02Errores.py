import sys

# Importamos los módulos necesarios de PyQt5
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTextEdit
)

# Importamos módulos de Matplotlib para graficar en la interfaz
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class TiposErroresApp(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración inicial de la ventana
        self.setWindowTitle("Tipos de Errores Numéricos")
        self.setGeometry(200, 200, 550, 700)

        # Layout vertical principal
        layout = QVBoxLayout()

        # ======= INSTRUCCIONES Y FÓRMULAS =======
        layout.addWidget(QLabel("📘 Instrucciones:"))
        layout.addWidget(QLabel("Ingresa un valor verdadero y un valor aproximado."))

        # Mostramos las fórmulas de los errores en texto
        layout.addWidget(QLabel("📐 Fórmulas utilizadas:"))
        layout.addWidget(QLabel("• Error absoluto = |valor verdadero - valor aproximado|"))
        layout.addWidget(QLabel("• Error relativo = Error absoluto / |valor verdadero|"))
        layout.addWidget(QLabel("• Error porcentual = Error relativo × 100"))

        # ======= ENTRADAS =======
        layout.addWidget(QLabel("🟦 Valor verdadero:"))
        self.input_valor_verdadero = QLineEdit("3.1416")  # Valor preestablecido
        layout.addWidget(self.input_valor_verdadero)

        layout.addWidget(QLabel("🟨 Valor aproximado:"))
        self.input_valor_aproximado = QLineEdit("3.14")
        layout.addWidget(self.input_valor_aproximado)

        # ======= BOTÓN DE CÁLCULO =======
        self.boton_calcular = QPushButton("Calcular errores")
        self.boton_calcular.clicked.connect(self.calcular_errores)
        layout.addWidget(self.boton_calcular)

        # ======= ÁREA DE RESULTADOS =======
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)  # Solo lectura
        layout.addWidget(self.resultado)

        # ======= ÁREA DE LA GRÁFICA =======
        self.figura = Figure(figsize=(5, 3))  # Crea figura de matplotlib
        self.canvas = FigureCanvas(self.figura)  # Canvas para integrarla a PyQt
        layout.addWidget(self.canvas)

        # Aplicamos el layout a la ventana principal
        self.setLayout(layout)

    def calcular_errores(self):
        try:
            # Convertimos las entradas a valores flotantes
            verdadero = float(self.input_valor_verdadero.text())
            aproximado = float(self.input_valor_aproximado.text())

            # ======= CÁLCULO DE ERRORES =======

            # Error absoluto: diferencia directa en valor
            error_absoluto = abs(verdadero - aproximado)

            # Error relativo: proporción del error respecto al valor verdadero
            error_relativo = error_absoluto / abs(verdadero)

            # Error porcentual: el error relativo expresado en porcentaje
            error_porcentual = error_relativo * 100

            # ======= MOSTRAR RESULTADOS EN TEXTO =======
            salida = (
                f"🔎 Valor verdadero: {verdadero}\n"
                f"🔎 Valor aproximado: {aproximado}\n\n"
                f"📏 Error absoluto = |{verdadero} - {aproximado}| = {error_absoluto:.6f}\n"
                f"📏 Error relativo = {error_absoluto:.6f} / |{verdadero}| = {error_relativo:.6f}\n"
                f"📏 Error porcentual = {error_relativo:.6f} × 100 = {error_porcentual:.4f}%"
            )
            self.resultado.setPlainText(salida)

            # ======= GRAFICAR LOS ERRORES =======
            self.figura.clear()  # Limpiar gráfica anterior
            ax = self.figura.add_subplot(111)  # Crear un solo gráfico

            # Datos y etiquetas para las barras
            etiquetas = ["Absoluto", "Relativo", "Porcentual (%)"]
            valores = [error_absoluto, error_relativo, error_porcentual]

            # Crear la gráfica de barras
            ax.bar(etiquetas, valores, color=['blue', 'orange', 'green'])

            # Personalizar la gráfica
            ax.set_title("Visualización de los Errores")
            ax.set_ylabel("Magnitud del Error")
            ax.grid(True, linestyle='--', alpha=0.5)

            # Renderizar la gráfica en la interfaz
            self.canvas.draw()

        except Exception as e:
            # Si ocurre un error (como letras en lugar de números), mostrar mensaje
            QMessageBox.critical(self, "Error", f"Ocurrió un problema: {str(e)}")


# ======= EJECUCIÓN DE LA APLICACIÓN =======
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = TiposErroresApp()
    ventana.show()
    sys.exit(app.exec_())
