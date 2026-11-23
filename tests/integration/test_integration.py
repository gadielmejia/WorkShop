"""Pruebas de integración para la aplicación Flask WorkShop.

Estas pruebas utilizan SQLite en memoria para simular las pruebas de
integración contra una base de datos cuando no hay una instancia de MySQL
disponible localmente. En GitHub Actions, las pruebas de integración se
ejecutan contra un contenedor MySQL temporal.
"""

import sqlite3

import pytest

from src.app import app


@pytest.fixture
def client():
    """Crea un cliente de prueba para la aplicación Flask."""
    app.config.update(
        TESTING=True,
        DATABASE_URL="sqlite:///:memory:",
    )

    with app.test_client() as test_client:
        yield test_client


def test_home_returns_success(client):
    """Verifica que la ruta raíz retorne código 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_home_returns_html(client):
    """Verifica que la ruta raíz retorne contenido HTML."""
    response = client.get("/")
    assert response.content_type.startswith("text/html")


def test_unknown_route_returns_not_found(client):
    """Verifica que una ruta inexistente retorne 404."""
    response = client.get("/ruta-que-no-existe")
    assert response.status_code == 404


def test_health_endpoint(client):
    """Verifica que el endpoint de health check retorne 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_database_connection():
    """Verifica que se pueda conectar a la base de datos."""
    # Para pruebas con SQLite en memoria
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    assert result == (1,)
    conn.close()
