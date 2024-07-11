import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Base de datos
DATABASE = 'impuestos.db'

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

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.boton_guardar)
        hbox.addStretch(1)
        layout.addLayout(hbox)

        self.setLayout(layout)
        self.cargar_impuestos()

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
            INSERT OR REPLACE INTO impuestos (id, gasoil_icl, gasoil_idc, diesel_icl, diesel_idc, nafta_super_icl, nafta_super_idc, nafta_euro_icl, nafta_euro_idc)
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
        self.setGeometry(250, 250, 600, 600)

        layout = QVBoxLayout()

        # Mostrar valores de impuestos
        self.label_impuestos = QLabel('Valores de Impuestos:')
        layout.addWidget(self.label_impuestos)
        
        self.labels_naftas = {}
        naftas = ['gasoil', 'diesel', 'nafta_super', 'nafta_euro']
        impuestos = ['icl', 'idc']
        
        grid_naftas = QGridLayout()
        row = 0
        for nafta in naftas:
            for col, impuesto in enumerate(impuestos):
                label = QLabel(f'{nafta.capitalize().replace("_", " ")} {impuesto.upper()}:')
                self.labels_naftas[f'{nafta}_{impuesto}'] = label
                grid_naftas.addWidget(label, row, col)
            row += 1
        
        layout.addLayout(grid_naftas)

        # Agregar un spacer para separar los layouts
        layout.addSpacerItem(QSpacerItem(20, 50))
    
        # Sección para ingresar valores y litros
        self.labels = {}
        self.spin_boxes = {}
        self.litros_spin_boxes = {}
        
        grid_valores = QGridLayout()
        grid_valores.addWidget(QLabel('Naftas'), 0, 0)
        grid_valores.addWidget(QLabel("Precio"), 0, 1)
        grid_valores.addWidget(QLabel('Litros'), 0, 2)
        
        row = 1
        for nafta in naftas:
            label = QLabel(f'{nafta.capitalize().replace("_", " ")}:')
            spin_box = QDoubleSpinBox(self)
            spin_box.setRange(0, 100000)
            spin_box.setDecimals(2)
            spin_box.setPrefix("$")
            
            litros_spin_box = QDoubleSpinBox(self)
            litros_spin_box.setRange(0, 100000)
            litros_spin_box.setDecimals(2)
            litros_spin_box.setSuffix("\tLitros")
            
            self.labels[nafta] = label
            self.spin_boxes[nafta] = spin_box
            self.litros_spin_boxes[nafta] = litros_spin_box

            grid_valores.addWidget(label, row, 0)
            grid_valores.addWidget(spin_box, row, 1)
            grid_valores.addWidget(litros_spin_box, row, 2)
            row += 1

        layout.addLayout(grid_valores)

        # Botones Factura A y Factura B
        self.boton_factura_a = QPushButton('Factura A', self)
        self.boton_factura_a.clicked.connect(self.calcular_factura_a)
        self.boton_factura_a.setFixedSize(200, 50)
        
        self.boton_factura_b = QPushButton('Factura B', self)
        self.boton_factura_b.clicked.connect(self.calcular_factura_b)
        self.boton_factura_b.setFixedSize(200, 50)
        
        hbox_botones = QHBoxLayout()
        hbox_botones.addWidget(self.boton_factura_a)
        hbox_botones.addWidget(self.boton_factura_b)

        layout.addLayout(hbox_botones)

        # Área de texto para mostrar resultados
        self.resultados_texto = QTextEdit(self)
        self.resultados_texto.setReadOnly(True)
        self.resultados_texto.setStyleSheet("font-size: 16pt;")  # Ajustar el tamaño de la fuente
        layout.addWidget(self.resultados_texto)

        self.setLayout(layout)
        self.cargar_valores_impuestos()

    def cargar_valores_impuestos(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        naftas = ['gasoil', 'diesel', 'nafta_super', 'nafta_euro']
        impuestos = ['icl', 'idc']

        cursor.execute('SELECT * FROM impuestos WHERE id = 1')
        fila = cursor.fetchone()
        if fila:
            for idx, nafta in enumerate(naftas):
                for impuesto in impuestos:
                    valor = fila[idx * 2 + (0 if impuesto == 'icl' else 1) + 1]  # +1 para compensar el id
                    label = self.labels_naftas.get(f'{nafta}_{impuesto}')
                    if label:
                        label.setText(f'{nafta.capitalize().replace("_", " ")} {impuesto.upper()}: {valor}')
                    setattr(self, f'{nafta}_{impuesto}', valor)
        conn.close()

    def calcular_factura_a(self):
        try:
            resultados = {}
            total_idc = 0
            total_icl = 0
            for key in self.spin_boxes.keys():
                valor = self.spin_boxes[key].value()
                litros = self.litros_spin_boxes[key].value()
                icl = getattr(self, f"{key}_icl")
                idc = getattr(self, f"{key}_idc")
                resultado = round((valor - icl - idc) / 1.21, 2)
                resultados[key] = resultado
                total_icl += icl * litros
                total_idc += idc * litros
            self.mostrar_resultados(resultados, total_icl, total_idc, "Factura A")
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Ocurrió un error: {e}')

    def calcular_factura_b(self):
        try:
            resultados = {}
            total_idc = 0
            total_icl = 0
            for key in self.spin_boxes.keys():
                valor = self.spin_boxes[key].value()
                litros = self.litros_spin_boxes[key].value()
                icl = getattr(self, f"{key}_icl")
                idc = getattr(self, f"{key}_idc")
                resultado = round((valor - icl - idc) / 1.21, 2)
                resultado_b = round(resultado * 0.21 + resultado, 2)
                resultados[key] = resultado_b
                total_icl += icl * litros
                total_idc += idc * litros
            self.mostrar_resultados(resultados, total_icl, total_idc, "Factura B")
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Ocurrió un error: {e}')

    def mostrar_resultados(self, resultados, total_icl, total_idc, tipo):
        try:
            resultados_texto = f'Resultados ({tipo}):\n'
            resultados_texto += '\n'.join([f'{key.capitalize().replace("_", " ")}: {resultados[key]}' for key in resultados.keys()])
            resultados_texto += f'\nICL Total: {total_icl}'
            resultados_texto += f'\nIDC Total: {total_idc}'
            self.resultados_texto.setText(resultados_texto)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Ocurrió un error: {e}')


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Estación de Servicio')
        self.setGeometry(200, 200, 350, 250)
        self.setWindowIcon(QIcon("S:\Proyectos\Combustible_Estacion_Servicio\Fuel_station.ico"))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Crear botones
        self.boton_impuestos = QPushButton('Impuestos', self)
        self.boton_impuestos.clicked.connect(self.mostrar_ventana_impuestos)
        self.boton_impuestos.setFixedHeight(50)

        self.boton_facturas = QPushButton('Tipo de Factura', self)
        self.boton_facturas.clicked.connect(self.mostrar_ventana_facturas)
        self.boton_facturas.setFixedHeight(50)

        
        layout.addWidget(self.boton_impuestos)
        layout.addWidget(self.boton_facturas)

    def mostrar_ventana_impuestos(self):
        self.ventana_impuestos = VentanaImpuestos()
        self.ventana_impuestos.show()

    def mostrar_ventana_facturas(self):
        self.ventana_factura_a = VentanaFacturas()
        self.ventana_factura_a.show()


def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
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
    conn.commit()
    conn.close()

def insert_initial_data():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM impuestos WHERE id = 1')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO impuestos (id, gasoil_icl, gasoil_idc, diesel_icl, diesel_idc, nafta_super_icl, nafta_super_idc, nafta_euro_icl, nafta_euro_idc)
            VALUES (1, 0, 0, 0, 0, 0, 0, 0, 0)
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