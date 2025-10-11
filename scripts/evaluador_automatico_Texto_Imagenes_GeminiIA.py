# evaluador_automatico

# -*- coding: utf-8 -*-

import os
import fitz  # PyMuPDF
import google.generativeai as genai
import time
import io
from PIL import Image # Importar Pillow (requiere: pip install Pillow)

# --- CONFIGURACIÓN DE RUTAS Y PROMPT ---
# Modifica estas rutas para que apunten a tus carpetas y archivos en Debian.
# Es recomendable usar rutas absolutas (ej: /home/tu_usuario/documentos/entregas)
RUTA_CARPETA_ENTREGAS = "/home/debianuser/Downloads/"
RUTA_ARCHIVO_RUBRICA = "/home/debianuser/Documents/4. Fundacion U Los Libertadores/Clases 202502/AUDITORIA Y LEGISLACIÓN INFORMÁTICA - IS0278/Actividades/Corte I/Actividad Evaluable 1/Taller_1-IS0278 - AUDITORIA Y LEGISLACIÓN INFORMÁTICA.pdf"
ASIGNATURA = "IS0278 - AUDITORIA Y LEGISLACIÓN INFORMÁTICA"

# --- PROMPT MEJORADO Y ESTRUCTURADO ---
# Se restaura la estructura original del prompt. Es VITAL para que la IA entienda qué hacer.
# Los marcadores {rubrica_texto} y {entrega_texto} son la clave para que la IA reciba la información.
PROMPT_PLANTILLA = """
Actúa como un profesor asistente experto para la asignatura de "{ASIGNATURA}".
Tu misión es evaluar la entrega de un estudiante de manera objetiva, basándote ESTRICTAMENTE en la rúbrica de evaluación que te proporciono.

**RÚBRICA DE EVALUACIÓN (CRITERIOS):**
---
{rubrica_texto}
---

**DOCUMENTO ENTREGADO POR EL ESTUDIANTE (CONTIENE TEXTO E IMÁGENES):**
---
{entrega_texto}
---

**INSTRUCCIONES PRECISAS:**
1.  **Analiza la entrega del estudiante** en su totalidad, incluyendo el texto y el contenido de las imágenes.
2.  **Verifica el cumplimiento de cada criterio** definido en la rúbrica. Si una imagen es relevante para un criterio (ej. un diagrama, un pantallazo de código), considérala en la evaluación.
3.  **Calcula la puntuación:** El puntaje total es de 50 puntos. Asigna un puntaje a cada criterio según su cumplimiento y describe la ponderación porcentual cumplida para cada uno.
4.  **Genera un informe estructurado** con el siguiente formato exacto:

**FORMATO DE RESPUESTA OBLIGATORIO:**
---
**Análisis de Criterios:**
- **Criterio 1 [Nombre del Criterio]:** Cumplimiento: [XX]%. Puntos: [Puntos sobre el total del criterio]. Justificación: [Breve explicación de por qué se asignó ese puntaje, mencionando imágenes si es relevante].
- **Criterio 2 [Nombre del Criterio]:** Cumplimiento: [XX]%. Puntos: [Puntos sobre el total del criterio]. Justificación: [Breve explicación].
- (Repetir para todos los criterios)

**Puntaje Final:** [Suma de todos los puntos] / 50

---
"""

# --- INICIO DEL SCRIPT ---

def configurar_api():
    """Configura la API de Gemini usando una variable de entorno."""
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("La variable de entorno GOOGLE_API_KEY no está configurada.")
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"Error en la configuración de la API: {e}")
        return False

def extraer_texto_de_pdf(ruta_pdf):
    """Abre un archivo PDF y extrae únicamente su contenido de texto."""
    try:
        with fitz.open(ruta_pdf) as doc:
            texto_completo = ""
            for pagina in doc:
                texto_completo += pagina.get_text()
            return texto_completo
    except Exception as e:
        print(f"Error al leer el archivo PDF '{ruta_pdf}': {e}")
        return None

def extraer_contenido_multimodal_de_pdf(ruta_pdf):
    """
    Abre un archivo PDF y extrae una lista de contenido multimodal (texto e imágenes).
    Las imágenes se devuelven como objetos de Pillow (PIL).
    """
    try:
        doc = fitz.open(ruta_pdf)
        contenido = []
        for page in doc:
            # Extraer texto de la página
            contenido.append(page.get_text())

            # Extraer imágenes de la página
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # Convertir los bytes de la imagen a un objeto PIL.Image
                image = Image.open(io.BytesIO(image_bytes))
                contenido.append(image)
        doc.close()
        return contenido
    except Exception as e:
        print(f"Error al procesar el archivo PDF multimodal '{ruta_pdf}': {e}")
        return None


def evaluar_entrega(modelo, rubrica_texto, entrega_contenido, asignatura):
    """Envía la solicitud multimodal a la API de Gemini y devuelve la evaluación."""

    # Construye la solicitud multimodal. Es una lista de partes (texto e imágenes).
    solicitud_completa = [
        # Parte 1: El inicio del prompt con el rol, la rúbrica y las instrucciones.
        PROMPT_PLANTILLA.split('{entrega_texto}')[0].format(
            ASIGNATURA=asignatura,
            rubrica_texto=rubrica_texto
        ),
        # A continuación, se insertará el contenido del PDF del estudiante (texto e imágenes)
    ]

    # Agrega el contenido del estudiante (texto e imágenes) a la solicitud
    solicitud_completa.extend(entrega_contenido)

    # Parte final: El resto del prompt que cierra las instrucciones.
    solicitud_completa.append(PROMPT_PLANTILLA.split('{entrega_texto}')[1])

    try:
        response = modelo.generate_content(solicitud_completa)
        return response.text
    except Exception as e:
        return f"Error al generar la evaluación: {e}"

def main():
    """Función principal que orquesta el proceso de evaluación."""
    if not configurar_api():
        return

    print("--- Iniciando Proceso de Evaluación Automática (Modo Multimodal) ---")
    print("Asegúrate de haber instalado Pillow: pip install Pillow")


    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo_salida = f"resultados_evaluacion_{timestamp}.txt"

    # 1. Extraer el texto de la rúbrica (se asume que la rúbrica solo tiene texto relevante)
    print(f"Cargando rúbrica desde: {RUTA_ARCHIVO_RUBRICA}")
    rubrica_texto = extraer_texto_de_pdf(RUTA_ARCHIVO_RUBRICA)
    if not rubrica_texto:
        print("No se pudo procesar la rúbrica. Abortando.")
        return

    # Instanciar el modelo. Se recomienda usar 'latest' para obtener la última versión estable.
    # gemini-1.5-pro-latest es un modelo multimodal, puede procesar texto e imágenes.
    modelo = genai.GenerativeModel('gemini-1.5-pro-latest')

    # 2. Iterar sobre los archivos de los estudiantes
    try:
        lista_archivos = os.listdir(RUTA_CARPETA_ENTREGAS)
        archivos_pdf_estudiantes = [f for f in lista_archivos if f.lower().endswith('.pdf')]

        if not archivos_pdf_estudiantes:
            print(f"No se encontraron archivos PDF en la carpeta: {RUTA_CARPETA_ENTREGAS}")
            return

        print(f"Se encontraron {len(archivos_pdf_estudiantes)} entregas en PDF para evaluar.")

        # 3. Procesar cada entrega y guardar los resultados
        with open(nombre_archivo_salida, "w", encoding="utf-8") as archivo_resultados:
            for nombre_archivo in archivos_pdf_estudiantes:
                ruta_completa_entrega = os.path.join(RUTA_CARPETA_ENTREGAS, nombre_archivo)
                print(f"\nProcesando: {nombre_archivo}...")

                # Usamos la nueva función para extraer texto e imágenes
                entrega_contenido = extraer_contenido_multimodal_de_pdf(ruta_completa_entrega)

                if not entrega_contenido:
                    resultado = "No se pudo extraer contenido (texto/imágenes) de este archivo."
                else:
                    print(f"Contenido extraído. Enviando a la API...")
                    # Hacemos la llamada a la API con el contenido multimodal
                    resultado = evaluar_entrega(modelo, rubrica_texto, entrega_contenido, ASIGNATURA)
                    print("Esperando 70 segundos para no exceder la cuota de la API...")
                    time.sleep(70)

                # Escribir el resultado en el archivo
                archivo_resultados.write(f"========================================\n")
                archivo_resultados.write(f"Archivo: {nombre_archivo}\n")
                archivo_resultados.write(f"========================================\n\n")
                archivo_resultados.write(f"{resultado}\n\n\n")
                print(f"Evaluación de '{nombre_archivo}' completada y guardada.")

    except FileNotFoundError:
        print(f"Error: La carpeta de entregas no se encontró en la ruta: '{RUTA_CARPETA_ENTREGAS}'")
        return

    print("\n--- Proceso de Evaluación Finalizado ---")
    print(f"Los resultados han sido guardados en '{nombre_archivo_salida}'")

if __name__ == "__main__":
    main()

