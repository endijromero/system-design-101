import os
from google import genai
from datetime import datetime
import base64
from google.genai.types import Content, Part, Blob

# Configuración de rutas - MODIFICA ESTAS VARIABLES SEGÚN TUS NECESIDADES
RUTA_IMAGENES = "/home/debianuser/Documents/proyectos/python/system-design-101/imagesUno"  # Cambia por tu ruta de imágenes
RUTA_SALIDA = "/home/debianuser/Documents/proyectos/python/system-design-101/imagesUno"  # Cambia por tu ruta de salida

def encode_image(image_path):
    """Codifica una imagen en base64 para la API de Gemini"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def procesar_imagen(ruta_imagen, cliente):
    """Procesa una imagen individual con Gemini"""
    try:
        # Codificar la imagen
        imagen_base64 = encode_image(ruta_imagen)
        
        # Crear el prompt en español
        prompt_text = """
        Analiza esta imagen en profundidad y realiza una investigación detallada sobre todos los conceptos relevantes que identifiques. 
        Tu respuesta debe ser en español y debe incluir:
        
        1. Descripción general del contenido de la imagen
        2. Análisis detallado de cada concepto identificado
        3. Explicación pedagógica para fines educativos
        4. Contexto y aplicaciones prácticas de los conceptos
        5. Relaciones entre los diferentes conceptos presentes
        
        Proporciona una investigación exhaustiva y bien estructurada.
        """
        
        # Crear la estructura correcta de contenido para la API
        contents = [
            Content(
                role="user",
                parts=[
                    Part(text=prompt_text),
                    Part(
                        inline_data=Blob(
                            mime_type="image/png",
                            data=imagen_base64
                        )
                    )
                ]
            )
        ]
        
        # Enviar la imagen y prompt a Gemini
        response = cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )
        
        return response.text
    
    except Exception as e:
        return f"Error al procesar la imagen: {str(e)}"

def main():
    """Función principal del script"""
    
    # Verificar que las rutas existen
    if not os.path.exists(RUTA_IMAGENES):
      print(f"Error: La ruta de imágenes no existe: {RUTA_IMAGENES}")
      return
    
    if not os.path.exists(RUTA_SALIDA):
        os.makedirs(RUTA_SALIDA)
        print(f"Creada ruta de salida: {RUTA_SALIDA}")
    
    # Inicializar cliente de Gemini con API key explícita
    # Reemplaza 'TU_API_KEY_AQUI' con tu API key real
    cliente = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    # Verificar que la API key está disponible
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY no está configurada en las variables de entorno")
        return
    
    # Obtener lista de archivos PNG
    archivos_png = [f for f in os.listdir(RUTA_IMAGENES) if f.lower().endswith('.png')]
    
    if not archivos_png:
        print("No se encontraron archivos PNG en la ruta especificada.")
        return
    
    print(f"Se encontraron {len(archivos_png)} archivos PNG para procesar...")
    
    # Procesar cada imagen
    for i, nombre_archivo in enumerate(archivos_png, 1):
        ruta_completa_imagen = os.path.join(RUTA_IMAGENES, nombre_archivo)
        
        print(f"Procesando ({i}/{len(archivos_png)}): {nombre_archivo}")
        
        # Procesar la imagen con Gemini
        resultado = procesar_imagen(ruta_completa_imagen, cliente)
        
        # Crear nombre de archivo de salida con formato yyyy-MM-dd HH-mm-ss
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        nombre_base = os.path.splitext(nombre_archivo)[0]
        nombre_archivo_salida = f"{nombre_base}_{fecha_actual}.txt"
        ruta_completa_salida = os.path.join(RUTA_SALIDA, nombre_archivo_salida)
        
        # Guardar resultado en archivo
        try:
            with open(ruta_completa_salida, 'w', encoding='utf-8') as archivo_salida:
                archivo_salida.write(f"Análisis de: {nombre_archivo}\n")
                archivo_salida.write(f"Fecha de procesamiento: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
                archivo_salida.write("="*80 + "\n\n")
                archivo_salida.write(resultado)
            
            print(f"✓ Resultado guardado: {nombre_archivo_salida}")
        
        except Exception as e:
            print(f"✗ Error guardando archivo {nombre_archivo_salida}: {str(e)}")
        
        # Pequeña pausa entre procesamientos para no saturar la API
        import time
        time.sleep(1)
    
    print("\n¡Procesamiento completado!")

if __name__ == "__main__":
    main()