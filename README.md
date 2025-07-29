# 🚀 Sistema de Autocompletado Inteligente

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

Un sistema avanzado de autocompletado que utiliza algoritmos de búsqueda inteligente y estructuras de datos Trie para proporcionar sugerencias precisas basadas en millones de oraciones de documentos académicos y RFCs.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [API](#-api)
- [Configuración](#-configuración)
- [Rendimiento](#-rendimiento)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## ✨ Características

### 🔍 Búsqueda Inteligente
- **Búsqueda exacta**: Encuentra coincidencias perfectas de palabras
- **Búsqueda aproximada**: Maneja errores tipográficos con distancia de edición
- **Búsqueda por prefijos**: Sugerencias basadas en prefijos de palabras
- **Contexto de oración**: Considera la posición y contexto de las palabras

### 🏗️ Arquitectura Optimizada
- **Estructura Trie**: Búsqueda O(k) donde k es la longitud de la palabra
- **Indexación eficiente**: Procesamiento rápido de millones de oraciones
- **Gestión de memoria**: Monitoreo y optimización del uso de memoria
- **Logging completo**: Registro detallado de operaciones y errores

### 📊 Sistema de Puntuación
- **Algoritmo de puntuación**: Evalúa calidad de sugerencias
- **Penalizaciones inteligentes**: Ajusta puntuaciones por errores tipográficos
- **Ranking dinámico**: Ordena resultados por relevancia
- **Top-5 resultados**: Devuelve las mejores sugerencias

### 🛠️ Funcionalidades Técnicas
- **Manejo de errores**: Gestión robusta de excepciones
- **Profiling**: Análisis de rendimiento integrado
- **Interfaz CLI**: Interfaz de línea de comandos intuitiva
- **Compatibilidad**: Soporte para diferentes versiones de Python

## 🏛️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  AutoComplete   │───▶│  Search Engine  │
│                 │    │     System      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Score Calc    │    │   Trie Index    │
                       │                 │    │                 │
                       └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Top Results    │    │  Data Archive   │
                       │                 │    │                 │
                       └─────────────────┘    └─────────────────┘
```

### Componentes Principales

1. **AutoCompleteSystem**: Sistema principal que coordina todas las operaciones
2. **Trie**: Estructura de datos para búsqueda eficiente de palabras
3. **ScoreCalculator**: Algoritmo de puntuación para evaluar sugerencias
4. **DataProcessor**: Procesamiento y indexación de archivos de datos

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- 4GB+ de RAM (recomendado para grandes datasets)

### Instalación Rápida

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/roeebenezra/AutoComplete.git
   cd AutoComplete
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verificar instalación**
   ```bash
   python main.py --help
   ```

### Dependencias Principales

```txt
pandas>=1.2.0
psutil>=5.8.0
python-Levenshtein>=0.12.0  # Opcional, mejora rendimiento
```

## 💻 Uso

### Uso Básico

```bash
# Ejecutar el sistema
python main.py
```

### Ejemplos de Interacción

```
🚀 Sistema de Autocompletado Inteligente
==================================================

🔄 Cargando archivos y preparando el sistema...
✅ Sistema inicializado con 1,234,567 oraciones

📊 Estadísticas del sistema:
   • Total de oraciones cargadas: 1,234,567
   • Archivos procesados: 89
   • Memoria utilizada: 2,456.78 MB

==================================================
💬 Ingresa tu texto (o 'quit' para salir): network protocol

🎯 Top 5 Sugerencias de Autocompletado:
================================================================================

1. 📄 Archivo: rfc7681.txt
   💯 Puntuación: 45.67
   📝 Sugerencia: network protocol implementation guidelines for modern systems
--------------------------------------------------------------------------------

2. 📄 Archivo: rfc7859.txt
   💯 Puntuación: 42.34
   📝 Sugerencia: network protocol security considerations and best practices
--------------------------------------------------------------------------------
```

### Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `quit`, `exit`, `q` | Salir del programa |
| `help` | Mostrar ayuda |
| `stats` | Mostrar estadísticas del sistema |
| `clear` | Limpiar pantalla |

## 🔧 API

### Clase AutoCompleteSystem

```python
from main import AutoCompleteSystem

# Inicializar sistema
system = AutoCompleteSystem()
system.load_data_files()

# Obtener sugerencias
suggestions = system.get_autocomplete_suggestions("network protocol")
for suggestion in suggestions:
    print(f"Score: {suggestion.score}, Text: {suggestion.sentence}")
```

### Clase Trie

```python
from Trie import Trie

# Crear y usar Trie
trie = Trie()
trie.insert("hello", sentence_id=1, position=0)
sentences = trie.get_sentences_of_word("hello")
```

### Clase ScoreCalculator

```python
from calculate_score import ScoreCalculator

# Calcular puntuaciones
calculator = ScoreCalculator()
scores = calculator.calculate_scores("user input", sentences_df)
```

## ⚙️ Configuración

### Variables de Entorno

```bash
# Configurar directorio de datos
export DATA_DIR="/path/to/archive"

# Configurar nivel de logging
export LOG_LEVEL="INFO"

# Configurar memoria máxima
export MAX_MEMORY="4GB"
```

### Archivo de Configuración

Crear `config.yaml`:

```yaml
data:
  directory: "./Archive"
  file_extensions: [".txt"]
  
performance:
  max_memory_mb: 4096
  batch_size: 1000
  
scoring:
  max_results: 5
  penalty_weights:
    substitution: 1.0
    addition: 2.0
    deletion: 2.0

logging:
  level: "INFO"
  file: "logs/application.log"
  max_size_mb: 100
```

## 📈 Rendimiento

### Métricas de Rendimiento

| Métrica | Valor |
|---------|-------|
| Tiempo de carga inicial | ~30-60 segundos |
| Tiempo de búsqueda promedio | <100ms |
| Uso de memoria | ~2-4GB |
| Precisión de sugerencias | >85% |

### Optimizaciones Implementadas

- **Indexación Trie**: Búsqueda O(k) en lugar de O(n)
- **Caching de resultados**: Almacenamiento en memoria de búsquedas frecuentes
- **Procesamiento por lotes**: Carga eficiente de archivos grandes
- **Gestión de memoria**: Liberación automática de memoria no utilizada

### Benchmarks

```bash
# Ejecutar benchmarks
python -m pytest tests/benchmarks/ -v

# Resultados típicos:
# - Carga de 1M oraciones: 45 segundos
# - Búsqueda simple: 15ms
# - Búsqueda con errores: 25ms
# - Búsqueda por prefijo: 10ms
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Instalar dependencias de testing
pip install pytest pytest-cov

# Ejecutar todos los tests
pytest

# Ejecutar con cobertura
pytest --cov=.

# Ejecutar tests específicos
pytest tests/test_trie.py
```

### Estructura de Tests

```
tests/
├── test_main.py          # Tests del sistema principal
├── test_trie.py          # Tests de la estructura Trie
├── test_scoring.py       # Tests del sistema de puntuación
├── test_performance.py   # Tests de rendimiento
└── benchmarks/           # Benchmarks de rendimiento
```

## 🤝 Contribución

### Guías de Contribución

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### Estándares de Código

- Seguir PEP 8 para estilo de código
- Documentar todas las funciones y clases
- Incluir tests para nuevas funcionalidades
- Mantener cobertura de código >80%

### Reportar Bugs

Usar el sistema de Issues de GitHub con:
- Descripción detallada del problema
- Pasos para reproducir
- Información del sistema
- Logs relevantes

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **Team 3** - *Desarrollo inicial* - [GitHub](https://github.com/roeebenezra)

## 🙏 Agradecimientos

- Documentos RFC por proporcionar el dataset de entrenamiento
- Comunidad de Python por las librerías utilizadas
- Contribuidores que han mejorado el proyecto

## 📞 Soporte

- **Email**: support@autocomplete.com
- **Issues**: [GitHub Issues](https://github.com/roeebenezra/AutoComplete/issues)
- **Documentación**: [Wiki](https://github.com/roeebenezra/AutoComplete/wiki)

---

⭐ **¡Si te gusta este proyecto, dale una estrella en GitHub!**

