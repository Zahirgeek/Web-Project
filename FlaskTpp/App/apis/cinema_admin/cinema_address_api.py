'''
电影院地址管理
'''
from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.api_contant import HTTP_CREATE_OK
from App.apis.cinema_admin.utils import require_permission
from App.models.cinema_admin.cinema_address_model import CinemaAddress
from App.models.cinema_admin.permissions_constant import PERMISSION_WRITE

'''
    c_user_id = db.Column(db.Integer, db.ForeignKey(CinemaUser.id))
    name = db.Column(db.String(64))
    city = db.Column(db.String(16))
    district = db.Column(db.String(16))
    address = db.Column(db.String(128))
    phone = db.Column(db.String(32))
'''
parse = reqparse.RequestParser()
parse.add_argument("name", required=True, help="请提供影院名字")
parse.add_argument("city", required=True, help="请提供城市名称")
parse.add_argument("district", required=True, help="请提供所在区")
parse.add_argument("address", required=True, help="请提供详细地址")
parse.add_argument("phone", required=True, help="请提供联系方式")

cinema_fields = {
    "c_user_id": fields.Integer,
    "name": fields.String,
    "city": fields.String,
    "district": fields.Integer,
    "address": fields.String,
    "phone": fields.String,

    "score": fields.Float,
    "servicecharge": fields.Float,
    "astrict": fields.Float,
    "hallnum": fields.Integer,

}


class CinemaAddressesResource(Resource):

    def get(self):
        return {"msg": "ok"}

    # 添加电影院地址
    @require_permission(PERMISSION_WRITE)
    def post(self):
        args = parse.parse_args()

        name = args.get("name")
        phone = args.get("phone")
        city = args.get("city")
        district = args.get("district")
        address = args.get("address")

        cinema_address = CinemaAddress()
        cinema_address.c_user_id = g.usr.id
        cinema_address.name = name
        cinema_address.phone = phone
        cinema_address.city = city
        cinema_address.district = district
        cinema_address.address  = address

        if not cinema_address.save():
            abort(400, msg="cinema can't save")
        data = {
            "status": HTTP_CREATE_OK,
            "msg": "创建地址成功",
            "data": marshal(cinema_address, cinema_fields)
        }

        return data


class CinemaAddressResource(Resource):

    def get(self, id):
        pass

    def put(self, id):
        pass

    def patch(self, id):
        pass

    def delete(self, id):
        pass