from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sqlite3

# Base de datos
DATABASE = 'impuestos.db'

# Inicializar la base de datos
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS impuestos (
            id INTEGER PRIMARY KEY,
            valor1 REAL,
            valor2 REAL
        )
    ''')
    conn.commit()
    conn.close()

# Defino la ventana de combustibles, donde se cargaran los precios y se realizarán las operaciones correspondientes
class VentanaCombustible(QWidget):
    def __init__(self):         
        super().__init__()
        self.initUI()
    
    # Inicializa la interfaz de usuario en el método "initUI" | UI = User Interface
    def initUI(self):
        self.setWindowTitle("Combustible")
        self.setGeometry(300, 300, 500, 300)

        layout = QVBoxLayout()

        # Mostrar valores de impuestos
        self.label_impuestos = QLabel("Valores de Impuestos")
        layout.addWidget(self.label_impuestos)
        
        self.label_valor1 = QLabel("ICL: ")
        layout.addWidget(self.label_valor1)
        
        self.label_valor2 = QLabel("IDC: ")
        layout.addWidget(self.label_valor2)

        # Campos para cargar datos de combustibles
        self.label_gasoil = QLabel("Gas Oil: ")
        self.gasoil_double_spin_box = QDoubleSpinBox(self)
        self.gasoil_double_spin_box.setRange(0, 100000)
        self.gasoil_double_spin_box.setDecimals(2)

        self.label_diesel = QLabel("Diesel Euro: ")
        self.diesel_double_spin_box = QDoubleSpinBox(self)
        self.diesel_double_spin_box.setRange(0, 100000)
        self.diesel_double_spin_box.setDecimals(2)

        self.label_nafta_super = QLabel("Nafta Super: ")
        self.nafta_super_double_spin_box = QDoubleSpinBox(self)
        self.nafta_super_double_spin_box.setRange(0, 100000)
        self.nafta_super_double_spin_box.setDecimals(2)

        self.label_nafta_euro = QLabel("Nafta Euro: ")
        self.nafta_euro_double_spin_box = QDoubleSpinBox(self)
        self.nafta_euro_double_spin_box.setRange(0, 100000)
        self.nafta_euro_double_spin_box.setDecimals(2)

        layout.addWidget(self.label_gasoil)
        layout.addWidget(self.gasoil_double_spin_box)
        layout.addWidget(self.label_diesel)
        layout.addWidget(self.diesel_double_spin_box)
        layout.addWidget(self.label_nafta_super)
        layout.addWidget(self.nafta_super_double_spin_box)
        layout.addWidget(self.label_nafta_euro)
        layout.addWidget(self.nafta_euro_double_spin_box)

        self.boton_factura_A = QPushButton('Factura A', self)
        self.boton_factura_A.clicked.connect(self.calcular_factura_A)
        self.boton_factura_A.setFixedSize(200, 50)
        
        self.boton_factura_B = QPushButton('Factura B', self)
        self.boton_factura_B.clicked.connect(self.calcular_factura_B)
        self.boton_factura_B.setFixedSize(200, 50)
        
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.boton_factura_A)
        hbox1.addStretch(1)
        
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.boton_factura_B)
        hbox2.addStretch(1)

        layout.addLayout(hbox1)
        layout.addLayout(hbox2)

        self.setLayout(layout)
        self.cargar_valores_impuestos()

    def cargar_valores_impuestos(self):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT valor1, valor2 FROM impuestos')
        row = c.fetchone()
        conn.close()
        
        if row:
            self.label_valor1.setText(f'Valor 1: {row[0]}')
            self.label_valor2.setText(f'Valor 2: {row[1]}')
            self.valor1 = row[0]
            self.valor2 = row[1]
        else:
            self.label_valor1.setText('Valor 1: No disponible')
            self.label_valor2.setText('Valor 2: No disponible')
            self.valor1 = 0
            self.valor2 = 0

    def calcular_factura_A(self):
        try:
            gasoil = self.gasoil_double_spin_box.value()
            diesel = self.diesel_double_spin_box.value()
            nafta_super = self.nafta_super_double_spin_box.value()
            nafta_euro = self.nafta_euro_double_spin_box.value()

            resultado_gasoil = round((gasoil - self.valor1 - self.valor2) / 1.21, 2)
            resultado_diesel = round((diesel - self.valor1 - self.valor2) / 1.21, 2)
            resultado_nafta_super = round((nafta_super - self.valor1 - self.valor2) / 1.21, 2)
            resultado_nafta_euro = round((nafta_euro - self.valor1 - self.valor2) / 1.21, 2)

            QMessageBox.information(self, 'Resultado Facturita', f'Gas Oil: {resultado_gasoil}\nDiesel Euro: {resultado_diesel}\nNafta Super: {resultado_nafta_super}\nNafta Euro: {resultado_nafta_euro}')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Ocurrió un error: {e}')

    def calcular_factura_B(self):
        try:
            gasoil = self.gasoil_double_spin_box.value()
            diesel = self.diesel_double_spin_box.value()
            nafta_super = self.nafta_super_double_spin_box.value()
            nafta_euro = self.nafta_euro_double_spin_box.value()

            resultado_gasoil = round((gasoil - self.valor1 - self.valor2) / 1.21, 2)
            resultado_diesel = round((diesel - self.valor1 - self.valor2) / 1.21, 2)
            resultado_nafta_super = round((nafta_super - self.valor1 - self.valor2) / 1.21, 2)
            resultado_nafta_euro = round((nafta_euro - self.valor1 - self.valor2) / 1.21, 2)

            resultado_b_gasoil = round(resultado_gasoil * 0.21 + resultado_gasoil, 2)
            resultado_b_diesel = round(resultado_diesel * 0.21 + resultado_diesel, 2)
            resultado_b_nafta_super = round(resultado_nafta_super * 0.21 + resultado_nafta_super, 2)
            resultado_b_nafta_euro = round(resultado_nafta_euro * 0.21 + resultado_nafta_euro, 2)

            QMessageBox.information(self, 'Resultado Factura B', f'Gas Oil: {resultado_b_gasoil}\nDiesel Euro: {resultado_b_diesel}\nNafta Super: {resultado_b_nafta_super}\nNafta Euro: {resultado_b_nafta_euro}')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Ocurrió un error: {e}')




# Defino la ventana de impuestos, donde se cargaran los valores de los impuestos
class VentanaImpuestos(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.cargar_valores()

    def initUI(self):
        self.setWindowTitle("Valor de Impuestos")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        self.label1 = QLabel("Impuesto a los Combustibles Líquidos(ICL):")
        self.double_spin_box1 = QDoubleSpinBox(self)
        self.double_spin_box1.setPrefix("$")
        self.double_spin_box1.setRange(-1,100000)
        self.double_spin_box1.setDecimals(5)

        self.label2 = QLabel("Impuesto al Dióxido de Carbono(IDC):")
        self.double_spin_box2 = QDoubleSpinBox(self)
        self.double_spin_box2.setPrefix("$")
        self.double_spin_box2.setRange(-1,100000)
        self.double_spin_box2.setDecimals(5)

        self.boton_guardar = QPushButton("Guardar", self)
        self.boton_guardar.clicked.connect(self.guardar_valores)

        layout.addWidget(self.label1)
        layout.addWidget(self.double_spin_box1)
        layout.addWidget(self.label2)
        layout.addWidget(self.double_spin_box2)
        layout.addWidget(self.boton_guardar)

        self.setLayout(layout)

    def guardar_valores(self):
        valor1 = self.double_spin_box1.value()
        valor2 = self.double_spin_box2.value()
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('DELETE FROM impuestos')  # Borrar valores anteriores
        c.execute('INSERT INTO impuestos (valor1, valor2) VALUES (?, ?)', (valor1, valor2))
        conn.commit()
        conn.close()
        
        QMessageBox.information(self, 'Guardado', 'Los valores han sido guardados.')

    def cargar_valores(self):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT valor1, valor2 FROM impuestos')
        row = c.fetchone()
        conn.close()
        
        if row:
            self.double_spin_box1.setValue(row[0])
            self.double_spin_box2.setValue(row[1])
        else:
            self.double_spin_box1.setValue(-1)
            self.double_spin_box2.setValue(-1)


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Gestión de Facturas e Impuestos")  #Titulo de la ventana
        self.setGeometry(200, 200, 350, 250)    #Defino los pixeles en "x" e "y" donde aparecerá la ventana, y su tamaño

        layout = QVBoxLayout()  # Organiza los botones verticalmente


        self.boton_combustible = QPushButton("Cálculo Combustible", self)   # Instancia un botón para los combustibles
        self.boton_combustible.clicked.connect(self.abrir_ventana_combustible)  # Conecta el botón con el método creado abrir_ventana_combustible
        self.boton_combustible.setFixedSize(150, 30)    # Tamaño del botón


        self.boton_impuestos = QPushButton("Impuestos", self)   # Instancia un botón para los impuestos
        self.boton_impuestos.clicked.connect(self.abrir_ventana_impuestos)  # Conecta el botón con el método creado abrir_ventana_impuestos
        self.boton_impuestos.setFixedSize(150, 30)  # Tamaño del botón

        # Centrar los botones en la ventana principal
        for boton in [self.boton_combustible, self.boton_impuestos]:    
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(boton)
            hbox.addStretch(1)
            layout.addLayout(hbox)

        self.setLayout(layout)


    def abrir_ventana_combustible(self):
        self.ventana_factura_a = VentanaCombustible()
        self.ventana_factura_a.show()

    def abrir_ventana_impuestos(self):
        self.ventana_impuestos = VentanaImpuestos()
        self.ventana_impuestos.show()

if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec_()
