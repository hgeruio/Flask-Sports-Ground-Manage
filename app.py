from flask import Flask, session, g
import config
from exts import db
from blueprints.user import bp as user_bp
from models import User
from blueprints.public import bp

from flask_migrate import Migrate  # 映射到数据库当中

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(bp)


@app.before_request
def user_login_before():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def user_context():
    return {"user": g.user}


if __name__ == '__main__':
    app.run()
