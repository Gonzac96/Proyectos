"""
Debe pedir el precio final del surtidor. Con esto hace el siguiente calculo
Precio final - ICL - IDC
El resultado de esta diferencia la divido por 1.21 (IVA) y la redondeo en 2 decimales

Es decir: [(PF-ICL-IDC)/1.21]round,2

Esto nos da el precio del producto que buscamos para una Factura A(2 decimales), 
y luego multiplicamos ese valor por 0.21 y sumamos ambos resultados para obtener el precio de Factura B(redondeo 3 decimales)

"""


#PRODUCTO ---> hasta 2 decimales
gas_oil_g2 = 0.00
gas_oil_g3 = 0.00
nafta_super = 0.00
nafta_euro = 0.00

#ICL e IDC ---> ya cargados en la pestaña de impuestos. Hasta 5 decimales

#IVA 21% ---> el precio del producto x 0.21 (redondea con 2 decimales)

