import pytest


@pytest.fixture
def client():
    """Crea un cliente de prueba para la aplicación Flask."""
    try:
        from app import app
    except ImportError:
        from src.app import app

    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client


def test_home_returns_success(client):
    response = client.get("/")

    assert response.status_code == 200


def test_home_returns_html(client):
    response = client.get("/")

    assert response.content_type.startswith("text/html")


def test_unknown_route_returns_not_found(client):
    response = client.get("/ruta-que-no-existe")

    assert response.status_code == 404
