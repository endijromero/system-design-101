# evaluador_automatico

# -*- coding: utf-8 -*-

import os
import fitz  # PyMuPDF
import google.generativeai as genai
import time

# --- CONFIGURACIÓN DE RUTAS Y PROMPT ---
# Modifica estas rutas para que apunten a tus carpetas y archivos en Debian.
# Es recomendable usar rutas absolutas (ej: /home/tu_usuario/documentos/entregas)
RUTA_CARPETA_ENTREGAS = "/home/debianuser/Downloads/"
# RUTA_ARCHIVO_RUBRICA = "/home/debianuser/Downloads/Taller_1-IS0278 - AUDITORIA Y LEGISLACIÓN INFORMÁTICA.pdf"
RUTA_ARCHIVO_RUBRICA = "/home/debianuser/Documents/4. Fundacion U Los Libertadores/Clases 202502/AUDITORIA Y LEGISLACIÓN INFORMÁTICA - IS0278/Actividades/Corte I/Actividad Evaluable 1/Taller_1-IS0278 - AUDITORIA Y LEGISLACIÓN INFORMÁTICA.pdf"

ASIGNATURA = "IS0278 - AUDITORIA Y LEGISLACIÓN INFORMÁTICA"
timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
nombre_archivo_salida = f"resultados_evaluacion_{timestamp}.txt"

# Este es el corazón de la evaluación. Personalízalo detalladamente.
# Usa {rubrica_texto} y {entrega_texto} como marcadores de posición.
PROMPT_PLANTILLA = """

En el documento adjunto "Taller_1-IS0278 - AUDITORIA Y LEGISLACIÓN INFORMÁTICA.pdf" que contiene RÚBRICA DE EVALUACIÓN (CRITERIOS), se describe una actividad a los estudiantes de la asignatura "{ASIGNATURA}".

Dada la información anterior se requiere verificar si los criterios de evaluación definidos en el documento de la actividad, se cumplen en el documento entregado por los alumnos.

**RÚBRICA DE EVALUACIÓN (CRITERIOS):**
---
{rubrica_texto}
---

**DOCUMENTO ENTREGADO POR EL ESTUDIANTE:**
---
{entrega_texto}
---

**INSTRUCCIONES PRECISAS:**
1.  **Analiza la entrega del estudiante** en su totalidad.
2.  **Verifica el cumplimiento de cada criterio** definido en la rúbrica.
3.  **Calcula la puntuación:** El puntaje total es de 50 puntos. Asigna un puntaje a cada criterio según su cumplimiento y describe la ponderación porcentual cumplida para cada uno.
4.  **Genera un informe estructurado** con el siguiente formato exacto:

**FORMATO DE RESPUESTA OBLIGATORIO:**
---
**Análisis de Criterios:**
- **Criterio 1 [Nombre del Criterio]:** Cumplimiento: [XX]%. Puntos: [Puntos sobre el total del criterio]. Justificación: [Breve explicación de por qué se asignó ese puntaje].
- **Criterio 2 [Nombre del Criterio]:** Cumplimiento: [XX]%. Puntos: [Puntos sobre el total del criterio]. Justificación: [Breve explicación].
- (Repetir para todos los criterios)

**Puntaje Final:** [Suma de todos los puntos] / 50

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
    """Abre un archivo PDF y extrae todo su contenido de texto."""
    try:
        with fitz.open(ruta_pdf) as doc:
            texto_completo = ""
            for pagina in doc:
                texto_completo += pagina.get_text()
            return texto_completo
    except Exception as e:
        print(f"Error al leer el archivo PDF '{ruta_pdf}': {e}")
        return None

def evaluar_entrega(modelo, rubrica_texto, entrega_texto):
    """Envía la solicitud a la API de Gemini y devuelve la evaluación."""
    prompt_completo = PROMPT_PLANTILLA.format(
        ASIGNATURA=ASIGNATURA,
        rubrica_texto=rubrica_texto,
        entrega_texto=entrega_texto
    )
    
    try:
        print(f"Texto completo {prompt_completo}")
        response = modelo.generate_content(prompt_completo)
        return response.text
    except Exception as e:
        return f"Error al generar la evaluación: {e}"

def main():
    """Función principal que orquesta el proceso de evaluación."""
    if not configurar_api():
        return

    print("--- Iniciando Proceso de Evaluación Automática ---")

    # 1. Extraer el texto de la rúbrica (se hace una sola vez)
    print(f"Cargando rúbrica desde: {RUTA_ARCHIVO_RUBRICA}")
    rubrica_texto = extraer_texto_de_pdf(RUTA_ARCHIVO_RUBRICA)
    if not rubrica_texto:
        print("No se pudo procesar la rúbrica. Abortando.")
        return

    # Instanciar el modelo
    modelo = genai.GenerativeModel('gemini-2.5-pro')

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

                print(f"Ruta {RUTA_CARPETA_ENTREGAS}{nombre_archivo}")

                ruta_completa_entrega = os.path.join(RUTA_CARPETA_ENTREGAS, nombre_archivo)
                print(f"\nProcesando: {nombre_archivo}...")

                entrega_texto = extraer_texto_de_pdf(ruta_completa_entrega)

                print(f"Texto del PDF {entrega_texto}")

                if not entrega_texto:
                    resultado = "No se pudo extraer el texto de este archivo."
                    print(f"Resultado {resultado}")
                else:
                    # Hacemos la llamada a la API
                    resultado = evaluar_entrega(modelo, rubrica_texto, entrega_texto)
                    # Pequeña pausa para no exceder los límites de la API (requests por minuto)
                    time.sleep(70)

                # Escribir el resultado en el archivo
                archivo_resultados.write(f"========================================\n")
                archivo_resultados.write(f"========================================\n")
                archivo_resultados.write(f"Archivo: {nombre_archivo}\n")
                archivo_resultados.write(f"========================================\n\n")
                archivo_resultados.write(f"{resultado}\n\n\n")
                archivo_resultados.write(f"========================================\n")
                archivo_resultados.write(f"========================================\n")
                print(f"Evaluación de '{nombre_archivo}' completada y guardada.")

    except FileNotFoundError:
        print(f"Error: La carpeta de entregas no se encontró en la ruta: '{RUTA_CARPETA_ENTREGAS}'")
        return
        
    print("\n--- Proceso de Evaluación Finalizado ---")
    print(f"Los resultados han sido guardados en '{nombre_archivo_salida}'")

if __name__ == "__main__":
    main()
