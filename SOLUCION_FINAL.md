# Solución Final - Error ModuleNotFoundError en GitHub Actions

## Problema
`ModuleNotFoundError: No hay módulo llamado 'src'` al ejecutar pytest en GitHub Actions.

## Causa
Python no encontraba el directorio `src/` porque no estaba en `sys.path` por defecto en el runner de GitHub Actions.

## Solución Tríplice

### 1. `tests/conftest.py` (archivo nuevo)
Archivo estándar de pytest que se ejecuta al inicio de las pruebas y agrega el directorio `src` a `sys.path`:
```python
import sys
import os

# Add src directory to Python path
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, os.path.abspath(src_path))
```

### 2. `export PYTHONPATH="src"` en workflow
```yaml
- name: Ejecutar pruebas unitarias
  run: |
    export PYTHONPATH="src"
    pytest tests/unit --cov=. --cov-report=xml --junitxml=unit-results.xml

- name: Ejecutar pruebas de integración
  run: |
    export PYTHONPATH="src"
    pytest tests/integration --junitxml=integration-results.xml
```

### 3. Resultados
```
$ python -m pytest tests/ -v
8 passed in ~1s
```

### Archivos Afectados
- `tests/conftest.py` (nuevo)
- `src/app.py` (nuevo)
- `wsgi.py` (nuevo)
- `.github/workflows/02-deploy.yml` (modificado)
- `requirements.txt` (modificado)

### Comando Git
```bash
git add .
git commit -m "Fix: add conftest.py and PYTHONPATH for pytest"
git push origin main
```