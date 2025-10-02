

import pandas as pd
import joblib
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder

def load_saved_model():

    
    model_path = os.path.join("Semana 7", "Archivos", "random_forest_model.pkl")
    info_path = os.path.join("Semana 7", "Archivos", "model_info.pkl")
    
    
    if os.path.exists(model_path) and os.path.exists(info_path):
        model = joblib.load(model_path)
        model_info = joblib.load(info_path)
        return model, model_info
    else:
        print("No se encontró el modelo guardado.")
        return None, None

def obtener_numero(prompt, min_val=None, max_val=None):
    while True:
        try:
            valor = float(input(prompt))
            if min_val is not None and valor < min_val:
                print(f"El valor debe ser mayor o igual a {min_val}")
                continue
            if max_val is not None and valor > max_val:
                print(f"El valor debe ser menor o igual a {max_val}")
                continue
            return valor
        except ValueError:
            print("Por favor ingresa un número válido")

def obtener_opcion(prompt, opciones):
    print(f"\n{prompt}")
    for i, opcion in enumerate(opciones, 1):
        print(f"  {i}. {opcion}")
    
    while True:
        try:
            seleccion = int(input("Selecciona una opción (número): ")) - 1
            if 0 <= seleccion < len(opciones):
                return opciones[seleccion]
            else:
                print(f"Selecciona un número entre 1 y {len(opciones)}")
        except ValueError:
            print("  Por favor ingresa un número válido")

def recopilar_datos_estudiante():
    
    datos_estudiante = {}
    
    # 1. INFORMACIÓN SOCIOECONÓMICA
    print("\nINFORMACION SOCIOECONOMICA")
    print("-" * 40)
    
    estratos = ["Estrato 1", "Estrato 2", "Estrato 3", "Estrato 4", "Estrato 5", "Estrato 6"]
    datos_estudiante['fami_estratovivienda'] = obtener_opcion(
        "¿Cuál es el estrato socioeconómico de la vivienda?", estratos
    )
    
    situacion_econ = ["Igual", "Mejor", "Peor"]
    datos_estudiante['fami_situacioneconomica'] = obtener_opcion(
        "¿Cómo considera la situación económica familiar comparada con hace un año?", situacion_econ
    )
    
    personas_hogar = ["1 a 2", "3 a 4", "5 a 6", "7 a 8", "9 o más"]
    datos_estudiante['fami_personashogar'] = obtener_opcion(
        "¿Cuántas personas viven en el hogar?", personas_hogar
    )
    
    # 2. EDUCACIÓN DE LOS PADRES
    print("\nEDUCACION DE LOS PADRES")
    print("-" * 40)
    
    niveles_educacion = [
        "Ninguno", "Primaria incompleta", "Primaria completa",
        "Secundaria (Bachillerato) incompleta", "Secundaria (Bachillerato) completa",
        "Técnica o tecnológica incompleta", "Técnica o tecnológica completa",
        "Educación profesional incompleta", "Educación profesional completa",
        "Postgrado", "No sabe"
    ]
    
    datos_estudiante['fami_educacionmadre'] = obtener_opcion(
        "¿Cuál es el nivel educativo de la madre?", niveles_educacion
    )
    
    datos_estudiante['fami_educacionpadre'] = obtener_opcion(
        "¿Cuál es el nivel educativo del padre?", niveles_educacion
    )
    
    # 3. RECURSOS DEL HOGAR
    print("\nRECURSOS DEL HOGAR")
    print("-" * 40)
    
    opciones_si_no = ["Si", "No"]
    datos_estudiante['fami_tienecomputador'] = obtener_opcion(
        "¿La familia tiene computador?", opciones_si_no
    )
    
    datos_estudiante['fami_tieneinternet'] = obtener_opcion(
        "¿La familia tiene internet?", opciones_si_no
    )
    
    datos_estudiante['fami_tieneautomovil'] = obtener_opcion(
        "¿La familia tiene automóvil?", opciones_si_no
    )
    
    num_libros = ["0", "1 a 10", "11 a 25", "26 a 100", "Más de 100"]
    datos_estudiante['fami_numlibros'] = obtener_opcion(
        "¿Aproximadamente cuántos libros hay en casa?", num_libros
    )
    
    # 4. INFORMACIÓN DEL ESTUDIANTE
    print("\nINFORMACION DEL ESTUDIANTE")
    print("-" * 40)
    
    generos = ["F", "M"]
    datos_estudiante['estu_genero'] = obtener_opcion(
        "¿Cuál es el género del estudiante?", generos
    )
    
    horas_trabajo = ["0", "Menos de 10", "Entre 11 y 20", "Entre 21 y 30", "Más de 30"]
    datos_estudiante['estu_horassemanatrabaja'] = obtener_opcion(
        "¿Cuántas horas trabaja el estudiante por semana?", horas_trabajo
    )
    
    dedicacion_internet = ["0", "Entre 1 y 2 horas", "Entre 3 y 5 horas", "Más de 5 horas"]
    datos_estudiante['estu_dedicacioninternet'] = obtener_opcion(
        "¿Cuánto tiempo dedica diariamente a internet?", dedicacion_internet
    )
    
    datos_estudiante['estu_dedicacionlecturadiaria'] = obtener_opcion(
        "¿Cuánto tiempo dedica diariamente a la lectura?", dedicacion_internet
    )
    
    datos_estudiante['estu_repite'] = obtener_opcion(
        "¿El estudiante ha repetido algún año escolar?", opciones_si_no
    )
    
    departamentos = [
        "BOGOTA D.C.",
        "AMAZONAS",
        "ANTIOQUIA",
        "ARAUCA",
        "ATLANTICO",
        "BOLIVAR",
        "BOYACA",
        "CAQUETA",
        "CASANARE",
        "CESAR",
        "CHOCO",
        "CUNDINAMARCA",
        "GUAVIARE",
        "HUILA",
        "LA GUAJIRA",
        "MAGDALENA",
        "META",
        "NARIÑO",
        "NORTE DE SANTANDER",
        "QUINDIO",
        "RISARALDA",
        "SAN ANDRES Y PROVIDENCIA",
        "SANTANDER",
        "TOLIMA",
        "VALLE DEL CAUCA",
        "VAUPES",
        "VICHADA",
    ]
    datos_estudiante['estu_depto_presentacion'] = obtener_opcion(
        "¿En qué departamento presenta la prueba?", departamentos
    )
    
    datos_estudiante['estu_inse_individual'] = obtener_numero(
        "\nIndice INSE individual (0-100, promedio 50): ", 0, 100
    )
    
    datos_estudiante['estu_nse_individual'] = obtener_numero(
        "Indice NSE individual (0-100, promedio 50): ", 0, 100
    )
    
    # 5. INFORMACIÓN DEL COLEGIO
    print("\nINFORMACION DEL COLEGIO")
    print("-" * 40)
    
    areas = ["Urbano", "Rural"]
    datos_estudiante['cole_area_ubicacion'] = obtener_opcion(
        "¿El colegio está ubicado en zona rural o urbana?", areas
    )
    
    naturalezas = ["Privado", "Publico"]
    datos_estudiante['cole_naturaleza'] = obtener_opcion(
        "¿Cuál es la naturaleza del colegio?", naturalezas
    )
    
    caracteres = ["ACADÉMICO", "NO APLICA", "TÉCNICO", "TÉCNICO/ACADÉMICO"]
    datos_estudiante['cole_caracter'] = obtener_opcion(
        "¿Cuál es el carácter del colegio?", caracteres
    )
    
    jornadas = ["COMPLETA", "MAÑANA", "NOCHE", "SABATINA", "TARDE", "UNICA"]
    datos_estudiante['cole_jornada'] = obtener_opcion(
        "¿Cuál es la jornada del colegio?", jornadas
    )
    
    calendarios = ["A", "B", "OTRO"]
    datos_estudiante['cole_calendario'] = obtener_opcion(
        "¿Qué tipo de calendario maneja el colegio?", calendarios
    )
    
    datos_estudiante['cole_bilingue'] = obtener_opcion(
        "¿El colegio es bilingüe?", opciones_si_no
    )
    
    return datos_estudiante

def procesar_datos_para_modelo(datos_estudiante, feature_names):
    """
    Procesa los datos del estudiante para que coincidan con el formato del modelo
    """
    # Crear DataFrame
    df_input = pd.DataFrame([datos_estudiante])
    
    # 1. Mapear personas en hogar a números
    mapa_personashogar = {
        "Sin dato": 0, "1 a 2": 1, "3 a 4": 2, 
        "5 a 6": 3, "7 a 8": 4, "9 o más": 5
    }
    df_input["fami_personashogar"] = df_input["fami_personashogar"].map(mapa_personashogar).fillna(0)
    
    # 2. Variables para Label Encoding
    label_vars = [
        'fami_estratovivienda', 'fami_educacionmadre', 'fami_educacionpadre',
        'fami_numlibros', 'estu_dedicacioninternet', 'estu_dedicacionlecturadiaria',
        'estu_depto_presentacion', 'cole_bilingue', 'estu_horassemanatrabaja', 'estu_repite'
    ]
    
    # Aplicar label encoding
    for col in label_vars:
        if col in df_input.columns:
            le = LabelEncoder()
            df_input[col] = le.fit_transform(df_input[col].astype(str))
    
    # 3. Variables para One-Hot Encoding
    onehot_vars = [
        'fami_tienecomputador', 'fami_tieneinternet', 'fami_tieneautomovil',
        'fami_situacioneconomica', 'estu_genero', 'cole_area_ubicacion',
        'cole_naturaleza', 'cole_caracter', 'cole_jornada', 'cole_calendario'
    ]
    
    # Aplicar one-hot encoding
    df_input = pd.get_dummies(df_input, columns=onehot_vars, drop_first=True)
    
    # 4. Asegurar que todas las columnas del modelo estén presentes
    for col in feature_names:
        if col not in df_input.columns:
            df_input[col] = 0
    
    # 5. Reordenar columnas en el mismo orden que el entrenamiento
    df_input = df_input.reindex(columns=feature_names, fill_value=0)
    
    return df_input

def mostrar_resultados(puntaje_predicho, model_info):
    """
    Muestra los resultados de la predicción
    """
    print("\n" + "="*60)
    print("RESULTADO DE LA PREDICCION")
    print("="*60)
    print(f"PUNTAJE PREDICHO: {puntaje_predicho:.2f} puntos")
    print("="*60)

def predictor_icfes_exacto():
 
    print("Predecir puntaje ICFES")
    
    
    # Cargar modelo
    loaded_model, loaded_info = load_saved_model()
    if loaded_model is None:
        return
    
    try:
        # Recopilar datos del estudiante
        datos_estudiante = recopilar_datos_estudiante()
        
        # Procesar datos para el modelo
        df_input = procesar_datos_para_modelo(datos_estudiante, loaded_info['feature_names'])
        
        # Hacer predicción exacta con el modelo
        puntaje_predicho = loaded_model.predict(df_input)[0]
        
        # Mostrar resultados
        mostrar_resultados(puntaje_predicho, loaded_info)
        
    except Exception as e:
        print(f"\nError al procesar la predicción: {e}")
        print("Verifica que todos los datos estén correctos.")

def main():
    """
    Función principal con manejo de errores y opción de repetir
    """
    while True:
        try:
            predictor_icfes_exacto()
            
            print(f"\n¿Deseas hacer otra predicción? (s/n): ", end="")
            respuesta = input().lower().strip()
            
            if respuesta not in ['s', 'si']:
                break
                
        except KeyboardInterrupt:
            print(f"\n Predicción cancelada por el usuario.")
            break
        except Exception as e:
            print(f"\n Error inesperado: {e}")
            print("Intenta nuevamente.")

if __name__ == "__main__":
    print("Predecir puntaje ICFES")
    print("="*50)
    
    main()
