# Smart Horses Backend

Backend REST API para el juego Smart Horses desarrollado para el curso de Inteligencia Artificial de la Universidad del Valle.

## 🎮 Descripción del Juego

Smart Horses es un juego estratégico de dos jugadores (humano vs IA) donde dos caballos compiten en un tablero 8×8 por capturar casillas con valores. La IA utiliza el algoritmo Minimax con poda Alpha-Beta para tomar decisiones inteligentes.

### Características Principales

- **Algoritmo Minimax**: Implementación completa con poda Alpha-Beta
- **Función Heurística**: Evaluación sofisticada basada en 5 factores estratégicos
- **Prevención de Colisiones**: Los caballos no pueden ocupar la misma casilla
- **Tres Niveles de Dificultad**:
  - Principiante (profundidad 2)
  - Amateur (profundidad 4)
  - Experto (profundidad 6)
- **28 Tests Automatizados**: Cobertura completa del código
- **API REST**: Endpoints bien documentados con Flask

## 🚀 Tecnologías

- **Python 3.13.1**
- **Flask 3.0.0**: Framework web
- **Pytest 9.0.1**: Testing
- **CORS**: Soporte para frontend separado

## 📁 Estructura del Proyecto

```
smart_backend/
├── algorithms/        # Minimax y heurística
│   ├── minimax.py    # Algoritmo Minimax con poda Alpha-Beta
│   └── heuristic.py  # Función de evaluación heurística
├── core/             # Lógica del juego
│   ├── board_manager.py    # Gestión del tablero
│   ├── game_state.py       # Estado del juego
│   └── move_generator.py   # Generador de movimientos legales
├── routes/           # API endpoints
│   └── game_routes.py
├── app.py           # Configuración de Flask
├── config.py        # Configuración
└── services.py      # Lógica de negocio
```

## 🔧 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/IvanAusechaS/smart-horses-backend.git
cd smart-horses-backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Uso

### Desarrollo Local

```bash
# Modo desarrollo
python run.py

# El servidor estará disponible en http://localhost:5000
```

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests con cobertura
pytest --cov=smart_backend

# Tests específicos
pytest tests/test_heuristic.py -v
```

## 📚 Documentación

- **[MINIMAX_IMPLEMENTATION.md](MINIMAX_IMPLEMENTATION.md)**: Documentación técnica completa del algoritmo Minimax
- **[docs/report.md](docs/report.md)**: Informe detallado de la función heurística
- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Guía de despliegue
- **[CHANGELOG.md](CHANGELOG.md)**: Historial de cambios

## 🎯 Función Heurística

La evaluación de posiciones se basa en la siguiente fórmula:

```
H(s) = 100·ΔScore + 10·ΔMobility + 5·ΔProximity + 3·ΔCenter - 400·Trapped
```

### Factores de Evaluación

1. **ΔScore (peso: 100)**: Diferencia de puntuación
2. **ΔMobility (peso: 10)**: Diferencia en movimientos legales (con prevención de colisiones)
3. **ΔProximity (peso: 5)**: Proximidad a casillas valiosas
4. **ΔCenter (peso: 3)**: Control del centro del tablero
5. **Trapped (peso: -400)**: Penalización por no tener movimientos

## 🔄 Actualizaciones Recientes (Noviembre 2025)

### Prevención de Colisiones de Caballos

- Implementado sistema para evitar que ambos caballos ocupen la misma casilla
- Archivos actualizados:
  - `move_generator.py`: Acepta parámetro `opponent_position`
  - `game_state.py`: Pasa posición del oponente al generar movimientos
  - `heuristic.py`: Considera restricción en cálculo de movilidad

## 👥 Autores

- **Andrey Quiceno**
- **Ivan Ausecha**
- **Jonathan Aristizabal**
- **Jose Martínez**

**Universidad del Valle**  
**Asignatura:** Inteligencia Artificial  
**Fecha:** Noviembre 2025

## 📄 Licencia

Este proyecto está bajo la licencia especificada en [LICENSE](LICENSE).

## 🔗 Enlaces

- **Frontend**: https://github.com/IvanAusechaS/smart-horses-frontend
- **Backend**: https://github.com/IvanAusechaS/smart-horses-backend
