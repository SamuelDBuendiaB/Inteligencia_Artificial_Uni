import requests
from bs4 import BeautifulSoup
import urllib3
from datetime import datetime, timedelta
import os

# Desactivar la advertencia de solicitudes inseguras
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Función para obtener los resultados existentes de un archivo (para evitar duplicados)
def obtener_resultados_existentes(nombre_archivo):
    """
    Lee todos los resultados existentes del archivo y los retorna como un set
    para verificar duplicados rápidamente
    """
    resultados_existentes = set()
    try:
        if os.path.exists(nombre_archivo):
            with open(nombre_archivo, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea:
                        resultados_existentes.add(linea)
    except Exception as e:
        print(f"  Advertencia: Error al leer archivo existente: {e}")
    
    return resultados_existentes

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

# Función para encontrar la última fecha procesada por año en un archivo
def encontrar_ultima_fecha_por_anio(nombre_archivo, anio):
    """
    Busca la última fecha de un año específico en el archivo de resultados
    """
    try:
        if not os.path.exists(nombre_archivo):
            return None
        
        ultima_fecha = None
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            
            # Buscar la última fecha válida del año desde el final
            for linea in reversed(lineas):
                if linea.strip():
                    partes = linea.strip().split(",")
                    if len(partes) >= 3:
                        fecha_str = partes[0].strip()
                        try:
                            fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")
                            if fecha_dt.year == anio:
                                ultima_fecha = fecha_dt
                                break
                        except:
                            continue
        
        return ultima_fecha
    except Exception as e:
        print(f"  Error al leer archivo {nombre_archivo}: {e}")
        return None

# Función para generar las fechas de inicio y fin de cada semana de un año
def generar_fechas_semanales(anio, nombre_archivo_unico, resultados_existentes, continuar_desde=None):
    fecha_actual = datetime.now()
    es_anio_actual = anio == fecha_actual.year
    
    # Determinar desde dónde empezar
    if continuar_desde is not None:
        # Si se especifica una fecha, usar esa
        fecha_inicio_base = continuar_desde
        print(f"  Continuando desde fecha especificada: {fecha_inicio_base.strftime('%Y-%m-%d')}")
    else:
        # Intentar encontrar la última fecha procesada del año específico
        ultima_fecha = encontrar_ultima_fecha_por_anio(nombre_archivo_unico, anio)
        if ultima_fecha:
            # Continuar desde el día siguiente a la última fecha procesada
            fecha_inicio_base = ultima_fecha + timedelta(days=1)
            print(f"  Última fecha encontrada en archivo: {ultima_fecha.strftime('%Y-%m-%d')}")
            print(f"  Continuando desde: {fecha_inicio_base.strftime('%Y-%m-%d')}")
        else:
            # Si no hay archivo, empezar desde el primer lunes del año
            fecha_inicio_base = datetime(anio, 1, 1)
            fecha_inicio_base = fecha_inicio_base - timedelta(days=fecha_inicio_base.weekday())
            print(f"  Iniciando desde el comienzo del año: {fecha_inicio_base.strftime('%Y-%m-%d')}")
    
    # Asegurarse de empezar en un lunes (ajustar al lunes anterior o siguiente)
    dias_hasta_lunes = fecha_inicio_base.weekday()
    fecha_inicio = fecha_inicio_base - timedelta(days=dias_hasta_lunes)
    
    # Si no es el año actual, podemos ir hasta el último día del año
    if not es_anio_actual:
        fecha_limite = datetime(anio, 12, 31)
    else:
        # Si es el año actual, usar la fecha de hoy como límite
        fecha_limite = fecha_actual
    
    # Continuar mientras el inicio de la semana esté dentro del año o antes de la fecha límite
    while True:
        # Calcular fin de semana
        fecha_fin_semana = fecha_inicio + timedelta(days=6)
        
        # Si el inicio de la semana es después del límite, detener
        if fecha_inicio.date() > fecha_limite.date():
            print(f"  Llegado al límite. Deteniendo (inicio semana: {fecha_inicio.strftime('%Y-%m-%d')}, límite: {fecha_limite.strftime('%Y-%m-%d')})")
            break
        
        # Si el fin de semana sobrepasa la fecha límite, ajustar
        if fecha_fin_semana.date() > fecha_limite.date():
            fecha_fin = fecha_limite
        else:
            fecha_fin = fecha_fin_semana
        
        # Convertimos las fechas a formato YYYY-MM-DD
        fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
        fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')
        
        print(f"  Procesando semana: {fecha_inicio_str} a {fecha_fin_str}")
        
        try:
            # Llamamos a la función para obtener los resultados de la semana
            resultados = obtener_resultados_por_semana(fecha_inicio_str, fecha_fin_str)
            
            if resultados:
                # Filtrar resultados para guardar solo los del año correspondiente y evitar duplicados
                resultados_nuevos = []
                resultados_filtrados = []
                
                for resultado in resultados:
                    resultado_limpio = resultado.strip()
                    # Verificar si ya existe
                    if resultado_limpio in resultados_existentes:
                        continue  # Saltar duplicados
                    
                    partes = resultado_limpio.split(",")
                    if len(partes) >= 3:
                        fecha_resultado = partes[0].strip()
                        try:
                            fecha_dt = datetime.strptime(fecha_resultado, "%Y-%m-%d")
                            # Solo guardar si pertenece al año que estamos procesando
                            if fecha_dt.year == anio or (anio == fecha_actual.year and fecha_dt.date() <= fecha_actual.date()):
                                resultados_filtrados.append(resultado_limpio)
                                resultados_nuevos.append(resultado_limpio)
                        except:
                            # Si no se puede parsear la fecha, guardarlo de todas formas (solo si no existe)
                            if resultado_limpio not in resultados_existentes:
                                resultados_filtrados.append(resultado_limpio)
                                resultados_nuevos.append(resultado_limpio)
                
                # Guardar solo los resultados nuevos (sin duplicados)
                if resultados_nuevos:
                    with open(nombre_archivo_unico, "a", encoding="utf-8") as archivo:
                        for resultado in resultados_nuevos:
                            archivo.write(resultado + "\n")
                    # Actualizar el set de existentes para siguientes iteraciones
                    resultados_existentes.update(resultados_nuevos)
                    print(f"    ✓ {len(resultados_nuevos)} resultados NUEVOS guardados (de {len(resultados)} obtenidos, {len(resultados) - len(resultados_nuevos)} duplicados omitidos)")
                else:
                    print(f"    ⚠ {len(resultados)} resultados obtenidos pero todos ya existen o no pertenecen a {anio}")
            else:
                print(f"    ⚠ No se obtuvieron resultados para esta semana")
        except Exception as e:
            print(f"    ✗ Error al obtener datos de la semana: {e}")
            import traceback
            traceback.print_exc()
            # Continuar con la siguiente semana aunque haya error
        
        # Pasamos a la siguiente semana ANTES de verificar el límite
        fecha_inicio += timedelta(weeks=1)
        
        # Si es el año actual y la siguiente semana ya pasó la fecha actual, detener
        if es_anio_actual and fecha_inicio.date() > fecha_actual.date():
            print(f"  Llegado a fecha actual. Última semana procesada termina en {fecha_fin_str}")
            break

# Recorrer los años especificados (2023, 2024, 2025)
# Nota: Para 2025, solo se obtendrán los datos disponibles hasta la fecha actual
anios = [2023, 2024, 2025]
fecha_actual = datetime.now()

# Obtener la ruta del directorio donde está este script
script_dir = os.path.dirname(os.path.abspath(__file__))
nombre_archivo_unico = os.path.join(script_dir, "resultados_guacharoactivo_completo.txt")

print(f"Iniciando scraping para los años: {anios}")
print(f"Fecha actual: {fecha_actual.strftime('%Y-%m-%d')}")
print(f"Archivo de salida único: {nombre_archivo_unico}")
print(f"\n{'='*60}")

# Cargar todos los resultados existentes una sola vez al inicio
print(f"Cargando resultados existentes de {nombre_archivo_unico}...")
resultados_existentes = obtener_resultados_existentes(nombre_archivo_unico)
print(f"Resultados existentes: {len(resultados_existentes)}")
print(f"{'='*60}\n")

for anio in anios:
    # Si el año es futuro, saltarlo
    if anio > fecha_actual.year:
        print(f"Saltando año {anio} (año futuro)")
        continue
    
    print(f"\n{'='*60}")
    print(f"Procesando año {anio}...")
    print(f"{'='*60}")
    
    try:
        # Intentar continuar desde donde se quedó
        generar_fechas_semanales(anio, nombre_archivo_unico, resultados_existentes)
        print(f"\n✓ Datos del año {anio} procesados exitosamente")
    except KeyboardInterrupt:
        print(f"\n⚠ Proceso interrumpido por el usuario")
        break
    except Exception as e:
        print(f"\n✗ Error al procesar año {anio}: {e}")
        import traceback
        traceback.print_exc()
        continue

