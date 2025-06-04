import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os

# Base de datos
DATABASE = 'impuestos.db'

# Función para obtener la ruta de los recursos
def get_resource_path(relative_path):
    """Obtiene la ruta del recurso tanto en desarrollo como en el ejecutable."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class VentanaImpuestos(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Impuestos')
        self.setGeometry(250, 250, 400, 400)

        layout = QVBoxLayout()

        self.campos_impuestos = {}
        naftas = ['gasoil', 'diesel', 'nafta_super', 'nafta_euro']
        impuestos = ['icl', 'idc']

        for nafta in naftas:
            h_layout = QHBoxLayout()
            for impuesto in impuestos:
                label = QLabel(f'{nafta.replace("_", " ").capitalize()} {impuesto.upper()}')
                label.setFont(QFont("Roboto", 10))
                spin_box = QDoubleSpinBox()
                spin_box.setRange(0, 100000)
                spin_box.setDecimals(3)
                spin_box.setPrefix("$")
                h_layout.addWidget(label)
                h_layout.addWidget(spin_box)
                self.campos_impuestos[f'{nafta}_{impuesto}'] = spin_box
            layout.addLayout(h_layout)

        self.boton_guardar = QPushButton('Guardar', self)
        self.boton_guardar.clicked.connect(self.guardar_impuestos)
        self.boton_guardar.setFixedSize(150, 50)

        self.boton_resetear = QPushButton("Borrar", self)
        self.boton_resetear.clicked.connect(self.resetear_spinbox)
        self.boton_resetear.setFixedSize(150, 50)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.boton_guardar)
        hbox.addWidget(self.boton_resetear)
        hbox.addStretch(1)
        layout.addLayout(hbox)

        self.setLayout(layout)
        self.cargar_impuestos()

    """Función para establecer el valor de todos los QDoubleSpinBox en 0."""
    def resetear_spinbox(self):
        for key in self.campos_impuestos.keys():
            self.campos_impuestos[key].setValue(0)

    def cargar_impuestos(self):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT * FROM impuestos WHERE id=1')
        row = c.fetchone()
        if row:
            for i, key in enumerate(self.campos_impuestos.keys(), start=1):
                self.campos_impuestos[key].setValue(row[i])
        conn.close()

    def guardar_impuestos(self):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        valores = [self.campos_impuestos[key].value() for key in self.campos_impuestos.keys()]
        c.execute('''
            INSERT OR REPLACE INTO impuestos (
                id, 
                gasoil_icl, gasoil_idc, 
                diesel_icl, diesel_idc, 
                nafta_super_icl, nafta_super_idc, 
                nafta_euro_icl, nafta_euro_idc
            )
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', valores)
        conn.commit()
        conn.close()
        QMessageBox.information(self, 'Guardado', 'Valores de impuestos guardados exitosamente.')


class VentanaFacturas(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tipo de Factura')
        self.setGeometry(250, 250, 700, 600)

        layout = QVBoxLayout()

        # --- Mostrar valores de impuestos ---
        self.label_impuestos = QLabel('Valores de Impuestos')
        self.label_impuestos.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.label_impuestos)

        self.labels_naftas = {}
        naftas = ['gasoil', 'diesel', 'nafta_super', 'nafta_euro']
        impuestos = ['icl', 'idc']

        grid_naftas = QGridLayout()
        row = 0
        for nafta in naftas:
            for col, impuesto in enumerate(impuestos):
                label = QLabel(f'{nafta.capitalize().replace("_", " ")} {impuesto.upper()}:')
                label.setFont(QFont("Roboto", 10))
                self.labels_naftas[f'{nafta}_{impuesto}'] = label
                grid_naftas.addWidget(label, row, col)
            row += 1

        layout.addLayout(grid_naftas)

        # Separador
        layout.addSpacerItem(QSpacerItem(20, 30))
        linea2 = QFrame()
        linea2.setFrameShape(QFrame.HLine)
        linea2.setFrameShadow(QFrame.Sunken)
        layout.addWidget(linea2)

        # Título sección Entrada de Datos
        self.label_titulo_naftas = QLabel("Entrada de Datos")
        self.label_titulo_naftas.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.label_titulo_naftas)

        # --- Sección para ingresar valores y litros ---
        self.labels = {}
        self.spin_boxes = {}
        self.litros_spin_boxes = {}

        grid_valores = QGridLayout()
        grid_valores.addWidget(QLabel("Precio Final"), 0, 1)
        grid_valores.addWidget(QLabel('Litros'), 0, 2)

        row = 1
        for nafta in naftas:
            label = QLabel(f'{nafta.capitalize().replace("_", " ")}')
            label.setFont(QFont("Roboto", 10))

            spin_box = QDoubleSpinBox(self)
            spin_box.setRange(0, 100000)
            spin_box.setDecimals(2)
            spin_box.setPrefix("$")

            litros_spin_box = QDoubleSpinBox(self)
            litros_spin_box.setRange(0, 100000)
            litros_spin_box.setDecimals(2)
            litros_spin_box.setSuffix("Lts")
            litros_spin_box.setFont(QFont("Roboto", 8))

            self.labels[nafta] = label
            self.spin_boxes[nafta] = spin_box
            self.litros_spin_boxes[nafta] = litros_spin_box

            grid_valores.addWidget(label, row, 0)
            grid_valores.addWidget(spin_box, row, 1)
            grid_valores.addWidget(litros_spin_box, row, 2)
            row += 1

        layout.addLayout(grid_valores)

        # --- Botones Factura A, Factura B y Botón Papelera ---
        self.boton_factura_a = QPushButton('Factura A', self)
        self.boton_factura_a.clicked.connect(self.calcular_factura_a)
        self.boton_factura_a.setFixedSize(200, 50)

        self.boton_factura_b = QPushButton('Factura B', self)
        self.boton_factura_b.clicked.connect(self.calcular_factura_b)
        self.boton_factura_b.setFixedSize(200, 50)

        # Botón de papelera para resetear precios y litros
        self.boton_basurero = QPushButton(self)
        icono_basurero = get_resource_path('iconos/basurero.ico')
        self.boton_basurero.setIcon(QIcon(icono_basurero))
        self.boton_basurero.setIconSize(QSize(32, 32))
        self.boton_basurero.setToolTip("Borrar precios y litros")
        self.boton_basurero.clicked.connect(self.resetear_campos_factura)
        # Lo dejamos del mismo alto que los otros dos botones:
        self.boton_basurero.setFixedSize(50, 50)

        hbox_botones = QHBoxLayout()
        hbox_botones.addWidget(self.boton_factura_a)
        hbox_botones.addWidget(self.boton_factura_b)
        hbox_botones.addWidget(self.boton_basurero)  # <-- botón de basura a la derecha
        layout.addLayout(hbox_botones)

        # --- Área de texto para mostrar resultados ---
        self.resultados_texto = QTextEdit(self)
        self.resultados_texto.setReadOnly(True)
        self.resultados_texto.setFont(QFont("Rockwell", 16))
        layout.addWidget(self.resultados_texto)

        self.setLayout(layout)

        # 1) Cargo los valores de ICL e IDC en las etiquetas
        self.cargar_valores_impuestos()
        # 2) Cargo los últimos valores de PRECIOS (sin litros) en los spin boxes
        self.cargar_ultimos_valores()

    def cargar_valores_impuestos(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        naftas = ['gasoil', 'diesel', 'nafta_super', 'nafta_euro']
        impuestos = ['icl', 'idc']

        cursor.execute('SELECT * FROM impuestos WHERE id = 1')
        fila = cursor.fetchone()
        conn.close()
        if fila:
            for idx, nafta in enumerate(naftas):
                for impuesto in impuestos:
                    valor = fila[idx * 2 + (0 if impuesto == 'icl' else 1) + 1]
                    label = self.labels_naftas.get(f'{nafta}_{impuesto}')
                    if label:
                        label.setText(f'{nafta.capitalize().replace("_", " ")} {impuesto.upper()}: {valor}')
                    setattr(self, f'{nafta}_{impuesto}', valor)

    def cargar_ultimos_valores(self):
        """Lee únicamente los valores de PRECIO y los asigna a los spin boxes correspondientes."""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT gasoil_precio, diesel_precio, nafta_super_precio, nafta_euro_precio
            FROM ultimos_valores WHERE id = 1
        ''')
        fila = cursor.fetchone()
        conn.close()

        if fila:
            # fila = (gasoil_precio, diesel_precio, nafta_super_precio, nafta_euro_precio)
            self.spin_boxes['gasoil'].setValue(fila[0])
            self.spin_boxes['diesel'].setValue(fila[1])
            self.spin_boxes['nafta_super'].setValue(fila[2])
            self.spin_boxes['nafta_euro'].setValue(fila[3])
            # NOTA: no modificamos los litros; quedan en 0 o en el valor que el usuario ingrese

    def guardar_ultimos_valores(self):
        """Toma los valores actuales de Precio para cada nafta y los persiste en SQLite."""
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        gasoil_precio     = self.spin_boxes['gasoil'].value()
        diesel_precio     = self.spin_boxes['diesel'].value()
        nafta_sup_precio  = self.spin_boxes['nafta_super'].value()
        nafta_euro_precio = self.spin_boxes['nafta_euro'].value()

        c.execute('''
            INSERT OR REPLACE INTO ultimos_valores (
                id,
                gasoil_precio,
                diesel_precio,
                nafta_super_precio,
                nafta_euro_precio
            ) VALUES (
                1, ?, ?, ?, ?
            )
        ''', (
            gasoil_precio,
            diesel_precio,
            nafta_sup_precio,
            nafta_euro_precio
        ))

        conn.commit()
        conn.close()

    def calcular_factura_a(self):
        try:
            resultados = {}
            total_idc = 0
            total_icl = 0

            for key in self.spin_boxes.keys():
                valor_nafta = self.spin_boxes[key].value()      # Precio ingresado
                valor_litros = self.litros_spin_boxes[key].value()  # Litros ingresados

                if valor_nafta > 0 and valor_litros > 0:
                    icl = getattr(self, f"{key}_icl")  # Valor ICL
                    idc = getattr(self, f"{key}_idc")  # Valor IDC

                    resultado = round((valor_nafta - icl - idc) / 1.21, 2)
                    resultados[key] = resultado
                    total_icl += icl * valor_litros
                    total_idc += idc * valor_litros

            if resultados:
                self.mostrar_resultados(resultados, total_icl, total_idc, "Factura A")
                # Guardar únicamente los precios en la BD
                self.guardar_ultimos_valores()
            else:
                QMessageBox.warning(self, 'Advertencia', 'Por favor, ingrese valores válidos para los cálculos.')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Ocurrió un error: {e}')

    def calcular_factura_b(self):
        try:
            resultados = {}
            total_idc = 0
            total_icl = 0

            for key in self.spin_boxes.keys():
                valor_nafta = self.spin_boxes[key].value()
                valor_litros = self.litros_spin_boxes[key].value()

                if valor_nafta > 0 and valor_litros > 0:
                    icl = getattr(self, f"{key}_icl")
                    idc = getattr(self, f"{key}_idc")

                    resultado = round((valor_nafta - icl - idc) / 1.21, 2)
                    resultado_b = round(resultado * 0.21 + resultado, 2)
                    resultados[key] = resultado_b
                    total_icl += icl * valor_litros
                    total_idc += idc * valor_litros

            if resultados:
                self.mostrar_resultados(resultados, total_icl, total_idc, "Factura B")
                # Guardar únicamente los precios en la BD
                self.guardar_ultimos_valores()
            else:
                QMessageBox.warning(self, 'Advertencia', 'Por favor, ingrese valores válidos para los cálculos.')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Ocurrió un error: {e}')

    def mostrar_resultados(self, resultados, total_icl, total_idc, tipo):
        try:
            resultados_texto = f'Resultados ({tipo}):\n'
            resultados_texto += '\n'.join([
                f'{key.capitalize().replace("_", " ")}: {resultados[key]}' 
                for key in resultados.keys()
            ])
            resultados_texto += f'\nICL Total: {total_icl}'
            resultados_texto += f'\nIDC Total: {total_idc}'
            self.resultados_texto.setText(resultados_texto)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Ocurrió un error: {e}')

    def resetear_campos_factura(self):
        """Pone en cero todos los spin boxes de precio y de litros."""
        for nafta in self.spin_boxes.keys():
            self.spin_boxes[nafta].setValue(0)
            self.litros_spin_boxes[nafta].setValue(0)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Estación de Servicio')
        self.setGeometry(200, 200, 300, 330)
        icono_ventana_principal = get_resource_path('iconos/Fuel_station.ico')
        self.setWindowIcon(QIcon(icono_ventana_principal))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Botón “Impuestos”
        self.boton_impuestos = QPushButton('Impuestos', self)
        self.boton_impuestos.clicked.connect(self.mostrar_ventana_impuestos)
        self.boton_impuestos.setFixedSize(150, 60)
        icono_boton_impuestos = get_resource_path('iconos/impuestos.ico')
        self.boton_impuestos.setIcon(QIcon(icono_boton_impuestos))
        self.boton_impuestos.setToolTip("Cargar los valores de los impuestos")

        # Botón “Tipo de Factura”
        self.boton_facturas = QPushButton('Tipo de Factura', self)
        self.boton_facturas.clicked.connect(self.mostrar_ventana_facturas)
        self.boton_facturas.setFixedSize(150, 60)
        icono_boton_facturas = get_resource_path('iconos/Facturas.ico')
        self.boton_facturas.setIcon(QIcon(icono_boton_facturas))
        self.boton_facturas.setToolTip("Cálculo del valor para facturas A y B")

        h_layout_impuestos = QHBoxLayout()
        h_layout_impuestos.addStretch(1)
        h_layout_impuestos.addWidget(self.boton_impuestos)
        h_layout_impuestos.addStretch(1)

        h_layout_facturas = QHBoxLayout()
        h_layout_facturas.addStretch(1)
        h_layout_facturas.addWidget(self.boton_facturas)
        h_layout_facturas.addStretch(1)

        layout.addLayout(h_layout_impuestos)
        layout.addLayout(h_layout_facturas)

    def mostrar_ventana_impuestos(self):
        self.ventana_impuestos = VentanaImpuestos()
        icono_ventana_impuestos = get_resource_path('iconos/impuestos.ico')
        self.ventana_impuestos.setWindowIcon(QIcon(icono_ventana_impuestos))
        self.ventana_impuestos.show()

    def mostrar_ventana_facturas(self):
        self.ventana_facturas = VentanaFacturas()
        icono_ventana_facturas = get_resource_path('iconos/Facturas.ico')
        self.ventana_facturas.setWindowIcon(QIcon(icono_ventana_facturas))
        self.ventana_facturas.show()


def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # --- Tabla de Impuestos ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS impuestos (
            id INTEGER PRIMARY KEY,
            gasoil_icl REAL,
            gasoil_idc REAL,
            diesel_icl REAL,
            diesel_idc REAL,
            nafta_super_icl REAL,
            nafta_super_idc REAL,
            nafta_euro_icl REAL,
            nafta_euro_idc REAL
        )
    ''')

    # --- Nueva tabla para ALMACENAR SOLO PRECIOS (sin litros) ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS ultimos_valores (
            id INTEGER PRIMARY KEY,
            gasoil_precio REAL,
            diesel_precio REAL,
            nafta_super_precio REAL,
            nafta_euro_precio REAL
        )
    ''')

    conn.commit()
    conn.close()


def insert_initial_data():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # —————— Impuestos (si no existe el registro) ——————
    c.execute('SELECT COUNT(*) FROM impuestos WHERE id = 1')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO impuestos (
                id, gasoil_icl, gasoil_idc,
                diesel_icl, diesel_idc,
                nafta_super_icl, nafta_super_idc,
                nafta_euro_icl, nafta_euro_idc
            ) VALUES (1, 0, 0, 0, 0, 0, 0, 0, 0)
        ''')

    # —————— Últimos valores de PRECIO (sin litros) ——————
    c.execute('SELECT COUNT(*) FROM ultimos_valores WHERE id = 1')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO ultimos_valores (
                id,
                gasoil_precio,
                diesel_precio,
                nafta_super_precio,
                nafta_euro_precio
            ) VALUES (1, 0, 0, 0, 0)
        ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    insert_initial_data()

    app = QApplication([])
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
    app.exec_()
