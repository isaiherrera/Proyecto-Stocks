from flask import Flask
import db
import os
from templates import auth
import stocks

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'almacen.db'), )

app.register_blueprint(auth.bp)
app.register_blueprint(stocks.bp)
app.add_url_rule('/', endpoint='index')

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
