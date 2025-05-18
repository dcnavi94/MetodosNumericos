# ===== IMPORTACIÓN DE LIBRERÍAS NECESARIAS =====
import sys  # Para terminar la app correctamente desde la línea de comandos

# Módulos de PyQt5 para crear la interfaz
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QProgressBar
)

# Módulos de Matplotlib para graficar dentro de la ventana
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# SymPy: para interpretar y transformar expresiones matemáticas desde texto
from sympy import sympify, lambdify, Symbol

# NumPy: para generar rangos de valores numéricos y evaluar funciones matemáticas
import numpy as np

# ===== CLASE PRINCIPAL DE LA INTERFAZ =====
class FalsaPosicionApp(QWidget):
    def __init__(self):
        super().__init__()

        # Título y tamaño inicial de la ventana
        self.setWindowTitle("Método de Falsa Posición")
        self.setGeometry(100, 100, 800, 700)

        # Layout principal tipo columna (vertical)
        layout = QVBoxLayout()

        # ===== ENTRADAS DEL USUARIO =====

        # Campo para ingresar la función f(x)
        layout.addWidget(QLabel("Función f(x):"))
        self.input_funcion = QLineEdit("x**2 - 4")  # Valor inicial por defecto
        layout.addWidget(self.input_funcion)

        # Campo para extremo inferior del intervalo (a)
        layout.addWidget(QLabel("Extremo inferior (a):"))
        self.input_a = QLineEdit("0")
        layout.addWidget(self.input_a)

        # Campo para extremo superior del intervalo (b)
        layout.addWidget(QLabel("Extremo superior (b):"))
        self.input_b = QLineEdit("3")
        layout.addWidget(self.input_b)

        # Campo para ingresar la tolerancia deseada
        layout.addWidget(QLabel("Tolerancia:"))
        self.input_tol = QLineEdit("0.0001")
        layout.addWidget(self.input_tol)

        # ===== BOTÓN PARA EJECUTAR EL MÉTODO =====
        self.btn_calcular = QPushButton("Calcular raíz y graficar")
        self.btn_calcular.clicked.connect(self.calcular_raiz)  # Conecta clic con la función
        layout.addWidget(self.btn_calcular)

        # ===== BARRA DE PROGRESO =====
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)  # Valor mínimo (0%)
        self.progress_bar.setMaximum(100)  # Valor máximo (100%)
        layout.addWidget(self.progress_bar)

        # ===== TABLA PARA MOSTRAR EL HISTORIAL DE ITERACIONES =====
        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        # ===== LIENZO PARA GRAFICAR CON MATPLOTLIB =====
        self.figura = Figure(figsize=(6, 4))  # Crea el objeto de figura
        self.canvas = FigureCanvas(self.figura)  # Lo integra al GUI como un widget
        layout.addWidget(self.canvas)

        # Aplica el layout a la ventana
        self.setLayout(layout)

    # ===== FUNCIÓN PRINCIPAL: MÉTODO DE FALSA POSICIÓN CON VISUALIZACIÓN =====
    def calcular_raiz(self):
        try:
            # --- PREPARACIÓN DE LA FUNCIÓN MATEMÁTICA ---
            x = Symbol('x')  # Declaramos símbolo 'x' para SymPy
            f_expr = sympify(self.input_funcion.text())  # Convertimos texto en expresión simbólica
            f = lambdify(x, f_expr, "numpy")  # Creamos función numérica evaluable con NumPy

            # --- LECTURA DE VALORES DESDE LOS CAMPOS DE TEXTO ---
            a = float(self.input_a.text())
            b = float(self.input_b.text())
            tol = float(self.input_tol.text())

            # Validación: asegurarse de que haya cambio de signo
            if f(a) * f(b) >= 0:
                raise ValueError("f(a) y f(b) deben tener signos opuestos para aplicar el método.")

            historial = []  # Lista para almacenar las iteraciones
            max_iteraciones = 100  # Límite para evitar ciclos infinitos
            contador = 0  # Contador de iteraciones

            # --- BUCLE DEL MÉTODO DE FALSA POSICIÓN ---
            while abs(b - a) > tol and contador < max_iteraciones:
                fa = f(a)
                fb = f(b)

                # Calcular el punto c usando interpolación lineal
                c = a - fa * (b - a) / (fb - fa)
                fc = f(c)

                # Guardar los datos de esta iteración
                historial.append((contador + 1, a, b, c, fa, fb, fc))

                # Elegir el nuevo subintervalo [a, b]
                if fa * fc < 0:
                    b = c
                else:
                    a = c

                # Actualizar la barra de progreso visualmente
                progreso = int((contador / max_iteraciones) * 100)
                self.progress_bar.setValue(progreso)

                contador += 1

            # Al finalizar, asegúrate de mostrar la barra completa
            self.progress_bar.setValue(100)

            # --- MOSTRAR HISTORIAL EN LA TABLA ---
            self.tabla.setRowCount(len(historial))  # Número de filas según iteraciones
            self.tabla.setColumnCount(7)  # Columnas: Iteración, a, b, c, f(a), f(b), f(c)
            self.tabla.setHorizontalHeaderLabels([
                "Iteración", "a", "b", "c", "f(a)", "f(b)", "f(c)"
            ])

            for i, fila in enumerate(historial):
                for j, valor in enumerate(fila):
                    self.tabla.setItem(i, j, QTableWidgetItem(f"{valor:.6f}"))

            # --- GRAFICAR FUNCIÓN Y APROXIMACIONES ---
            self.figura.clear()  # Limpiar gráfico anterior
            ax = self.figura.add_subplot(111)  # Agregar gráfico principal

            # Generar puntos para graficar f(x)
            x_vals = np.linspace(historial[0][1] - 1, historial[0][2] + 1, 400)
            y_vals = f(x_vals)

            # Dibujar la curva de la función
            ax.plot(x_vals, y_vals, label='f(x)', color='blue')
            ax.axhline(0, color='black', linewidth=0.5)  # Línea del eje X

            # Dibujar puntos c (aproximaciones) en rojo
            puntos_x = [fila[3] for fila in historial]
            puntos_y = [fila[6] for fila in historial]
            ax.scatter(puntos_x, puntos_y, color='red', label='Aproximaciones c')

            # Añadir detalles a la gráfica
            ax.set_title("Método de Falsa Posición")
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.legend()
            ax.grid(True)

            # Mostrar la gráfica en el canvas
            self.canvas.draw()

        # --- MANEJO DE ERRORES ---
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))  # Muestra un mensaje emergente


# ===== BLOQUE PRINCIPAL: ARRANQUE DE LA APLICACIÓN =====
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Crear instancia de la app
    ventana = FalsaPosicionApp()  # Crear objeto de la clase
    ventana.show()  # Mostrar la ventana
    sys.exit(app.exec_())  # Ejecutar el loop de eventos
