# Bitron Vision Edge

Este repositorio contiene el código para el sistema de visión por computador que se ejecuta en el borde (edge), específicamente en una Raspberry Pi. Es responsable de capturar imágenes, procesarlas y comunicar los resultados a través de MQTT.

## Arquitectura

Este proyecto forma parte de un sistema más grande compuesto por:
*   **`bitron-vision-edge`**: Este repositorio. Lógica de visión en el borde.
*   **`bitron-backend`**: (Enlace al repo) Backend que recibe los datos.
*   **`bitron-console`**: (Enlace al repo) Consola web para visualización.

## Primeros Pasos

Sigue estas instrucciones para tener una copia del proyecto funcionando en tu máquina local para desarrollo y pruebas.

### Prerrequisitos

- Python 3.9+
- Docker
- Un broker MQTT (local o en la nube)

### Instalación

1.  Clona el repositorio:
    ```sh
    git clone <https://github.com/tu-usuario/bitron-vision-edge.git>
    cd bitron-vision-edge
    ```

2.  Crea y activa un entorno virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

Para ejecutar la aplicación localmente (sin Docker):

```sh
python src/main.py
```

# Bitron Vision Edge

Módulo de procesamiento de imágenes al borde (Edge Computing) para la inspección de paneles de asiento BMW X6 G06. Desarrollado para Raspberry Pi / ESP32-S3.

## Requisitos
* Docker y Docker Compose
* Python 3.10+ (para desarrollo local)

## Desarrollo Local
1. Instalar dependencias: `pip install -r requirements.txt`
2. Ejecutar el orquestador: `python src/main.py`

## Despliegue con Docker
Construir la imagen:
`docker build -t bitron-vision-edge .`

Ejecutar el contenedor:
`docker run -d --name bitron-edge bitron-vision-edge`