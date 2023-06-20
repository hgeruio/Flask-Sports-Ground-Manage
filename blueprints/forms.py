from re import match

import wtforms
from wtforms.validators import Email, Length, Regexp


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Regexp(r"^[a-zA-Z0-9]{4,20}", message="密码格式错误！")])

class AddUser(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Regexp(r"^[a-zA-Z0-9]{4,20}", message="密码格式错误！")])
    name= wtforms.StringField(validators=[Length(min=2, max=20, message="用户名格式错误！")])