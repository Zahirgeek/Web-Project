import uuid

from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal

from App.apis.admin.model_utils import get_admin_user
from App.apis.api_contant import HTTP_CREATE_OK, USER_ACTION_REGISTER, USER_ACTION_LOGIN, HTTP_OK
from App.apis.movie_user.model_utils import get_user
from App.ext import cache
from App.models.admin.admin_user_model import AdminUser
from App.models.movie_user import MovieUser
from App.settings import ADMINS
from App.utils import generate_admin_user_token

admin_user_fields = {
    "username": fields.String,
    "password": fields.String(attribute="_password"),
}

single_admin_user_fields = {
    "status": fields.Integer,
    "msg": fields.String,
    "data": fields.Nested(admin_user_fields),
}

'''
注册: 用户名和手机号码都为必填字段
登录: 用户名和手机号码选填一个
'''
parse_base = reqparse.RequestParser()

parse_base.add_argument("password", type=str, required=True, help="请输入密码")
parse_base.add_argument("action", type=str, required=True, help="请确认请求参数")
parse_base.add_argument("username", type=str, required=True, help="请输入用户名")


class AdminUsersResource(Resource):

    # 用户注册,登录
    def post(self):

        args = parse_base.parse_args()

        password = args.get("password")
        action = args.get("action").lower()

        # 注册
        if action == USER_ACTION_REGISTER:

            args_register = parse_base.parse_args()
            username = args_register.get("username")

            admin_user = AdminUser()
            admin_user.username = username
            admin_user.password = password

            # 验证是否是超级用户
            if username in ADMINS:

                admin_user.is_super = True

            if not admin_user.save():
                abort(400, msg="create fail")

            data = {
                "status": HTTP_CREATE_OK,
                "msg": "用户创建成功",
                "data": marshal(admin_user, single_admin_user_fields),
            }

            return data

        # 登录
        elif action == USER_ACTION_LOGIN:

            args_login = parse_base.parse_args()
            username = args_login.get("username")

            user = get_admin_user(username)

            if not user:
                abort(400, msg="用户不存在")

            if not user.check_password(password):
                abort(401, msg="密码错误")

            if user.is_delete:
                abort(401, msg="用户不存在")

            # 给用户发送token,并存到缓存中
            token = generate_admin_user_token()

            cache.set(token, user.id, timeout=60*60*24*7)

            data = {
                "msg": "login success",
                "status": HTTP_OK,
                "token": token,
            }

            return data

        else:

            abort(400, msg="请提供正确的参数")