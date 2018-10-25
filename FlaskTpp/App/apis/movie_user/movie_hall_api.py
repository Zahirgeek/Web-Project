# 用户选择影院和电影界面
import datetime

from flask_restful import Resource, reqparse, fields, marshal
from sqlalchemy import or_

from App.apis.api_contant import HTTP_OK
from App.apis.movie_user.utils import login_required
from App.models.cinema_admin.cinema_address_model import CinemaAddress
from App.models.cinema_admin.cinema_hall_model import Hall
from App.models.cinema_admin.cinema_hall_movie_model import HallMovie
from App.models.movie_user.movie_order_model import MovieOrder, ORDER_STATUS_PAYED_NOT_GET, ORDER_STATUS_GET,ORDER_STATUS_NOT_PAY

parse = reqparse.RequestParser()
parse.add_argument("address_id")
parse.add_argument("district")
parse.add_argument("movie_id")

hall_movie_fields = {
    "id": fields.Integer,
    "h_movie_id": fields.Integer,
    "h_hall_id": fields.Integer,
    "h_time": fields.DateTime,
}

multi_hall_movie_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(hall_movie_fields)),
}


class UserMovieHallsResource(Resource):

    def get(self):
        args = parse.parse_args()

        address_id = args.get("address_id")
        district = args.get("district")
        movie_id = args.get("movie_id")

        cinema_address = CinemaAddress.query.filter(CinemaAddress.district == district).filter(CinemaAddress.id == address_id)

        halls = Hall.query.filter_by(h_address_id=cinema_address.id).all()

        all_hall_movies = []

        for hall in halls:

            hall_movies = HallMovie.query.filter_by(h_hall_id=hall.id).filter_by(h_movie_id=movie_id).all()
            all_hall_movies += hall_movies

        data = {
            "msg": "ok",
            "status": HTTP_OK,
            "data": all_hall_movies,
        }

        return marshal(data, multi_hall_movie_fields)


hall_fields = {
    "h_address_id": fields.Integer,
    "h_num": fields.Integer,
    "h_seats": fields.String,
}


class UserMovieHallResource(Resource):

    # 返回影厅,可选座位表
    @login_required
    def get(self, id):
        # 排挡
        hall_movie = HallMovie.query.get(id)
        # 影厅
        hall = Hall.query.get(hall_movie.h_hall_id)

        # 已完成支付
        '''
        1. 在订单表中通过id找到排挡
        2. 再筛选找到状态是已支付未取票和已取票的订单
        '''
        movie_orders_buyed = MovieOrder.query.filter(MovieOrder.o_hall_movie_id == id).filter(or_(MovieOrder.o_status == ORDER_STATUS_PAYED_NOT_GET, MovieOrder.o_status == ORDER_STATUS_GET)).all()

        # 订单未付款未超时
        '''
        1. 找到未付款的订单
        2. 再筛选找到截止时间未过的订单
        '''
        movie_orders_lock = MovieOrder.query.filter(MovieOrder.o_status == ORDER_STATUS_NOT_PAY).filter(MovieOrder.o_time > datetime.datetime.now()).all()

        seats = []

        for movie_orders in movie_orders_buyed:

            sold_seats = movie_orders.o_seats.split("#")
            seats += sold_seats

        for movie_orders in movie_orders_lock:
            sold_seats = movie_orders.o_seats.split("#")
            seats += sold_seats

        all_seats = hall.h_seats.split("#")

        # 可买的座位
        can_buy = list(set(all_seats) - set(seats))

        hall.h_seats = "#".join(can_buy)

        data = {
            "msg": "ok",
            "status": HTTP_OK,
            "data": marshal(hall, hall_fields),
        }

        return data
