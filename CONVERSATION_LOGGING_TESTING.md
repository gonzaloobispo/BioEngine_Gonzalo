# 🧪 Test de Conversation Logging

## Sistema Implementado

✅ **Conversaciones guardadas automáticamente cuando:**
1. Usuario modifica el plan ("pon ciclismo hoy")
2. Usuario reporta estado de rodilla
3. Usuario hace consulta personalizada (recomienda, debería, consejo, etc.)
4. Asistente detecta patrones o correlaciones

## Estructura de Datos

### Guardado en `user_context.json`:
```json
"conversaciones_relevantes": [
  {
    "fecha": "2026-01-19",
    "aprendizaje": "Usuario solicitó cambio de plan: pon ciclismo...",
    "contexto": "Resumen de la respuesta del asistente..."
  }
]
```

### Límite:
- Máximo 20 conversaciones almacenadas
- Se mantienen las más recientes

## Tests Manuales

### Test 1: Modificación de Plan
**Acción:**
1. Abrir dashboard (`streamlit run dashboard.py`)
2. En el chat escribir: "Pon ciclismo hoy"

**Resultado esperado:**
- ✅ Plan se modifica
- ✅ Mensaje en consola: `[CONV] Conversación importante guardada: Usuario solicitó cambio de plan...`
- ✅ En `user_context.json` → nuevo registro en `conversaciones_relevantes`

---

### Test 2: Reporte de Dolor
**Acción:**
1. En el chat escribir: "Siento la rodilla bien hoy"

**Resultado esperado:**
- ✅ Dolor registrado (0/10)
- ✅ Conversación guardada: "Usuario reportó estado de rodilla"

---

### Test 3: Consulta Personalizada
**Acción:**
1. Escribir: "¿Qué me recomiendas para mañana?"

**Resultado esperado:**
- ✅ Asistente responde con recomendación
- ✅ Si respuesta > 100 chars → Conversación guardada
- ✅ Aprendizaje: "Consulta personalizada: ¿Qué me recomiendas..."

---

### Test 4: Verificar Contexto
**Acción:**
```bash
# Ver archivo
cat data_cloud_sync/user_context.json
# O abrirlo en editor
```

**Buscar:**
```json
"conversaciones_relevantes": [
  {
    "fecha": "2026-01-19",
    "aprendizaje": "...",
    "contexto": "..."
  }
]
```

**Verificar:**
- ✅ Conversaciones recientes aparecen
- ✅ Máximo 20 conversaciones
- ✅ Fechas correctas

---

## Criterios de Importancia

### SÍ se guarda:
- ✅ "Pon ciclismo hoy" (modificación plan)
- ✅ "Rodilla bien" (reporte médico)
- ✅ "¿Qué me recomiendas?" (consulta personalizada)
- ✅ Respuestas que mencionan "patrón" o "correlación"

### NO se guarda:
- ❌ "Hola" (saludo simple)
- ❌ "Ok, gracias" (agradecimiento)
- ❌ Conversaciones genéricas muy cortas
- ❌ Respuestas < 100 caracteres en consultas

---

## Integración con LLM

Las conversaciones guardadas se incluyen en el contexto del LLM:

```python
# En ContextManager.get_formatted_context_for_llm()
conversaciones = context.get('conversaciones_relevantes', [])[-3:]
# Últimas 3 conversaciones se pasan al prompt
```

Esto permite que el asistente:
- 🧠 Recuerde conversaciones anteriores
- 💡 Haga referencias a temas previos
- 📈 Mejore la personalización con el tiempo

---

## Solución de Problemas

### No se guardan conversaciones
**Verifica:**
1. Archivo `user_context.json` existe
2. Permisos de escritura en `data_cloud_sync/`
3. Consola muestra `[CONV]` al chatear

### Conversaciones duplicadas
**Causa:** Sistema guarda cada interacción importante
**Solución:** Esto es normal, máximo 20 se mantienen

### Error al guardar
**Verifica consola:** `[WARNING] Error guardando conversacion: ...`
**Acción:** Revisar permisos de archivos

---

## Próximos Pasos (Opcional)

**Mejoras futuras:**
- ✅ Clasificación automática de conversaciones (médico, plan, técnica)
- ✅ Búsqueda de conversaciones por palabra clave
- ✅ Exportar historial de conversaciones
- ✅ Análisis de tendencias en consultas

---

**Estado:** ✅ Implementado y funcionando  
**Última revisión:** 19/01/2026 03:15 AM
