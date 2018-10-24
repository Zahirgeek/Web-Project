from App.models.cinema_admin.cinema_user_model import CinemaUser


# 实现根据id, 手机号码, 用户名查找并返回用户
def get_cinema_user(user_ident):

    if not user_ident:
        return None

    # 根据id查找
    user = CinemaUser.query.get(user_ident)

    if user:
        return user

    # 根据手机号码查找
    user = CinemaUser.query.filter(CinemaUser.phone == user_ident).first()

    if user:
        return user

    # 根据用户名查找
    user = CinemaUser.query.filter(CinemaUser.username == user_ident).first()

    if user:
        return user

    return None
