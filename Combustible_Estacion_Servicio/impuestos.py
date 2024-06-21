import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QClipboard

# Base de datos
DATABASE = 'impuestos.db'

# Inicializar la base de datos
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        DROP TABLE IF EXISTS impuestos
    ''')
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

class VentanaImpuestos(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.cargar_valores()

    def initUI(self):
        self.setWindowTitle('Gestión de Impuestos')
        self.setGeometry(150, 150, 400, 400)

        layout = QVBoxLayout()

        # Crear etiquetas y spin boxes para cada valor
        self.labels = {}
        self.spin_boxes = {}
        impuestos = ['gasoil', 'diesel', 'nafta_super', 'nafta_euro']
        tipos = ['icl', 'idc']

        for impuesto in impuestos:
            hbox = QHBoxLayout()
            for tipo in tipos:
                label = QLabel(f'{impuesto.capitalize().replace("_", " ")} {tipo.upper()}:')
                spin_box = QDoubleSpinBox(self)
                spin_box.setRange(0, 100000)
                spin_box.setDecimals(2)

                self.labels[f'{impuesto}_{tipo}'] = label
                self.spin_boxes[f'{impuesto}_{tipo}'] = spin_box

                hbox.addWidget(label)
                hbox.addWidget(spin_box)
            layout.addLayout(hbox)

        self.boton_guardar = QPushButton('Guardar', self)
        self.boton_guardar.clicked.connect(self.guardar_valores)
        self.boton_guardar.setFixedSize(150, 50)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.boton_guardar)
        hbox.addStretch(1)
        layout.addLayout(hbox)

        self.setLayout(layout)

    def guardar_valores(self):
        valores = {key: spin_box.value() for key, spin_box in self.spin_boxes.items()}
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('DELETE FROM impuestos')  # Borrar valores anteriores
        c.execute('''
            INSERT INTO impuestos (gasoil_icl, gasoil_idc, diesel_icl, diesel_idc, nafta_super_icl, nafta_super_idc, nafta_euro_icl, nafta_euro_idc)
            VALUES (:gasoil_icl, :gasoil_idc, :diesel_icl, :diesel_idc, :nafta_super_icl, :nafta_super_idc, :nafta_euro_icl, :nafta_euro_idc)
        ''', valores)
        conn.commit()
        conn.close()
        
        QMessageBox.information(self, 'Guardado', 'Los valores han sido guardados.')

    def cargar_valores(self):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT gasoil_icl, gasoil_idc, diesel_icl, diesel_idc, nafta_super_icl, nafta_super_idc, nafta_euro_icl, nafta_euro_idc FROM impuestos')
        row = c.fetchone()
        conn.close()
        
        if row:
            for i, key in enumerate(self.spin_boxes.keys()):
                self.spin_boxes[key].setValue(row[i])
        else:
            for spin_box in self.spin_boxes.values():
                spin_box.setValue(0)

class VentanaFacturaA(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Factura A')
        self.setGeometry(200, 200, 500, 350)

        layout = QVBoxLayout()

        # Mostrar valores de impuestos
        self.label_impuestos = QLabel('Valores de Impuestos:')
        layout.addWidget(self.label_impuestos)
        
        self.labels_impuestos = {}
        impuestos = ['gasoil', 'diesel', 'nafta_super', 'nafta_euro']
        tipos = ['icl', 'idc']
        
        grid_impuestos = QGridLayout()
        row = 0
        for impuesto in impuestos:
            for col, tipo in enumerate(tipos):
                label = QLabel(f'{impuesto.capitalize().replace("_", " ")} {tipo.upper()}:')
                self.labels_impuestos[f'{impuesto}_{tipo}'] = label
                grid_impuestos.addWidget(label, row, col)
            row += 1
        
        layout.addLayout(grid_impuestos)

        # Campos para nuevos valores
        self.labels = {}
        self.spin_boxes = {}
        
        grid_valores = QGridLayout()
        row = 0
        for impuesto in impuestos:
            label = QLabel(f'{impuesto.capitalize().replace("_", " ")}:')
            spin_box = QDoubleSpinBox(self)
            spin_box.setRange(0, 100000)
            spin_box.setDecimals(2)
            
            self.labels[impuesto] = label
            self.spin_boxes[impuesto] = spin_box

            grid_valores.addWidget(label, row, 0)
            grid_valores.addWidget(spin_box, row, 1)
            row += 1

        layout.addLayout(grid_valores)

        # Añadir los botones al layout
        self.boton_facturita = QPushButton('Facturita', self)
        self.boton_facturita.clicked.connect(self.calcular_facturita)
        self.boton_facturita.setFixedSize(200, 50)

        self.boton_factura_b = QPushButton('Factura B', self)
        self.boton_factura_b.clicked.connect(self.calcular_factura_b)
        self.boton_factura_b.setFixedSize(200, 50)

        # Crear un QHBoxLayout para los botones
        hbox_botones = QHBoxLayout()
        hbox_botones.addWidget(self.boton_facturita)
        hbox_botones.addStretch(1)
        hbox_botones.addWidget(self.boton_factura_b)

        # Añadir el QHBoxLayout de los botones al layout principal
        layout.addLayout(hbox_botones)

        self.setLayout(layout)

        self.cargar_valores_impuestos()

    def cargar_valores_impuestos(self):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT gasoil_icl, gasoil_idc, diesel_icl, diesel_idc, nafta_super_icl, nafta_super_idc, nafta_euro_icl, nafta_euro_idc FROM impuestos')
        row = c.fetchone()
        conn.close()
        
        if row:
            for i, key in enumerate(self.labels_impuestos.keys()):
                self.labels_impuestos[key].setText(f'{key.capitalize().replace("_", " ")}: {row[i]}')
                setattr(self, key, row[i])
        else:
            for label in self.labels_impuestos.values():
                label.setText('No disponible')
            for key in self.labels_impuestos.keys():
                setattr(self, key, 0)

    def calcular_facturita(self):
        try:
            resultados = {}
            for key in self.spin_boxes.keys():
                valor = self.spin_boxes[key].value()
                icl = getattr(self, f'{key}_icl')
                idc = getattr(self, f'{key}_idc')
                resultado = round((valor - icl - idc) / 1.21, 2)
                resultados[key] = resultado

            resultados_texto = '\n'.join([f'{key.capitalize().replace("_", " ")}: {result}' for key, result in resultados.items()])
            QMessageBox.information(self, 'Resultado Facturita', resultados_texto)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Ocurrió un error: {e}')

    def calcular_factura_b(self):
        try:
            resultados = {}
            resultados_finales = {}
            for key in self.spin_boxes.keys():
                valor = self.spin_boxes[key].value()
                icl = getattr(self, f'{key}_icl')
                idc = getattr(self, f'{key}_idc')
                resultado = round((valor - icl - idc) / 1.21, 2)
                resultado_final = round(resultado * 0.21 + resultado, 2)
                resultados[key] = resultado
                resultados_finales[key] = resultado_final

            resultados_texto = '\n'.join([f'{key.capitalize().replace("_", " ")}: {resultados[key]} (Final: {resultados_finales[key]})' for key in resultados.keys()])
            QMessageBox.information(self, 'Resultado Factura B', resultados_texto)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Ocurrió un error: {e}')

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gestión de Facturas e Impuestos')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.boton_factura_a = QPushButton('Factura A', self)
        self.boton_factura_a.clicked.connect(self.abrir_ventana_factura_a)
        self.boton_factura_a.setFixedSize(200, 50)

        self.boton_impuestos = QPushButton('Impuestos', self)
        self.boton_impuestos.clicked.connect(self.abrir_ventana_impuestos)
        self.boton_impuestos.setFixedSize(200, 50)

        for boton in [self.boton_factura_a, self.boton_impuestos]:
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(boton)
            hbox.addStretch(1)
            layout.addLayout(hbox)

        self.setLayout(layout)

    def abrir_ventana_factura_a(self):
        self.ventana_factura_a = VentanaFacturaA()
        self.ventana_factura_a.show()

    def abrir_ventana_impuestos(self):
        self.ventana_impuestos = VentanaImpuestos()
        self.ventana_impuestos.show()

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
