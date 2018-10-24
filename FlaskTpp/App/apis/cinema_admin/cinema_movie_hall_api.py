# 排挡
from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.api_contant import HTTP_CREATE_OK
from App.apis.cinema_admin.utils import login_required
from App.models.cinema_admin.cinema_address_model import CinemaAddress
from App.models.cinema_admin.cinema_hall_movie_model import HallMovie
from App.models.cinema_admin.cinema_movie_model import CinemaMovie
from App.models.cinema_admin.cinema_hall_model import Hall

parse = reqparse.RequestParser()
parse.add_argument("movie_id", required=True, help="请选择电影")
parse.add_argument("hall_id", required=True, help="请选择大厅")
parse.add_argument("h_time", required=True, help="请选择排挡时间")

hall_movie_fields = {
    "h_movie_id": fields.Integer,
    "h_hall_id": fields.Integer,
    "h_time": fields.DateTime,
}


class CinemaMovieHallsResource(Resource):

    def get(self):
        return {"msg": "ok"}

    # 添加排挡
    @login_required
    def post(self):

        args = parse.parse_args()

        movie_id = args.get("movie_id")
        hall_id = args.get("hall_id")
        h_time = args.get("h_time")

        # 验证 movie_id是否已经购买
        # 验证 hall_id是否是该用户
        # 同时间同影厅是否有不同排挡

        # 查找到所选影院所有电影id
        cinema_movies = CinemaMovie.query.filter_by(c_cinema_id=g.user.id).all()
        movie_ids = [cinema_movie.c_movie_id for cinema_movie in cinema_movies]

        # 判断影院是否购买该电影
        if not movie_id in movie_ids:
            abort(403, msg="电影未被授权")

        cinema_addresses = CinemaAddress.query.filter_by(c_user_id=g.user.id)

        all_halls = []

        # 遍历影院的所有影厅
        for cinema_address in cinema_addresses:
            halls = Hall.query.filter_by(h_address_id=cinema_address.id).all()
            all_halls.append(halls)

        all_halls_ids = [hall.id for hall in all_halls]

        if not hall_id in all_halls_ids:
            abort(403, msg="大厅选择错误")

        hall_movie = HallMovie()
        hall_movie.h_movie_id = movie_id
        hall_movie.hall_id = hall_id
        hall_movie.h_time = h_time

        if not hall_movie.save():
            abort(400, msg="排挡失败")

        data = {
            "status": HTTP_CREATE_OK,
            "msg": "ok",
            "data": marshal(hall_movie, hall_movie_fields)
        }

        return data