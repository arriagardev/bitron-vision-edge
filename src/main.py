import time
import json
import paho.mqtt.client as mqtt
import cv2
import uuid
from vision_algoritmo import procesar_imagen

# Configuración MQTT (Estos valores luego pueden venir de variables de entorno)
MQTT_BROKER = "192.168.1.100" # IP del servidor donde estará Mosquitto/Blazor
MQTT_PORT = 1883
TOPIC_RESULTADOS = "bitron/linea1/inspeccion/resultado"
# Ruta a la imagen de prueba. En producción, esto vendría de una cámara.
RUTA_IMAGEN_PRUEBA = "data/sample_image.png"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Conectado al broker MQTT con código: {reason_code}")
    # Aquí podríamos suscribirnos a un tópico de configuración:
    # client.subscribe("bitron/linea1/config")

def iniciar_edge():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        print(f"Error conectando al broker: {e}")
        return

    client.loop_start()

    print("Iniciando servicio de inspección BMW Bitron...")
    
    try:
        while True:
            # 1. Capturar imagen (aquí leemos de un archivo para simular)
            # En un sistema real, la función capturar_frame() se encargaría de esto.
            img_gray = cv2.imread(RUTA_IMAGEN_PRUEBA, cv2.IMREAD_GRAYSCALE)
            
            if img_gray is None:
                print(f"Error: No se pudo cargar la imagen de prueba en '{RUTA_IMAGEN_PRUEBA}'")
                time.sleep(5)
                continue

            # 2. Llamar al algoritmo de visión
            resultado_vision = procesar_imagen(img_gray)
            
            # 3. Enriquecer el payload con metadatos
            payload_final = {
                "transaccion_id": f"tx-{uuid.uuid4()}",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                **resultado_vision
            }
            
            # 4. Publicar resultados al servidor
            client.publish(TOPIC_RESULTADOS, json.dumps(payload_final))
            print(f"Resultados publicados: {payload_final['veredicto_global']} (Modelo: {payload_final.get('modelo_detectado', 'N/A')})")
            
            # Esperar antes de la siguiente captura (ajustar según el ciclo de la línea)
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("Deteniendo servicio...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    iniciar_edge()