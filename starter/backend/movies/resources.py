from flask import jsonify, request
from flask.views import MethodView


movies = {
    "123": {
        "title": "Top Gun: Maverick",
        "description": "Fighter planes"
    },
    "456": {
        "title": "Sonic the Hedgehog",
        "description": "Blue Sega character"
    },
    "789": {
        "title": "A Quiet Place",
        "description": "Scary monsters"
    }
}


class Movies(MethodView):

    def get(self, movie_id):
        if movie_id is None:
            return jsonify({
                "movies": [
                    dict(
                        {"title": movie["title"]},
                        **{"id": i}
                    )
                    for i, movie in movies.items()
                ]
            })

        movie = movies.get(str(movie_id))

        if movie is None:
            return jsonify({"error": "Movie not found"}), 404

        return jsonify({"movie": movie})

    def post(self):
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        if "title" not in data or "description" not in data:
            return jsonify({
                "error": "title and description are required"
            }), 400

        new_id = str(max(map(int, movies.keys())) + 1)

        movies[new_id] = {
            "title": data["title"],
            "description": data["description"]
        }

        return jsonify({
            "id": new_id,
            "movie": movies[new_id]
        }), 201

    def put(self, movie_id):
        movie_id = str(movie_id)

        if movie_id not in movies:
            return jsonify({"error": "Movie not found"}), 404

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        if "title" not in data or "description" not in data:
            return jsonify({
                "error": "title and description are required"
            }), 400

        movies[movie_id] = {
            "title": data["title"],
            "description": data["description"]
        }

        return jsonify({
            "id": movie_id,
            "movie": movies[movie_id]
        }), 200

    def delete(self, movie_id):
        movie_id = str(movie_id)

        if movie_id not in movies:
            return jsonify({"error": "Movie not found"}), 404

        deleted_movie = movies.pop(movie_id)

        return jsonify({
            "message": "Movie deleted successfully",
            "movie": deleted_movie
        }), 200
