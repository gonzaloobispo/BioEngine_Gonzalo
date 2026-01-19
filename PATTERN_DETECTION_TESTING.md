# 🧪 Test de Detección de Patrones

Este archivo documenta cómo testear el sistema de detección de patrones.

## Sistema Implementado

✅ **Detectores activos:**
1. **Correlación Actividad-Dolor** - Encuentra qué actividades resultan en menos dolor
2. **Adherencia por Tipo** - Identifica actividades con alta/baja adherencia

## Cómo Funciona

### Ejecución Automática:
- Se ejecuta **cada vez que sincronizas** (botón "Sincronizar")
- Analiza últimos 60 días de datos
- Requiere mínimo 10 observaciones para calcular correlación
- Solo guarda insights con confianza > 75%

### Datos Necesarios:
- CSV de actividades: `data_processed/historial_deportivo_total_full.csv`
- JSON de dolor: `data_cloud_sync/dolor_rodilla.json`
- Plan de entrenamiento: `config/plan_entrenamiento.json`

## Tests Manuales

### Test 1: Ejecutar detector standalone
```bash
python pattern_detector.py
```

**Resultado esperado:**
- Mensaje: "Analizando patrones..."
- Lista de patrones encontrados (puede ser 0 si no hay suficientes datos)
- Cada patrón muestra: descripción, confianza %, recomendación

### Test 2: Verificar integración con sincronización
```bash
# Opción 1: Desde Python
python cloud_sync.py

# Opción 2: Desde dashboard
streamlit run dashboard.py
# → Presionar botón "Sincronizar"
```

**Resultado esperado:**
- Mensaje: "Detectando patrones..."
- Si encuentra patrones: "X patrones encontrados"
- Si guarda insights: "Y nuevos insights guardados"

### Test 3: Verificar insights guardados
```bash
# Ver archivo de contexto
cat data_cloud_sync/user_context.json
# O abrirlo en editor
```

**Buscar sección:**
```json
"insights_aprendidos": [
  {
    "patron": "...",
    "accion": "...",
    "confianza": 85
  }
]
```

## Escenarios de Prueba

### Escenario A: Datos Insuficientes
- **Situación:** Menos de 10 actividades o sin registros de dolor
- **Resultado:** 0 patrones detectados
- **Mensaje:** "No se detectaron patrones nuevos"

### Escenario B: Patrón Detectado
- **Situación:** 10+ sesiones de ciclismo con dolor registrado bajo
- **Resultado:** Patrón "Ciclismo → Dolor bajo (XX%)"
- **Guardado en:** `user_context.json` → `insights_aprendidos`

### Escenario C: Baja Adherencia
- **Situación:** Plan indica 4 sesiones/semana pero solo se hacen 1-2
- **Resultado:** Patrón de baja adherencia detectado
- **Recomendación:** "Considerar reemplazar [actividad] por otra"

## Ejemplos de Insights

### Insight Tipo 1: Actividad-Dolor
```json
{
  "patron": "Ciclismo → Dolor bajo (92% de las veces)",
  "accion": "Priorizar Ciclismo cuando hay dolor alto",
  "confianza": 92
}
```

### Insight Tipo 2: Alta Adherencia
```json
{
  "patron": "Alta adherencia a Ciclismo (85%)",
  "accion": "Mantener Ciclismo en el plan - buena adherencia",
  "confianza": 85
}
```

### Insight Tipo 3: Baja Adherencia
```json
{
  "patron": "Baja adherencia a Fuerza (30%)",
  "accion": "Considerar reemplazar Fuerza por otra actividad",
  "confianza": 70
}
```

## Solución de Problemas

### No detecta patrones
**Causas posibles:**
1. Menos de 10 actividades en últimos 60 días
2. Sin registros de dolor
3. Correlación < 75%

**Solución:**
- Agregar más registros de dolor vía chat
- Esperar acumular más actividades
- Verificar que archivos CSV/JSON existen

### Patrones duplicados
**Causa:** El sistema ya detectó ese patrón antes

**Solución:** Sistema verifica automáticamente y no guarda duplicados

### Error al ejecutar
**Verifica:**
- Archivos CSV tienen datos válidos
- JSON de dolor tiene formato correcto
- Permisos de lectura/escritura

## Mejoras Futuras (Opcional)

- ✅ Correlación peso-carga
- ✅ Patrones de recuperación
- ✅ Detección de ventanas óptimas de entrenamiento
- ✅ ML avanzado con scikit-learn

---

**Estado:** ✅ Implementado y funcionando  
**Última revisión:** 19/01/2026 03:00 AM
