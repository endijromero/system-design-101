# -*- coding: utf-8 -*-

"""
Script para procesar imágenes desde una carpeta local utilizando la API de IA de Gemini.

Este script realiza las siguientes acciones:
1. Lee archivos de imagen (.png) de una carpeta de entrada especificada.
2. Para cada imagen, envía una solicitud a la API de Gemini para que la analice.
3. El prompt solicita a Gemini una investigación profunda sobre los conceptos de la imagen.
4. La respuesta generada se guarda en un archivo de texto con un encabezado informativo.
5. El nombre del archivo de salida se compone del nombre de la imagen original más una marca de tiempo.
"""

import os
import pathlib
import time
from datetime import datetime
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN DE RUTAS ---
# 1. Modifica esta variable con la ruta a la carpeta que contiene tus imágenes PNG.
#    Ejemplo en Windows: "C:\\Users\\TuUsuario\\Desktop\\Imagenes"
#    Ejemplo en macOS/Linux: "/home/TuUsuario/Documentos/Imagenes"
ruta_carpeta_imagenes = "/home/debianuser/Documentos/proyectos/python/system-design-101/data/images"


# 2. Modifica esta variable con la ruta a la carpeta donde se guardarán las respuestas.
#    Ejemplo en Windows: "C:\\Users\\TuUsuario\\Desktop\\Respuestas"
#    Ejemplo en macOS/Linux: "/home/TuUsuario/Documentos/Respuestas"
ruta_carpeta_salida = "/home/debianuser/Documentos/proyectos/python/system-design-101/data/images"

# --- CONFIGURACIÓN DE LA API DE GEMINI ---
try:
    # Intenta obtener la API Key de las variables de entorno del sistema.
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("La variable de entorno GOOGLE_API_KEY no está configurada.")
    
    genai.configure(api_key=api_key)
    
    # Configuración del modelo a utilizar
    # model = genai.GenerativeModel('gemini-1.5-flash')
    model = genai.GenerativeModel('gemini-2.5-pro')

    # gemini-1.5-flash

    # gemini-2.5-pro


except Exception as e:
    print(f"Error al configurar la API de Gemini: {e}")
    print("Asegúrate de haber configurado la variable de entorno GOOGLE_API_KEY.")
    exit()

# --- PROMPT PARA GEMINI ---
# Este es el prompt que se enviará a Gemini junto con cada imagen.
prompt_template = """
Actuando como un experto investigador y tutor.

Analizar la siguiente imagen en profundidad y realizar una investigación detallada sobre todos los conceptos relevantes que se identifiquen.

La respuesta debe ser en español y estar bien estructurada para fines educativos.

Debe incluir:
1. Descripción Detallada: Del contenido y propósito de los componentes de la imagen.
2. Investigación profunda sobre Conceptos Clave: Identificación y análisis detallado de cada concepto, teoría o elemento importante.
3. Explicación Pedagógica: Una explicación clara y didáctica de cada concepto.
4. Contexto y Aplicaciones: Dónde se aplican estos conceptos y cuál es su relevancia práctica o histórica.
5. Relaciones: Cómo se interconectan los diferentes conceptos presentados en la imagen.

Proporcionar una investigación exhaustiva, profunda y bien organizada.

Como parte de la descripción general se requiere que no se haga mención de la imagen, por ejemplo ("La imagen presenta").

El texto se debe expresar en tercera persona.
"""

def obtener_tipo_mime(ruta_archivo):
    print("")
    print("iniciar def obtener_tipo_mime(ruta_archivo)")
    print(f"ruta_archivo '{ruta_archivo}'")
    """Determina el tipo MIME basado en la extensión del archivo"""
    extension = os.path.splitext(ruta_archivo)[1].lower()
    
    print(f"extension '{extension}'")
        
    if extension == '.png':
        return '.png'
    elif extension in ('.jpg'):
        return '.jpg'
    elif extension in ('.jpeg'):
        return '.jpeg'
    elif extension == '.gif':
        return 'image/gif'
    elif extension == '.bmp':
        return 'image/bmp'
    else:
        return 'image/png'  # Por defecto
    print("Finalizar def obtener_tipo_mime(ruta_archivo)")
    print("")

def procesar_imagenes():
    """
    Función principal que itera sobre las imágenes, llama a la API de Gemini y guarda los resultados.
    """
    print("--- Iniciando el procesamiento de imágenes con Gemini ---")

    # Crear la carpeta de salida si no existe
    pathlib.Path(ruta_carpeta_salida).mkdir(parents=True, exist_ok=True)
    
    # Verificar si la carpeta de entrada existe
    if not os.path.isdir(ruta_carpeta_imagenes):
        print(f"Error: La carpeta de entrada '{ruta_carpeta_imagenes}' no existe.")
        print("Creando la carpeta. Por favor, añade tus imágenes PNG y ejecuta el script de nuevo.")
        pathlib.Path(ruta_carpeta_imagenes).mkdir(parents=True, exist_ok=True)
        return

    print(f"ruta_carpeta_imagenes:::::{ruta_carpeta_imagenes}")

    # tipo_mime = obtener_tipo_mime(ruta_imagen)

    # Obtener la lista de archivos de imagen en la carpeta
    archivos_imagen = [f for f in os.listdir(ruta_carpeta_imagenes) if f.lower().endswith(f"{obtener_tipo_mime(f)}")]
    total_imagenes = len(archivos_imagen)

    if not archivos_imagen:
        print(f"No se encontraron archivos .png en la carpeta '{ruta_carpeta_imagenes}'.")
        return

    print(f"Se encontraron {total_imagenes} imágenes para procesar.")

    # Procesar cada imagen
    for i, nombre_archivo in enumerate(archivos_imagen, 1):
        ruta_completa_imagen = os.path.join(ruta_carpeta_imagenes, nombre_archivo)
        
        try:
            print(f"\nProcesando imagen ({i}/{total_imagenes}): {nombre_archivo}...")
            
            # Abrir la imagen
            img = Image.open(ruta_completa_imagen)

            # Enviar la imagen y el prompt al modelo
            response = model.generate_content([prompt_template, img], request_options={"timeout": 120})
            
            # Crear nombre de archivo de salida con formato de fecha seguro para sistemas de archivos
            timestamp_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_base_archivo = pathlib.Path(nombre_archivo).stem
            nombre_archivo_salida = f"{nombre_base_archivo}_{timestamp_archivo}.txt"
            ruta_completa_salida = os.path.join(ruta_carpeta_salida, nombre_archivo_salida)

            # Guardar la respuesta en un archivo de texto con encabezado
            with open(ruta_completa_salida, "w", encoding="utf-8") as f:
                # Escribir encabezado informativo
                f.write(f"Análisis de la imagen: {nombre_archivo}\n")
                f.write(f"Fecha de procesamiento: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
                f.write("="*80 + "\n\n")
                # Escribir respuesta de la IA
                f.write(response.text)
            
            print(f"-> ✓ Respuesta guardada exitosamente en: {nombre_archivo_salida}")

        except Exception as e:
            print(f"-> ✗ Error al procesar la imagen {nombre_archivo}: {e}")
            with open(os.path.join(ruta_carpeta_salida, "_log_de_errores.txt"), "a", encoding="utf-8") as log:
                log.write(f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')} - Error en {nombre_archivo}: {e}\n")
        
        # Pausa entre solicitudes para no saturar la API
        time.sleep(31)

    print("\n--- Proceso finalizado ---")


if __name__ == "__main__":
    procesar_imagenes()

