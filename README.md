# 🍷 Wine Quality Prediction - ML Pipeline con CI/CD

Pipeline automatizado de Machine Learning con MLflow tracking y GitHub Actions CI/CD para predicción de calidad de vino.

## 📋 Descripción

Este proyecto implementa un pipeline completo de MLOps que:
- Descarga automáticamente el dataset de Wine Quality desde UCI
- Realiza preprocesamiento y limpieza de datos
- Entrena un modelo de Random Forest para clasificación
- Realiza tracking completo con MLflow (parámetros, métricas, modelos)
- Automatiza todo el proceso mediante GitHub Actions

## 🎯 Características

- ✅ Dataset externo (UCI Wine Quality) - no sklearn.datasets
- ✅ Preprocesamiento completo (limpieza, escalamiento, codificación)
- ✅ Entrenamiento con Random Forest Classifier
- ✅ Evaluación con múltiples métricas (Accuracy, F1, Precision, Recall)
- ✅ MLflow tracking local con registro de modelo
- ✅ CI/CD completo con GitHub Actions
- ✅ Makefile para automatización de tareas
- ✅ Tests unitarios con pytest
- ✅ Linting con flake8

## 🏗️ Estructura del Proyecto

```
ml-pipeline-project/
├── .github/
│   └── workflows/
│       └── ml.yml              # GitHub Actions workflow
├── src/
│   ├── __init__.py
│   └── train.py                # Script principal de entrenamiento
├── tests/
│   └── test_pipeline.py        # Tests unitarios
├── data/
│   └── .gitkeep               # Directorio para datos
├── config.yaml                 # Configuración de hiperparámetros
├── requirements.txt            # Dependencias del proyecto
├── Makefile                    # Tareas automatizadas
├── README.md                   # Este archivo
└── .gitignore                  # Archivos ignorados por git
```

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.9 o superior
- pip
- Git

### Instalación Local

1. **Clonar el repositorio:**
```bash
git clone <URL_DEL_REPOSITORIO>
cd ml-pipeline-project
```

2. **Instalar dependencias:**
```bash
make install
# O manualmente:
pip install -r requirements.txt
```

## 💻 Uso

### Comandos Disponibles (Makefile)

```bash
make help       # Mostrar ayuda con todos los comandos
make install    # Instalar dependencias
make train      # Ejecutar pipeline completo
make test       # Ejecutar tests
make lint       # Verificar código con flake8
make format     # Formatear código con black
make clean      # Limpiar archivos generados
make all        # Ejecutar todo: install, lint, test, train
```

### Ejecutar el Pipeline Manualmente

```bash
# Opción 1: Usar Makefile (recomendado)
make train

# Opción 2: Ejecutar directamente
python src/train.py
```

### Ejecutar Tests

```bash
# Opción 1: Usar Makefile
make test

# Opción 2: Ejecutar pytest directamente
pytest tests/ -v
```

## 📊 Dataset

**Fuente:** UCI Machine Learning Repository  
**Nombre:** Wine Quality Dataset (Red Wine)  
**URL:** https://archive.ics.uci.edu/ml/datasets/wine+quality

**Características:**
- 1599 muestras de vino tinto
- 11 características físico-químicas
- Target: Calidad del vino (convertida a clasificación binaria)

**Preprocesamiento:**
- Conversión a problema de clasificación binaria (bueno: calidad ≥ 6, malo: calidad < 6)
- Manejo de valores faltantes con media
- Escalamiento con StandardScaler
- División 80-20 train-test con estratificación

## 🤖 Modelo

**Algoritmo:** Random Forest Classifier

**Hiperparámetros (configurables en `config.yaml`):**
- n_estimators: 100
- max_depth: 10
- min_samples_split: 2
- min_samples_leaf: 1
- random_state: 42

## 📈 Métricas de Evaluación

El pipeline calcula y registra:
- **Accuracy:** Precisión general del modelo
- **F1 Score:** Media armónica de precisión y recall
- **Precision:** Proporción de predicciones positivas correctas
- **Recall:** Proporción de casos positivos identificados

## 🔬 MLflow Tracking

### Visualizar Resultados

```bash
# Iniciar UI de MLflow
mlflow ui

# Acceder en el navegador a:
# http://localhost:5000
```

### Información Registrada

MLflow registra automáticamente:
- **Parámetros:** Hiperparámetros del modelo y configuración
- **Métricas:** Accuracy, F1, Precision, Recall
- **Modelo:** Modelo entrenado con firma y ejemplo de entrada
- **Artefactos:** Modelo serializado registrado como "wine_quality_classifier"

## 🔄 CI/CD con GitHub Actions

### Workflow Automático

El archivo `.github/workflows/ml.yml` ejecuta automáticamente:

1. **Setup:** Checkout código + Setup Python 3.9
2. **Install:** Instalación de dependencias
3. **Lint:** Verificación de código
4. **Test:** Ejecución de tests
5. **Train:** Entrenamiento del modelo
6. **Artifacts:** Guardado de modelo y MLflow data

### Triggers

El workflow se ejecuta en:
- Push a `main` o `develop`
- Pull requests a `main`
- Manualmente desde GitHub Actions tab

### Ver Resultados

1. Ir a la pestaña "Actions" en GitHub
2. Seleccionar el workflow run
3. Descargar artifacts generados

## 🧪 Testing

El proyecto incluye tests para:
- Validación de configuración
- Estructura del proyecto
- Lógica de preprocesamiento
- Existencia de directorios críticos

```bash
# Ejecutar todos los tests
make test

# Ejecutar tests con más detalle
pytest tests/ -v --tb=long
```

## 📝 Configuración

Editar `config.yaml` para modificar:
- URL del dataset
- Tamaño del test set
- Hiperparámetros del modelo
- Configuración de preprocesamiento
- Nombre del experimento en MLflow

Ejemplo:

```yaml
model:
  type: "random_forest"
  params:
    n_estimators: 200      # Cambiar número de árboles
    max_depth: 15          # Cambiar profundidad máxima
```

## 🛠️ Desarrollo

### Agregar Nuevas Features

1. Modificar `src/train.py`
2. Actualizar tests en `tests/test_pipeline.py`
3. Ejecutar `make lint` y `make test`
4. Commit y push

### Cambiar Modelo

1. Importar nuevo modelo en `src/train.py`
2. Actualizar función `train_model()`
3. Actualizar `config.yaml` con nuevos parámetros

## 📦 Entregables

Este proyecto incluye todos los entregables solicitados:

1. ✅ **Repositorio Git:** Estructura completa con código fuente
2. ✅ **MLflow Tracking:** Registro completo de experimentos
3. ✅ **GitHub Actions:** Pipeline CI/CD funcional
4. ✅ **README:** Documentación completa
5. ✅ **Tests:** Suite de pruebas unitarias
6. ✅ **Makefile:** Automatización de tareas

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError"
```bash
make install  # Reinstalar dependencias
```

### Error: "No module named 'src'"
```bash
# Asegurarse de estar en el directorio raíz del proyecto
cd ml-pipeline-project
```

### MLflow UI no muestra experimentos
```bash
# Verificar que mlruns/ existe
ls mlruns/

# Reiniciar MLflow UI
mlflow ui --backend-store-uri file:./mlruns
```

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👥 Autor

Proyecto desarrollado como parte del curso de MLOps.

## 🙏 Referencias

- Dataset: Cortez, Paulo et al. "Wine Quality" UCI Machine Learning Repository
- MLflow Documentation: https://mlflow.org/docs/latest/index.html
- GitHub Actions: https://docs.github.com/en/actions

---

**Nota:** Este README es parte del proyecto de automatización de pipelines de ML con prácticas modernas de MLOps.
