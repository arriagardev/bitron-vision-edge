import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# 1. ENTRENAMIENTO KNN (Firma de Símbolo OK vs Ruido)
# Se ejecuta una sola vez cuando el módulo es importado.
X_train = np.array([[15.0, 200], [10.0, 180], [0.5, 30], [2.0, 45]])
y_train = np.array([1, 1, 0, 0]) # 1: OK, 0: Ruido/Fallo
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)

def procesar_imagen(img_gray: np.ndarray) -> dict:
    """
    Procesa una imagen de un panel de asiento para inspección de calidad.

    Args:
        img_gray: La imagen en escala de grises como un array de numpy.

    Returns:
        Un diccionario con los resultados de la inspección.
    """
    if img_gray is None:
        return {"veredicto_global": "NG", "error": "Imagen no válida"}

    alto, ancho = img_gray.shape

    # PROCESAMIENTO: Balance de Grises e Identificación de Símbolos
    _, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5,5), np.uint8)
    morfologia = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # IDENTIFICACIÓN POR ICONOS SUPERIORES (Franja 0-20%)
    franja = morfologia[0:int(alto*0.20), :]
    mitad_x = ancho // 2
    # Comparamos la suma de píxeles blancos en cada mitad de la franja superior
    es_modelo_a = np.sum(franja[:, :mitad_x] == 255) > np.sum(franja[:, mitad_x:] == 255)

    if es_modelo_a:
        label = "MODELO A (PILOTO) - 4 BOTONES"
        rois = {
            "Asiento": [int(alto*0.42), int(alto*0.55), int(ancho*0.28), int(ancho*0.48)],
            "SET":     [int(alto*0.35), int(alto*0.48), int(ancho*0.58), int(ancho*0.80)],
            "Boton 1": [int(alto*0.52), int(alto*0.65), int(ancho*0.62), int(ancho*0.88)],
            "Boton 2": [int(alto*0.70), int(alto*0.82), int(ancho*0.68), int(ancho*0.95)]
        }
    else:
        label = "MODELO B (COPILOTO) - 3 BOTONES"
        rois = {
            "SET":     [int(alto*0.42), int(alto*0.58), int(ancho*0.18), int(ancho*0.38)],
            "Boton 1": [int(alto*0.60), int(alto*0.75), int(ancho*0.15), int(ancho*0.32)],
            "Boton 2": [int(alto*0.76), int(alto*0.92), int(ancho*0.10), int(ancho*0.28)]
        }

    fallos = []
    detalles_roi = {}

    for zona, c in rois.items():
        roi_bin = morfologia[c[0]:c[1], c[2]:c[3]]
        roi_gray = img_gray[c[0]:c[1], c[2]:c[3]]
        
        if roi_bin.size == 0:
            es_ok = False
            densidad = 0
            mean_gray = 0
        else:
            densidad = (np.sum(roi_bin == 255) / roi_bin.size) * 100
            mean_gray = np.mean(roi_gray)
            es_ok = knn.predict([[densidad, mean_gray]])[0] == 1
        
        detalles_roi[zona] = {
            "veredicto": "OK" if es_ok else "NG",
            "densidad_percent": round(densidad, 2),
            "gris_promedio": round(mean_gray, 2)
        }
        
        if not es_ok:
            fallos.append(zona)

    resultado = {
        "veredicto_global": "OK" if not fallos else "NG",
        "modelo_detectado": label,
        "zonas_fallidas": fallos,
        "detalles_roi": detalles_roi
    }

    return resultado