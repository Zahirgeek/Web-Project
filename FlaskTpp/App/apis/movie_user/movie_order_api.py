# 订单
import datetime
from operator import or_

from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.api_contant import HTTP_CREATE_OK
from App.apis.movie_user.utils import login_required, require_permission
from App.models.cinema_admin.cinema_hall_model import Hall
from App.models.cinema_admin.cinema_hall_movie_model import HallMovie
from App.models.movie_user.movie_order_model import MovieOrder, ORDER_STATUS_PAYED_NOT_GET, ORDER_STATUS_GET,ORDER_STATUS_NOT_PAY
from App.models.movie_user.movie_user_model import VIP_USER

parse = reqparse.RequestParser()
parse.add_argument("hall_movie_id", required=True, help="请提供排挡信息")
parse.add_argument("o_seats", required=True, help="请正确选择座位")

movie_order_fields = {
    "o_price": fields.Float,
    "o_seats": fields.String,
    "o_hall_movie_id": fields.Integer,
}


class MovieOrdersResource(Resource):

    @login_required
    def post(self):

        args = parse.parse_args()

        hall_movie_id = args.get("hall_movie_id")

        o_seats = args.get("o_seats")

        # 已完成支付
        movie_orders_buyed = MovieOrder.query.filter(MovieOrder.o_hall_movie_id == hall_movie_id).filter(or_(MovieOrder.o_status == ORDER_STATUS_PAYED_NOT_GET, MovieOrder.o_status == ORDER_STATUS_GET)).all()

        # 订单未付款未超时
        movie_orders_lock = MovieOrder.query.filter(MovieOrder.o_status == ORDER_STATUS_NOT_PAY).filter(MovieOrder.o_time > datetime.datetime.now()).all()

        seats = []

        for movie_orders in movie_orders_buyed:
            sold_seats = movie_orders.o_seats.split("#")
            seats += sold_seats

        for movie_orders in movie_orders_lock:
            sold_seats = movie_orders.o_seats.split("#")
            seats += sold_seats

        hall_movie = HallMovie.query.get(hall_movie_id)

        hall = Hall.query.get(hall_movie.h_hall_id)

        all_seats = hall.h_seats.split("#")

        # 可买的座位
        can_buy = list(set(all_seats) - set(seats))

        # 用户提交的座位
        want_buy = o_seats.split("#")

        # 判断用户提交的座位是否可购买
        for item in want_buy:
            if item not in can_buy:
                abort(400, msg="锁座失败")

        user = g.user

        movie_order = MovieOrder()
        movie_order.o_hall_movie_id = hall_movie_id
        movie_order.o_seats = o_seats
        movie_order.o_user_id = user.id
        # 订单过期时间
        movie_order.o_time = datetime.datetime.now() + datetime.timedelta(minutes=15)

        # # 悲观锁
        # db.session.with_lockmode("update")
        # # 给表加锁
        # db.session.Query(MovieOrder).with_lockmode("update")
        #
        # # 解锁
        # db.session.commit()

        # #事务
        # try:
        #     movie_order = MovieOrder.query.get(1)
        #
        # except Exception as e:
        #     print(e)
        #
        #     db.session.rollback()
        #
        # else:
        #     db.session.commit()
        #

        if not movie_order.save():
            abort(400, msg="下单失败")

        data = {
            "msg": "success",
            "status": HTTP_CREATE_OK,
            "data": marshal(movie_order, movie_order_fields),
        }

        return data


class MovieOrderResource(Resource):

    @require_permission(VIP_USER)
    def put(self, order_id):

        return {"msg": "change success"}
