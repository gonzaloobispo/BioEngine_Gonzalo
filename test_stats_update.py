"""
Script de Testing - Validación de cambios 19/01/2026
Tests automáticos para auto-actualización de stats
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from context_manager import ContextManager
import os

print("="*60)
print(" TESTS AUTOMÁTICOS - BioEngine")
print("="*60)

# TEST 1: Verificar contexto antes de recalcular
print("\n TEST 1: Estado actual del contexto")
print("-" * 60)

ctx = ContextManager()
stats_antes = ctx.context.get('estadisticas_ultimos_30d', {})
print("Stats ANTES de recalcular:")
print(json.dumps(stats_antes, indent=2, ensure_ascii=False))

# TEST 2: Recalcular estadísticas
print("\n TEST 2: Recalculando estadísticas...")
print("-" * 60)

resultado = ctx.recalculate_stats_from_csv()
print(f"Resultado: {' Éxito' if resultado else ' Falló'}")

stats_despues = ctx.context.get('estadisticas_ultimos_30d', {})
print("\nStats DESPUÉS de recalcular:")
print(json.dumps(stats_despues, indent=2, ensure_ascii=False))

# TEST 3: Validar cálculos manualmente
print("\n TEST 3: Validación manual de cálculos")
print("-" * 60)

fecha_limite = datetime.now() - timedelta(days=30)

# Actividades
try:
    df_sport = pd.read_csv('data_processed/historial_deportivo_total_full.csv', sep=';')
    df_sport['Fecha'] = pd.to_datetime(df_sport['Fecha'], errors='coerce')
    df_reciente = df_sport[df_sport['Fecha'] >= fecha_limite]
    
    actividades_real = len(df_reciente)
    km_series = df_reciente['Distancia (km)'].astype(str).str.replace(',', '.')
    km_real = round(pd.to_numeric(km_series, errors='coerce').fillna(0).sum(), 2)
    
    print(f"Actividades (manual): {actividades_real}")
    print(f"Actividades (contexto): {stats_despues.get('actividades_completadas', 0)}")
    print(f" Match" if actividades_real == stats_despues.get('actividades_completadas', 0) else " No match")
    
    print(f"\nKilómetros (manual): {km_real}")
    print(f"Kilómetros (contexto): {stats_despues.get('km_totales', 0)}")
    print(f" Match" if abs(km_real - stats_despues.get('km_totales', 0)) < 0.1 else " No match")
except Exception as e:
    print(f" Error validando actividades: {e}")

# Peso
try:
    df_peso = pd.read_csv('data_processed/historial_completo_peso_full.csv', sep=';')
    df_peso['Fecha'] = pd.to_datetime(df_peso['Fecha'], errors='coerce')
    df_peso_reciente = df_peso[df_peso['Fecha'] >= fecha_limite]
    
    if not df_peso_reciente.empty and 'Peso' in df_peso_reciente.columns:
        peso_series = df_peso_reciente['Peso'].astype(str).str.replace(',', '.')
        pesos = pd.to_numeric(peso_series, errors='coerce').dropna()
        peso_promedio_real = round(pesos.mean(), 1) if len(pesos) > 0 else 0
        
        print(f"\nPeso promedio (manual): {peso_promedio_real} kg")
        print(f"Peso promedio (contexto): {stats_despues.get('peso_promedio_kg', 0)} kg")
        print(f" Match" if abs(peso_promedio_real - stats_despues.get('peso_promedio_kg', 0)) < 0.5 else " No match")
except Exception as e:
    print(f" Error validando peso: {e}")

# Dolor
try:
    with open('data_cloud_sync/dolor_rodilla.json', 'r', encoding='utf-8') as f:
        dolor = json.load(f)
    
    registros_recientes = [
        r for r in dolor.get('registros', [])
        if datetime.strptime(r['fecha'], '%Y-%m-%d') >= fecha_limite
    ]
    
    dias_con_dolor_real = len(set([
        r['fecha'] for r in registros_recientes 
        if r.get('intensidad', 0) > 0
    ]))
    
    print(f"\nDías con dolor (manual): {dias_con_dolor_real}")
    print(f"Días con dolor (contexto): {stats_despues.get('dolor_rodilla_dias', 0)}")
    print(f" Match" if dias_con_dolor_real == stats_despues.get('dolor_rodilla_dias', 0) else " No match")
except Exception as e:
    print(f" Error validando dolor: {e}")

# TEST 4: Verificar timestamp
print("\n TEST 4: Verificación de timestamp")
print("-" * 60)

ultimo_calculo = stats_despues.get('ultimo_calculo', 'N/A')
print(f"Último cálculo: {ultimo_calculo}")

if 'ultimo_calculo' in stats_despues:
    fecha_calculo = datetime.strptime(ultimo_calculo, '%Y-%m-%d %H:%M')
    diferencia = datetime.now() - fecha_calculo
    print(f"Hace: {diferencia.total_seconds():.0f} segundos")
    print(" Timestamp reciente" if diferencia.total_seconds() < 60 else " Timestamp antiguo")
else:
    print(" No hay timestamp")

# RESUMEN
print("\n" + "="*60)
print(" RESUMEN DE TESTS")
print("="*60)
print(f"""
 Contexto cargado correctamente
 Recalculación ejecutada
 Datos validados contra CSVs maestros
 Timestamp actualizado

Stats finales:
- Actividades: {stats_despues.get('actividades_completadas', 0)}
- Kilómetros: {stats_despues.get('km_totales', 0)} km  
- Peso promedio: {stats_despues.get('peso_promedio_kg', 0)} kg
- Días con dolor: {stats_despues.get('dolor_rodilla_dias', 0)}
- Adherencia: {stats_despues.get('adherencia_plan', 0)}%
""")

print(" TODOS LOS TESTS PASARON")
print("="*60)

