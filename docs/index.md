# Smart Horses - Guía de Sustentación

**Equipo:** Andrey Quiceno, Ivan Ausecha, Jonathan Aristizabal, Jose Martínez  
**Universidad del Valle** - Inteligencia Artificial

---

## 1. Introducción del Proyecto

### Objetivo

Implementar un juego estratégico de dos jugadores (Smart Horses) donde una IA basada en Minimax con poda Alpha-Beta compite contra un jugador humano.

### Descripción del Juego

- Juego de suma cero en tablero 8×8
- Dos caballos (knight de ajedrez) compiten por puntos
- Casillas visitadas se destruyen permanentemente
- Gana quien acumula más puntos

---

## 2. Reglas del Juego

### Elementos del Tablero

- **64 casillas** en total (8×8)
- **Exactamente 10 casillas con puntos:**
  - Valores: -10, -5, -4, -3, -1, +1, +3, +4, +5, +10
  - Uno de cada valor (sin repetición)
  - Ubicación aleatoria al inicio
- **2 caballos:** Blanco (máquina) y Negro (humano)
  - Posiciones iniciales aleatorias únicas
- **Resto:** Casillas vacías (0 puntos)

### Mecánica de Juego

- **Movimiento:** Patrón L del caballo (8 direcciones posibles)
- **Turnos:** Alternados, la máquina siempre inicia
- **Destrucción:** Cada casilla visitada se marca como destruida
- **Penalización:** -4 puntos si un jugador no tiene movimientos legales
- **Fin del juego:** Cuando ningún jugador puede moverse
- **Victoria:** Mayor puntuación final

---

## 3. Tecnologías Utilizadas

### Backend (Python)

- **Framework:** Flask 3.0.0
- **CORS:** Flask-CORS 4.0.0
- **Configuración:** python-dotenv 1.0.0
- **Servidor:** Gunicorn 21.2.0 (producción)
- **Testing:** pytest 9.0.1
- **Estructura:**
  ```
  smart_backend/
  ├── algorithms/      # Minimax y heurística
  ├── core/           # Lógica del juego
  ├── routes/         # API REST endpoints
  └── tests/          # 28 tests automatizados
  ```

### Frontend (React + Vite)

- **Framework:** React 18.2.0
- **Build Tool:** Vite 5.2.0
- **Estilos:** CSS puro
- **Gestión de Estado:** Context API
- **Componentes principales:**
  - ChessBoard: Tablero interactivo
  - DifficultySelector: Selector de nivel
  - ScorePanel: Marcador y estado
  - GameControls: Controles de juego

### Despliegue

- **Backend:** Compatible con Render/Heroku
- **Frontend:** Vercel/Netlify
- **Repositories:**
  - https://github.com/IvanAusechaS/smart-horses-backend
  - https://github.com/IvanAusechaS/smart-horses-frontend

---

## 4. Algoritmo Minimax

### Concepto

- **Tipo:** Búsqueda adversarial para juegos de suma cero
- **Objetivo:** Encontrar el mejor movimiento asumiendo juego óptimo del oponente
- **Implementación:** Recursiva con alternancia MAX/MIN

### Poda Alpha-Beta

- **Optimización** que elimina ramas innecesarias del árbol
- **Variables:**
  - α (alpha): Mejor valor garantizado para MAX
  - β (beta): Mejor valor garantizado para MIN
- **Condición de poda:** β ≤ α
- **Eficiencia:** Reduce nodos ~50-70%

### Niveles de Dificultad

| Nivel        | Profundidad | Nodos       | Tiempo   | Descripción                 |
| ------------ | ----------- | ----------- | -------- | --------------------------- |
| Principiante | 2           | 20-50       | <10ms    | Mira 2 movimientos adelante |
| Amateur      | 4           | 200-500     | 10-50ms  | Mira 4 movimientos adelante |
| Experto      | 6           | 2,000-5,000 | 50-200ms | Mira 6 movimientos adelante |

---

## 5. Función Heurística (Detalle Principal)

### Fórmula Completa

```
H(s) = w₁·ΔScore + w₂·ΔMobility + w₃·ΔProximity + w₄·ΔCenter + w₅·NTrapped
```

### Componentes y Pesos

#### 1. Diferencia de Puntos (w₁ = 100)

- **Cálculo:** (puntos_blanco - puntos_negro) × 100
- **Justificación:** Factor más importante - determina la victoria
- **Ejemplo:** Si blanco tiene 15 y negro 8 → 700 puntos

#### 2. Movilidad (w₂ = 10)

- **Cálculo:** (movimientos_blanco - movimientos_negro) × 10
- **Justificación:** Flexibilidad estratégica, evita trampas
- **Ejemplo:** 6 vs 4 movimientos → 20 puntos

#### 3. Proximidad a Casillas Valiosas (w₃ = 5)

- **Cálculo:** Σ(valor_casilla / distancia_Manhattan)
- **Justificación:** Posicionamiento para capturas futuras
- **Ejemplo:** Estar a distancia 3 de casilla +10 → +16.67 puntos

#### 4. Control del Centro (w₄ = 3)

- **Posiciones centro:** (3,3), (3,4), (4,3), (4,4)
- **Justificación:** Hasta 8 movimientos posibles vs 2-4 en bordes
- **Ejemplo:** Blanco en centro → +3 puntos

#### 5. Penalización por Trampa (w₅ = -400)

- **Cálculo:** -400 si sin movimientos, +400 si oponente sin movimientos
- **Justificación:** Evitar -4 puntos de penalización del juego
- **Ejemplo:** Quedar atrapado → -400 puntos

### Estados Terminales

- **Victoria blanco:** +10,000
- **Victoria negro:** -10,000
- **Empate:** 0

### Ejemplo Práctico

```
Posición:
  Blanco: 15 puntos, 6 movimientos, proximidad 10, en centro
  Negro: 8 puntos, 4 movimientos, proximidad 7, no centro

Cálculo:
  H(s) = 100(15-8) + 10(6-4) + 5(10-7) + 3(1-0) + 0
       = 700 + 20 + 15 + 3 + 0
       = 738

Interpretación: Ventaja fuerte para blanco
```

### Complejidad

- **Tiempo:** O(n + m) = O(1) en práctica (n≤10, m≤8)
- **Espacio:** O(1)

---

## 6. Validaciones Implementadas

### ✅ Pruebas Automatizadas (28 tests, 100% exitosos)

#### Generación de Casillas

- Exactamente 10 casillas con puntos
- Valores correctos: -10, -5, -4, -3, -1, +1, +3, +4, +5, +10
- Sin duplicación de valores

#### Posiciones Únicas

- Caballos en posiciones diferentes
- Caballos no inician en casillas con puntos
- Todas las posiciones especiales son únicas

#### Movimientos del Caballo

- Patrón L correcto (8 direcciones)
- Movimientos dentro del tablero
- Esquinas solo 2 movimientos

#### Destrucción de Casillas

- Casillas se marcan como destruidas
- No se pueden reutilizar
- Filtrado correcto en movimientos válidos

#### Penalizaciones

- -4 puntos aplicados correctamente
- Sin penalización cuando ambos atrapados

#### Configuración de Profundidad

- Principiante: profundidad 2
- Amateur: profundidad 4
- Experto: profundidad 6

#### Documentación

- Módulos con docstrings completos
- Funciones documentadas con ejemplos
- Fórmulas y complejidad especificadas

---

## 7. Demostración en Vivo

### Comandos para Ejecutar Localmente

#### Backend:

```bash
cd smart-horses-backend
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python run.py
# Servidor en http://localhost:5000
```

#### Frontend:

```bash
cd smart-horses-frontend
npm install
npm run dev
# Aplicación en http://localhost:5173
```

#### Tests:

```bash
cd smart-horses-backend
pytest tests/test_game_validations.py -v
# Resultado: 28 passed in 0.78s
```

### Flujo de Demostración

1. Iniciar backend y frontend
2. Seleccionar nivel de dificultad
3. Observar primer movimiento de la IA
4. Realizar movimiento del jugador
5. Ver movimiento de respuesta de la IA (con delay visual)
6. Mostrar puntuaciones en tiempo real
7. Jugar hasta final o reiniciar

---

## 8. Arquitectura del Sistema

### API REST Endpoints

#### `POST /api/game/new`

- Crea nuevo juego con dificultad seleccionada
- Retorna estado inicial con primer movimiento de IA

#### `POST /api/game/move`

- Procesa movimiento del jugador
- Calcula respuesta de IA con Minimax
- Retorna estado actualizado

#### `POST /api/game/valid-moves`

- Obtiene movimientos legales para un caballo
- Usado para mostrar casillas disponibles

#### `POST /api/game/machine-move`

- Obtiene siguiente movimiento de IA sin aplicarlo
- Útil para hints o análisis

### Flujo de Datos

```
Usuario hace clic → Frontend valida →
API recibe movimiento → Backend aplica →
Minimax calcula respuesta → API retorna estado →
Frontend actualiza UI con delay visual
```

---

## 9. Resultados y Logros

### Métricas de Calidad

- ✅ **28 tests automatizados** pasando (100%)
- ✅ **Documentación exhaustiva** (>300 líneas por módulo)
- ✅ **Rendimiento óptimo** (<200ms respuesta en experto)
- ✅ **Código limpio** con type hints y docstrings
- ✅ **Validaciones completas** según requerimientos

### Funcionalidades Destacadas

- Visualización clara de movimientos (delay configurable)
- Tres niveles de dificultad bien balanceados
- Interfaz intuitiva y responsiva
- Manejo robusto de errores
- Explicación detallada de decisiones de IA

### Documentación Entregada

- `report.tex` - Informe LaTeX profesional
- `report.md` - Versión Markdown
- `index.md` - Guía de sustentación (este archivo)
- `MINIMAX_IMPLEMENTATION.md` - Documentación técnica
- Tests documentados con propósito y validación

---

## 10. Conclusiones

### Objetivos Cumplidos

✅ Juego completamente funcional según especificaciones  
✅ IA competente con Minimax + Alpha-Beta  
✅ Heurística bien diseñada y justificada  
✅ Validaciones exhaustivas (28 tests)  
✅ Documentación profesional completa  
✅ Código limpio y mantenible  
✅ Rendimiento en tiempo real

### Aprendizajes Clave

- Diseño e implementación de funciones heurísticas
- Optimización con poda Alpha-Beta
- Balance entre complejidad y eficiencia
- Importancia de testing automatizado
- Documentación como parte integral del desarrollo

### Trabajo Futuro

- Tablas de transposición para cachear posiciones
- Ordenamiento de movimientos para mejor poda
- Pesos adaptativos según fase del juego
- Modo de análisis con explicación detallada
- Machine learning para ajustar heurística

---

## 11. Preguntas Frecuentes

### ¿Por qué exactamente 10 casillas con puntos?

Para mantener el juego balanceado y con duración razonable (~15-25 turnos).

### ¿Por qué estos valores específicos?

Rango simétrico (-10 a +10) que permite estrategia: perseguir positivos, evitar negativos.

### ¿Por qué profundidad máxima 6?

Balance entre fuerza de juego y tiempo de respuesta (<200ms).

### ¿Cómo se eligieron los pesos?

Análisis iterativo: puntos > movilidad > proximidad > centro, con testing empírico.

### ¿La IA siempre juega perfectamente?

Dentro de su profundidad de búsqueda, sí. Más allá puede ser sub-óptima (horizonte limitado).

---

## 12. Contacto y Enlaces

### Repositorios

- **Backend:** https://github.com/IvanAusechaS/smart-horses-backend
- **Frontend:** https://github.com/IvanAusechaS/smart-horses-frontend

### Equipo

- **Andrey Quiceno**
- **Ivan Ausecha**
- **Jonathan Aristizabal**
- **Jose Martínez**

### Institución

**Universidad del Valle**  
Facultad de Ingeniería  
Asignatura: Inteligencia Artificial  
Año: 2025

---

**¡Gracias por su atención!**

_Este proyecto demuestra la aplicación práctica de algoritmos de búsqueda adversarial y diseño de heurísticas en un entorno interactivo y educativo._
