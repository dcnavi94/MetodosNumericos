import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline


class InterpolacionSplineApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interpolación Spline Cúbica")
        self.setGeometry(200, 200, 600, 500)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("📌 Ingrese los puntos x separados por coma (ej: 1,2,3):"))
        self.input_x = QLineEdit()
        layout.addWidget(self.input_x)

        layout.addWidget(QLabel("📌 Ingrese los puntos y correspondientes (ej: 2,4,6):"))
        self.input_y = QLineEdit()
        layout.addWidget(self.input_y)

        layout.addWidget(QLabel("🔍 Punto a interpolar:"))
        self.input_eval = QLineEdit()
        layout.addWidget(self.input_eval)

        self.btn_calcular = QPushButton("Calcular Interpolación Spline")
        self.btn_calcular.clicked.connect(self.interpolar)
        layout.addWidget(self.btn_calcular)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def interpolar(self):
        try:
            x = np.array([float(i.strip()) for i in self.input_x.text().split(',')])
            y = np.array([float(i.strip()) for i in self.input_y.text().split(',')])
            x_eval = float(self.input_eval.text())

            if len(x) != len(y):
                raise ValueError("Los vectores x e y deben tener la misma longitud.")

            cs = CubicSpline(x, y)
            y_interp = cs(x_eval)

            salida = f"🎯 Valor interpolado en x = {x_eval}: {y_interp:.6f}\n"
            self.resultado.setPlainText(salida)

            # Gráfica
            x_graf = np.linspace(min(x), max(x), 200)
            y_graf = cs(x_graf)

            plt.figure(figsize=(8, 5))
            plt.plot(x, y, 'ro', label='Datos')
            plt.plot(x_graf, y_graf, label='Spline Cúbico')
            plt.axvline(x_eval, color='gray', linestyle='--', label=f'x = {x_eval}')
            plt.axhline(y_interp, color='blue', linestyle='--')
            plt.scatter([x_eval], [y_interp], color='green', label='Interpolación')
            plt.title('Interpolación Spline Cúbica')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = InterpolacionSplineApp()
    ventana.show()
    sys.exit(app.exec_())
