import requests
from bs4 import BeautifulSoup
import urllib3
from datetime import datetime, timedelta

# Desactivar la advertencia de solicitudes inseguras
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Función para obtener los resultados de una semana específica
def obtener_resultados_por_semana(fecha_inicio, fecha_fin):
    # URL de la página con las fechas de la semana
    url = f"https://lotoven.com/animalito/guacharoactivo/historial/{fecha_inicio}/{fecha_fin}/"
    
    # Realizar la solicitud ignorando el certificado SSL
    response = requests.get(url, verify=False)
    response.raise_for_status()  # Verifica que la solicitud fue exitosa
    
    # Analizar el contenido HTML
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Inicializar lista para almacenar los resultados
    resultados = []
    
    # Buscar la tabla con los datos
    tabla = soup.find("table", class_="table")
    if tabla:
        # Extraemos los encabezados de las columnas (fechas)
        encabezados = tabla.find("thead").find_all("th")
        fechas = [encabezado.get_text(strip=True) for encabezado in encabezados[1:]]  # Omite la primera columna que no tiene fecha
        
        # Extraemos las filas de la tabla (horas y resultados)
        filas = tabla.find("tbody").find_all("tr")
        for fila in filas:
            celdas = fila.find_all("td")
            hora = celdas[0].get_text(strip=True)  # La primera columna tiene la hora
            
            # Recorremos las celdas de las fechas
            for idx, celda in enumerate(celdas[1:], start=1):  # Comienza desde 1 para omitir la hora
                numero = celda.get_text(strip=True)
                fecha = fechas[idx-1]  # La fecha corresponde con la posición de la celda
                resultados.append(f"{fecha}, {hora}, {numero}")
    
    return resultados

# Función para generar las fechas de inicio y fin de cada semana de un año
def generar_fechas_semanales(anio):
    fecha_inicio = datetime(anio, 1, 1)
    fecha_inicio = fecha_inicio - timedelta(days=fecha_inicio.weekday())  # Primer lunes del año
    
    while fecha_inicio.year == anio:
        # Calculamos la fecha de fin de la semana (7 días después)
        fecha_fin = fecha_inicio + timedelta(days=6)
        
        # Convertimos las fechas a formato YYYY-MM-DD
        fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
        fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')
        
        # Llamamos a la función para obtener los resultados de la semana
        resultados = obtener_resultados_por_semana(fecha_inicio_str, fecha_fin_str)
        
        # Guardar los resultados en el archivo
        with open(f"resultados_guacharoactivo_{anio}.txt", "a", encoding="utf-8") as archivo:
            for resultado in resultados:
                archivo.write(resultado + "\n")
        
        # Pasamos a la siguiente semana
        fecha_inicio += timedelta(weeks=1)

# Recorrer solo los años 2023 y 2024
for anio in [2023, 2024,2025]:
    generar_fechas_semanales(anio)

print("Datos guardados exitosamente para los años 2023 y 2024!")
