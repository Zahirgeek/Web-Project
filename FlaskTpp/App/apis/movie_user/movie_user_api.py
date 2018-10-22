import uuid

from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal

from App.apis.api_contant import HTTP_CREATE_OK, USER_ACTION_REGISTER, USER_ACTION_LOGIN, HTTP_OK
from App.apis.movie_user.model_utils import get_user
from App.ext import cache
from App.models.movie_user import MovieUser

movie_user_fields = {
    "username": fields.String,
    "password": fields.String(attribute="_password"),
    "phone": fields.String,
}

single_movie_user_fields = {
    "status": fields.Integer,
    "msg": fields.String,
    "data": fields.Nested(movie_user_fields),
}

'''
注册: 用户名和手机号码都为必填字段
登录: 用户名和手机号码选填一个
'''
parse_base = reqparse.RequestParser()

parse_base.add_argument("password", type=str, required=True, help="请输入密码")
parse_base.add_argument("action", type=str, required=True, help="请确认请求参数")

parse_register = parse_base.copy()
parse_register.add_argument("username", type=str, required=True, help="请输入用户名")
parse_register.add_argument("phone", type=str, required=True, help="请输入手机号码")

parse_login = parse_base.copy()
parse_login.add_argument("username", type=str, help="请输入用户名")
parse_login.add_argument("phone", type=str, help="请输入手机号码")


class MovieUsersResource(Resource):

    # 用户注册,登录
    def post(self):

        args = parse_base.parse_args()

        password = args.get("password")
        action = args.get("action").lower()

        # 注册
        if action == USER_ACTION_REGISTER:

            args_register = parse_register.parse_args()
            phone = args_register.get("phone")
            username = args_register.get("username")

            movie_user = MovieUser()
            movie_user.username = username
            movie_user.password = password
            movie_user.phone = phone

            if not movie_user.save():
                abort(400, msg="create fail")

            data = {
                "status": HTTP_CREATE_OK,
                "msg": "用户创建成功",
                "data": marshal(movie_user),
            }

            return data

        # 登录
        elif action == USER_ACTION_LOGIN:

            args_login = parse_login.parse_args()
            phone = args_login.get("phone")
            username = args_login.get("username")

            user = get_user(username) or get_user(phone)

            if not user:
                abort(400, msg="用户不存在")

            if not user.check_password(password):
                abort(401, msg="密码错误")

            if user.is_delete:
                abort(401, msg="用户不存在")

            # 给用户发送token,并存到缓存中
            token = uuid.uuid4().hex

            cache.set(token, user.id, timeout=60*60*24*7)

            data = {
                "msg": "login success",
                "status": HTTP_OK,
                "token": token,
            }

            return data

        else:

            abort(400, msg="请提供正确的参数")