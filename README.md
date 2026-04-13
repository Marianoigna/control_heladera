# ERROR PROOFING — AIS BOX

Monitor de temperatura en tiempo real usando **Django**, **WebSockets** y **MQTT**.  
Los datos llegan desde un sensor (o simulador MQTTX) a través de un broker MQTT público, se almacenan en SQLite3 y se reflejan instantáneamente en el dashboard sin recargar la página.

---

## Arquitectura

```
[Sensor / MQTTX]
       │
       │  MQTT (broker.emqx.io:8084 WSS)
       ▼
[mqtt_subscriber.py]
       │
       │  POST /api/temperatura/
       ▼
[Django REST API]
       │
       ├──► SQLite3 (persistencia)
       │
       └──► Django Channels (WebSocket)
                   │
                   ▼
           [Dashboard HTML]
         (actualización en tiempo real)
```

---

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Django 6 + Django REST Framework |
| WebSockets | Django Channels + Daphne (ASGI) |
| MQTT | paho-mqtt (WSS sobre broker.emqx.io) |
| Base de datos | SQLite3 |
| Frontend | HTML + CSS + JavaScript vanilla |

---

## Estructura del proyecto

```
ERROR PROOFING/
├── levantar_servidor.bat        # Script para levantar todo con un doble clic
├── activar_entorno.bat          # Activa el entorno virtual
├── .gitignore
└── ERROR_PROOFING/
    ├── manage.py
    ├── mqtt_subscriber.py       # Puente MQTT → API REST
    ├── AIS_BOX/                 # App principal
    │   ├── models.py            # Modelo Temperatura
    │   ├── views.py             # API REST + vista dashboard
    │   ├── consumers.py         # WebSocket consumer
    │   ├── serializers.py
    │   ├── urls.py
    │   ├── routing.py
    │   └── templates/
    │       └── AIS_BOX/
    │           └── dashboard.html
    └── ERROR_PROOFING/
        ├── settings.py
        ├── asgi.py
        └── urls.py
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Marianoigna/ERROR_PROOFING.git
cd ERROR_PROOFING
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install django djangorestframework channels daphne paho-mqtt requests
```

### 4. Aplicar migraciones

```bash
cd ERROR_PROOFING
python manage.py migrate
```

---

## Levantar el servidor

### Opción A — Script automático (recomendado)

Doble clic en **`levantar_servidor.bat`** desde la raíz del proyecto.  
Abre dos ventanas: una con el Django server y otra con el MQTT subscriber.

### Opción B — Manual

Abrir **dos terminales** con el entorno virtual activado:

**Terminal 1 — Django:**
```bash
cd ERROR_PROOFING
python manage.py runserver
```

**Terminal 2 — MQTT Subscriber:**
```bash
cd ERROR_PROOFING
python mqtt_subscriber.py
```

---

## Uso con MQTTX (simulador de sensor)

1. Descargar [MQTTX](https://mqttx.app/)
2. Crear nueva conexión:
   - **Host:** `broker.emqx.io`
   - **Port:** `1883`
   - **Protocol:** MQTT
3. Publicar en el topic `temperatura_prueba` con alguno de estos payloads:

```json
{"sensor_id": "sensor_01", "valor": 25.3}
```

```
25.3
```

4. Abrir el dashboard en `http://127.0.0.1:8000/` y ver el valor actualizarse en tiempo real.

---

## API REST

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/temperatura/` | Últimas 50 lecturas |
| `POST` | `/api/temperatura/` | Registra nueva lectura |

**Ejemplo POST:**
```json
{
  "sensor_id": "sensor_01",
  "valor": 25.3
}
```

---

## Dashboard

Accesible en `http://127.0.0.1:8000/`

- Muestra el valor de temperatura actual en tiempo real
- Cambia de color según el rango (azul frío / rojo caliente)
- Historial de las últimas 20 lecturas
- Indicador de estado de conexión WebSocket con reconexión automática
