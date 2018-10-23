

# 实现根据id, 用户名查找并返回用户
from App.models.admin.admin_user_model import AdminUser


def get_admin_user(user_ident):

    if not user_ident:
        return None

    # 根据id查找
    user = AdminUser.query.get(user_ident)

    if user:
        return user

    # 根据用户名查找
    user = AdminUser.query.filter(AdminUser.username == user_ident).first()

    if user:
        return user

    return None
