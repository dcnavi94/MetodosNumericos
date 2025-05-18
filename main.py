import sys
import os
import importlib.util
import inspect
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTreeWidget,
    QTreeWidgetItem, QMenuBar, QAction, QMenu, QDialog, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MetodoNumericoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📘 Menú de Métodos Numéricos ")
        self.setGeometry(200, 100, 700, 600)

        # Menú superior
        menu_bar = self.menuBar()
        archivo_menu = menu_bar.addMenu("Archivo")
        archivo_menu.addAction(self._crear_accion("Salir", self.close))

        ayuda_menu = menu_bar.addMenu("Ayuda")
        ayuda_menu.addAction(self._crear_accion("Acerca de", self.mostrar_acerca_de))

        # Crear carpeta de documentación
        os.makedirs("documentacion", exist_ok=True)

        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Árbol de unidades y métodos
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Metodos Numéricos"])
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.mostrar_menu_contextual)
        self.tree.itemDoubleClicked.connect(self.ejecutar_metodo)
        layout.addWidget(self.tree)

        # Íconos
        icon_folder = QIcon.fromTheme("folder")
        icon_method = QIcon.fromTheme("applications-education")

        # Recorrer carpetas de unidades
        for unidad in sorted(os.listdir()):
            if os.path.isdir(unidad) and unidad.startswith("Unidad"):
                nodo_unidad = QTreeWidgetItem([unidad])
                nodo_unidad.setIcon(0, icon_folder)
                self.tree.addTopLevelItem(nodo_unidad)

                carpeta_path = os.path.join(os.getcwd(), unidad)
                for archivo in sorted(os.listdir(carpeta_path)):
                    if archivo.endswith('.py') and not archivo.startswith('__'):
                        nombre_modulo = archivo[:-3]
                        ruta_modulo = os.path.join(carpeta_path, archivo)
                        clase = self._cargar_clase_app(unidad, nombre_modulo, ruta_modulo)
                        if clase:
                            display_name = clase.__name__.replace('App', '')
                            nodo_metodo = QTreeWidgetItem([display_name])
                            nodo_metodo.setIcon(0, icon_method)
                            nodo_metodo.setData(0, Qt.UserRole, (clase, unidad))
                            nodo_unidad.addChild(nodo_metodo)
                            # Crear teoría si falta
                            self._crear_teoria(clase, unidad)

    def _crear_accion(self, nombre, funcion):
        accion = QAction(nombre, self)
        accion.triggered.connect(funcion)
        return accion

    def _cargar_clase_app(self, unidad, modulo_nombre, ruta):
        spec = importlib.util.spec_from_file_location(f"{unidad}.{modulo_nombre}", ruta)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            for _, obj in inspect.getmembers(mod, inspect.isclass):
                if obj.__module__ == mod.__name__ and obj.__name__.endswith("App"):
                    return obj
        except Exception as e:
            print(f"Error cargando módulo {modulo_nombre}: {e}")
        return None

    def ejecutar_metodo(self, item, _col):
        data = item.data(0, Qt.UserRole)
        if data:
            clase, _ = data
            ventana = clase()
            ventana.setWindowIcon(QIcon.fromTheme("applications-education"))
            ventana.show()
            setattr(self, f"win_{clase.__name__}", ventana)

    def mostrar_menu_contextual(self, pos):
        item = self.tree.itemAt(pos)
        data = item.data(0, Qt.UserRole) if item else None
        if data:
            clase, unidad = data
            menu = QMenu()
            menu.addAction("📖 Ver teoría", lambda: self.ver_teoria(clase, unidad))
            menu.exec_(self.tree.viewport().mapToGlobal(pos))

    def ver_teoria(self, clase, unidad):
        nombre_html = clase.__name__.replace('App', '').lower() + '.html'
        ruta = os.path.join('documentacion', unidad, nombre_html)
        if not os.path.exists(ruta):
            QMessageBox.information(self, "Sin teoría", f"No existe teoría para {clase.__name__}.")
            return
        # Mostrar HTML con QWebEngineView
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Teoría - {clase.__name__}")
        vlayout = QVBoxLayout(dlg)
        view = QWebEngineView()
        url = QUrl.fromLocalFile(os.path.abspath(ruta))
        view.load(url)
        vlayout.addWidget(view)
        dlg.resize(800, 600)
        dlg.exec_()

    def _crear_teoria(self, clase, unidad):
        nombre_html = clase.__name__.replace('App', '').lower() + '.html'
        carpeta = os.path.join('documentacion', unidad)
        os.makedirs(carpeta, exist_ok=True)
        ruta = os.path.join(carpeta, nombre_html)
        if not os.path.exists(ruta):
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>{clase.__name__.replace('App','')}</title></head>
<body>
  <h1>{clase.__name__.replace('App','')}</h1>
  <p>Descripción del método...</p>
</body>
</html>""")

    def mostrar_acerca_de(self):
        QMessageBox.information(
            self,
            "Acerca de",
            "Aplicación de métodos numéricos con PyQt5\nHecho por Iván Carapia"
        )

if __name__ == '__main__':
    # Inicializar Qt WebEngine
    from PyQt5.QtWebEngineWidgets import QWebEngineProfile
    app = QApplication(sys.argv)
    win = MetodoNumericoApp()
    win.show()
    sys.exit(app.exec_())