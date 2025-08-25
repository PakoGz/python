from datetime import datetime
import csv

# --- Leer CSV ---
def leer_csv(path_csv):
    with open(path_csv, newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)

# --- Parsear línea de TXT ---
def parsear_linea_txt(linea):
    return {
        "ente": linea[0:3].strip(),
        "denominacion": linea[3:23].strip(),
        "tipo_adherido": linea[23].strip(),
        "cantidad": int(linea[23:29]),
        "bruto": int(linea[29:47]),
        "signo_ajuste": linea[47],
        "ajuste": int(linea[48:64]),
        "adherido": linea[64],
        "comision_emisor": int(linea[65:81]),
        "signo_comision_adherente": linea[81],
        "comision_adherente": int(linea[82:98]),
        "iva_comision_emisor": int(linea[98:114]),
        "signo_iva_comision_adherente": linea[114],
        "iva_comision_adherente": int(linea[115:131]),
        "percepcion": int(linea[131:147]),
        "retencion_iva": int(linea[147:163]),
        "retencion_ganancias": int(linea[163:179]),
        "retencion_iibb": int(linea[179:195]),
        "signo_neto": linea[195],
        "neto": int(linea[196:214])
    }

# --- Generar líneas de salida ---
def generar_lineas_salida(registro_txt, registro_csv):
    lineas = []

    # Conceptos a emitir con su valor y signo
    conceptos = [
        ("BRUTO", registro_txt["bruto"], "+"),
        ("AJUSTE", registro_txt["ajuste"], registro_txt["signo_ajuste"]),
        ("COMISION_EMISOR", registro_txt["comision_emisor"], "-"),
        ("IVA_COMISION_EMISOR", registro_txt["iva_comision_emisor"], "-"),
        ("COMISION_ADHERENTE", registro_txt["comision_adherente"], registro_txt["signo_comision_adherente"]),
        ("IVA_COMISION_ADHERENTE", registro_txt["iva_comision_adherente"], registro_txt["signo_iva_comision_adherente"]),
        ("PERCEPCION", registro_txt["percepcion"], "+"),
        ("RETENCION_IVA", registro_txt["retencion_iva"], "-"),
        ("RETENCION_GANANCIAS", registro_txt["retencion_ganancias"], "-"),
        ("RETENCION_IIBB", registro_txt["retencion_iibb"], "-"),
        ("NETO", registro_txt["neto"], registro_txt["signo_neto"])
    ]

    # Implementando formato de la salida
    for concepto, valor, signo in conceptos:
        if valor != 0:
            linea = (
                f"{registro_txt['ente'].zfill(3)}"                         # 01–03
                f"{registro_txt['denominacion']:<20}"                      # 04–23
                f"{registro_txt['tipo_adherido']}"                          # 24
                f"{registro_csv['sucursal'].zfill(3)}"                     # 25–27
                f"{registro_csv['cuenta'].zfill(11)}"                      # 28–38
                f"{concepto:<20}"                                          # 39–58
                f"{signo}"                                                  # 59
                f"{str(valor).zfill(16)}"                                   # 60–75
            )
            lineas.append(linea)
    return lineas

def main():
    fecha = datetime.now().strftime("%m%d")
    nombre_salida = f"OUTPUT{fecha}.txt"

    entes_csv = leer_csv("convenios.csv")
    datos_salida = []

    with open("INPUT0822.txt", "r", encoding="utf-8") as f:
        for linea in f:
            registro_txt = parsear_linea_txt(linea)

            # Buscar coincidencia en CSV
            for registro_csv in entes_csv:
                if registro_csv["ente_id"].strip() == registro_txt["ente"]:
                    lineas = generar_lineas_salida(registro_txt, registro_csv)
                    datos_salida.extend(lineas)
          

    # Guardar archivo de salida
    with open(nombre_salida, "w", encoding="utf-8") as out:
        for linea in datos_salida:
            out.write(linea + "\n")

main()
