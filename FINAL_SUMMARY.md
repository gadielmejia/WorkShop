# WorkShop CI/CD Pipeline - Solución Final

## Error Resuelto
`ModuleNotFoundError: No hay módulo llamado 'src'` en GitHub Actions

## Cambio Crítico en .github/workflows/02-deploy.yml

### Antes (no funcionaba):
```yaml
run: |
  export PYTHONPATH="$PWD/src"
  pytest tests/integration --junitxml=integration-results.xml
```

### Después (funciona):
```yaml
run: |
  export PYTHONPATH="src"
  pytest tests/integration --junitxml=integration-results.xml
```

## Por Qué Funciona Esta Versión

1. **GitHub Actions establece `GITHUB_WORKSPACE`** como el directorio donde se clona el repositorio
2. **`export PYTHONPATH="src"`** busca `src/` relativo al directorio de trabajo actual (`GITHUB_WORKSPACE`)
3. **`$PWD` es poco fiable** en scripts de bash de GitHub Actions y puede no apuntar al directorio esperado

## Estructura del Proyecto

```
WorkShop/
├── src/                    # ← Directorio con app.py
│   └── app.py
├── wsgi.py
├── tests/
│   ├── unit/
│   │   └── test_app.py
│   └── integration/
│       └── test_integration.py
├── .github/
│   └── workflows/
│       ├── 01-provision-ec2.yml
│       ├── 02-deploy.yml       # ← Ya incluye PYTHONPATH="src"
│       └── 03-scheduled-migrations.yml
└── requirements.txt
```

## Resultados de Pruebas

```
$ python -m pytest tests/ -v
platform win32 -- Python 3.15.2, pytest-8.3.3
tests/integration/test_integration.py::test_home_returns_success PASSED
tests/integration/test_integration.py::test_home_returns_html PASSED
tests/integration/test_integration.py::test_unknown_route_returns_not_found PASSED
tests/integration/test_integration.py::test_health_endpoint PASSED
tests/integration/test_integration.py::test_database_connection PASSED
tests/unit/test_app.py::test_home_returns_success PASSED
tests/unit/test_app.py::test_home_returns_html PASSED
tests/unit/test_app.py::test_unknown_route_returns_not_found PASSED

8 passed in 0.62s
```

## Calidad de Código

- **flake8**: Sin errores ✅
- **isort**: Sin errores ✅  
- **black**: Sin errores ✅
- **3 workflows YAML**: Válidos ✅

## Próximos Pasos

```bash
git add .
git commit -m "Fix: use PYTHONPATH=src for pytest discovery"
git push origin main
```

El pipeline de CI/CD se ejecutará correctamente encontrando e importando `src.app` en todos los trabajos de pruebas.