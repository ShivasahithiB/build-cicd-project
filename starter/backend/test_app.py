from . import app
import os


def test_movies_endpoint_returns_200():
    with app.test_client() as client:
        status_code = os.getenv("FAIL_TEST", 200)
        response = client.get("/movies/")
        assert response.status_code == int(status_code)


def test_movies_endpoint_returns_json():
    with app.test_client() as client:
        response = client.get("/movies/")
        assert response.content_type == "application/json"


def test_movies_endpoint_returns_valid_data():
    with app.test_client() as client:
        response = client.get("/movies/")
        data = response.get_json()

        assert isinstance(data, dict)
        assert "movies" in data
        assert isinstance(data["movies"], list)
        assert len(data["movies"]) > 0
        assert "title" in data["movies"][0]


def test_get_single_movie():
    with app.test_client() as client:
        response = client.get("/movies/123")

        assert response.status_code == 200

        data = response.get_json()

        assert "movie" in data
        assert data["movie"]["title"] == "Top Gun: Maverick"


def test_post_movie():
    with app.test_client() as client:
        response = client.post(
            "/movies",
            json={
                "title": "Interstellar",
                "description": "Space adventure"
            }
        )

        assert response.status_code == 201

        data = response.get_json()

        assert "id" in data
        assert data["movie"]["title"] == "Interstellar"
        assert data["movie"]["description"] == "Space adventure"


def test_post_movie_invalid_data():
    with app.test_client() as client:
        response = client.post(
            "/movies",
            json={
                "title": "Incomplete Movie"
            }
        )

        assert response.status_code == 400


def test_put_movie():
    with app.test_client() as client:
        response = client.put(
            "/movies/456",
            json={
                "title": "Sonic Updated",
                "description": "Updated blue character"
            }
        )

        assert response.status_code == 200

        data = response.get_json()

        assert data["id"] == "456"
        assert data["movie"]["title"] == "Sonic Updated"
        assert data["movie"]["description"] == "Updated blue character"


def test_put_movie_not_found():
    with app.test_client() as client:
        response = client.put(
            "/movies/9999",
            json={
                "title": "Unknown",
                "description": "Unknown movie"
            }
        )

        assert response.status_code == 404


def test_delete_movie():
    with app.test_client() as client:
        response = client.delete("/movies/789")

        assert response.status_code == 200

        data = response.get_json()

        assert data["message"] == "Movie deleted successfully"

        response = client.get("/movies/789")

        assert response.status_code == 404


def test_delete_movie_not_found():
    with app.test_client() as client:
        response = client.delete("/movies/9999")

        assert response.status_code == 404
