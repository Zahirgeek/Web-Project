# 影院电影管理
from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.api_contant import HTTP_OK
from App.apis.cinema_admin.utils import login_required
from App.models.cinema_admin.cinema_movie_model import CinemaMovie
from App.models.common.movie_model import Movie

parse = reqparse.RequestParser()
parse.add_argument("movie_id", required=True, help="请选择需要购买的电影")

movie_fields = {
    "showname": fields.String,
    "shownameen": fields.String,
    "director": fields.String,
    "leadingRole": fields.String,
    "type": fields.String,
    "country": fields.String,
    "language": fields.String,
    "duration": fields.Integer,
    "screeningmodel": fields.String,
    "openday": fields.DateTime,
    "backgroundpicture": fields.String,
}

multi_movies_fields = {
    "status": fields.Integer,
    "msg": fields.String,
    "data": fields.List(fields.Nested(movie_fields)),
}


class CinemaMoviesResource(Resource):

    # 得到影院所有购买的电影
    @login_required
    def get(self):

        user_id = g.user.id
        cinema_movies = CinemaMovie.query.filter(CinemaMovie.c_cinema_id==user_id).all()

        movies = []

        for cinema_movie in cinema_movies:
            movies.append(Movie.query.get(cinema_movie.c_movie_id))

        data = {
            "msg": "ok",
            "status": HTTP_OK,
            "data": movies,
        }

        return marshal(movies, multi_movies_fields)

    # 购买电影
    @login_required
    def post(self):

        user_id = g.user.id

        args = parse.parse_args()

        movie_id = args.get("movie_id")

        cinema_movies = CinemaMovie.query.filter(CinemaMovie.c_cinema_id==user_id).filter(CinemaMovie.c_movie_id==movie_id).all()

        if cinema_movies:
            abort(400, msg="已经购买了此电影,无需重复购买")

        cinema_movie = CinemaMovie()
        cinema_movie.c_movie_id = movie_id
        cinema_movie.c_cinema_id = user_id

        data = {
            "msg": "购买成功",
            "status": HTTP_OK,
        }

        return data