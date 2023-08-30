from flask import Flask, jsonify
from blueprint.admin import admin_blueprint
from setup.appsetup import secret_key
from flask_wtf.csrf import CSRFProtect, CSRFError

from setup.dbsetup import db, create_tables
# from admin import admin_blueprint


# Create the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/narc_setup'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


csrf.init_app(app)

# Register the blueprint with the app
app.register_blueprint(admin_blueprint, url_prefix='/admin')


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return jsonify({"status_code": 400, "status": "Not allowed"}), 400


if __name__ == "__main__":
    create_tables(app)  # Add this line before running the app
    app.run(debug=True, host='0.0.0.0', port=4000)
