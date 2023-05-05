import pandas as pd
# import matplotlib.pyplot as plt
import sys

def main(argv):
    direccion = str(argv[1])
    CSV = leer_csv(direccion)
    print("Contenido\n", CSV)

def leer_csv(direccion):
    datos = pd.read_csv(direccion, encoding= 'unicode_escape')
    return datos

main(sys.argv)