# 📦 Backup del Proyecto - Servicios de IA en AWS

Este repositorio contiene una **copia (backup)** de un laboratorio práctico enfocado en el uso de servicios de Inteligencia Artificial de AWS.

---

## ⚠️ Importante

Este repositorio:

* Es una copia del proyecto original
* Puede no reflejar cambios recientes del repositorio fuente
* Se utiliza con fines de aprendizaje, práctica y respaldo

---

## 🎯 Objetivo del Proyecto

Aplicar servicios de IA de AWS para resolver problemas reales como:

* Procesamiento de texto
* Análisis de audio
* Detección de entidades
* Automatización de flujos de datos

---

## 🧠 Ejercicios realizados

Durante este laboratorio se desarrollaron los siguientes ejercicios:

### 🔹 1. Análisis de entidades con AWS Comprehend

* Identificación de entidades (personas, lugares, organizaciones)
* Detección de información sensible (PII)
* Procesamiento de texto en lenguaje natural

---

### 🔹 2. Pipeline de audio (Transcribe + Polly)

* Conversión de audio a texto usando AWS Transcribe
* Generación de voz a partir de texto con AWS Polly
* Automatización del flujo completo de procesamiento de audio

---

### 🔹 3. Procesamiento y almacenamiento de resultados

* Conversión de resultados a formato JSON
* Organización de salidas en la carpeta `outputs/`
* Manejo de archivos desde Python

---

### 🔹 4. Uso de AWS Rekognition

* Análisis de imágenes
* Detección de objetos y características
* Interpretación de resultados generados por el servicio

---

### 🔹 5. Automatización con scripts en Python

* Integración de múltiples servicios de AWS
* Manejo de errores comunes
* Ejecución de pipelines completos

---

## 🛠️ Tecnologías utilizadas

* Python 🐍
* AWS SDK (Boto3)
* Amazon Comprehend
* Amazon Transcribe
* Amazon Polly
* Amazon Rekognition

---

## 📁 Estructura del proyecto

```bash id="p3q8jm"
.
├── data/              # Archivos de entrada
├── ejercicios/        # Scripts de los ejercicios
├── outputs/           # Resultados generados
├── validate.py        # Validaciones
└── README.md
```

---

## 🚫 Exclusiones recomendadas

Para mantener el repositorio limpio:

* `.venv/`
* `__pycache__/`
* Archivos temporales

---

## 🚀 Cómo usar este proyecto

1. Clonar el repositorio
2. Crear entorno virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Instalar dependencias
4. Configurar credenciales de AWS
5. Ejecutar los scripts en la carpeta `ejercicios/`

---

## 🔄 Origen

Proyecto basado en un laboratorio de servicios de IA en AWS.

---

## 📌 Nota final

Este repositorio **no está sincronizado automáticamente** con el original y representa un estado específico del proyecto al momento del respaldo.

---

✨ Proyecto desarrollado con fines académicos y de práctica en IA y Cloud Computing.
