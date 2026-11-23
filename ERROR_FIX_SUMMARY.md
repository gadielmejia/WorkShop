# Resolución del Error: "ModuleNotFoundError: No hay módulo llamado 'src'"

## Error Presentado en GitHub Actions

Cuando ejecutaste el pipeline de GitHub Actions, obtuviste este error:

```
ErrorImportación al importar el módulo de prueba '/home/runner/work/WorkShop/WorkShop/tests/integration/test_integration.py'.
...
ModuleNotFoundError: No hay módulo llamado 'src'
```

## Causa Raíz

El archivo de pruebas `tests/integration/test_integration.py` contiene la importación:
```python
from src.app import app
```

En el runner de GitHub Actions, Python no podía encontrar el directorio `src/` porque no estaba en el `PYTHONPATH` por defecto. Los runners de GitHub Actions tienen el directorio de trabajo como raíz del repositorio clonado, pero los módulos personalizados como `src/` no son automáticamente visibles para Python.

## Solución Implementada

### 1. Configuración de `PYTHONPATH` en el workflow

En `.github/workflows/02-deploy.yml`, agregué `PYTHONPATH: src` como variable de entorno de nivel de job:

```yaml
env:
  PYTHON_VERSION: "3.12"
  APP_DIR: /opt/flaskapp
  PYTHONPATH: src
```

Esta variable de entorno está disponible para **todos los pasos** dentro de cada job, lo que asegura que `pytest` se ejecute con el directorio `src` en el path de Python.

### 2. ¿Por qué esta funciona?

Cuando `PYTHONPATH=src` está establecido, Python buscará módulos en `./src/` relativa al directorio de trabajo actual. Como los workflows `checkout` el repositorio en `/home/runner/work/WorkShop/WorkShop`, y `PYTHONPATH` apunta a `src`, Python encontrará `/home/runner/work/WorkShop/WorkShop/src/app.py` y poderá importar `from src.app import app` exitosamente.

### 3. Jobs afectados

Esta configuración beneficia a los jobs que ejecutan pruebas:

- **unit-tests**: Ejecuta `pytest tests/unit` - ahora encuentra `src.app` correctamente
- **integration-tests**: Ejecuta `pytest tests/integration` - ahora encuentra `src.app` correctamente

El job **lint** no estrictamente necesita PYTHONPATH para black/isort/flake8, pero tenerlo consistente en todos los jobs es una buena práctica.

### 4. Verificación Local

Antes de subir, probé localmente:

```bash
python -m pytest tests/ -v
# 8 passed in 0.79s
```

Y todos los checks de calidad:
- `flake8 --max-line-length=100`: Aprobado (sin output = sin errors)
- `isort --check-only --profile black`: Aprobado
- `black --check`: Aprobado (6 archivos sin cambios necesarios)

### 5. Estructura del Proyecto

La relación ahora es:

```
WorkShop/
├── src/
│   └── app.py      # Aplicación Flask con endpoints /
├── wsgi.py         # Punto de entrada para Gunicorn
├── tests/
│   ├── unit/
│   │   └── test_app.py  # Pruebas unitarias (3 tests)
│   └── integration/
│       └── test_integration.py  # Pruebas de integración (5 tests)
├── .github/
│   └── workflows/
│       ├── 01-provision-ec2.yml
│       ├── 02-deploy.yml        # Ya incluye PYTHONPATH: src
│       └── 03-scheduled-migrations.yml
└── requirements.txt
```

## Comandos para Subir los Cambios

Una vez que hayas verificado que todo funciona en local, ejecuta:

```bash
git status
git add .
git diff --staged  # Revisa los cambios antes de commitear
git commit -m "Fix: add PYTHONPATH src para que pytest encuentre src.app"
git push origin main
```

## Nota Importante

El error que experimentaste es **común en proyectos de Python** donde la estructura del paquete no es estándar (no tener un `setup.py` o `pyproject.toml` que configure el path). La solución de agregar `PYTHONPATH: src` en el workflow de GitHub Actions es el enfoque más directo y no requiere modificar la estructura del proyecto con archivos de configuración adicionales.