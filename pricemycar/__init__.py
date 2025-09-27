import os
import pickle
from flask import Flask


def create_app() -> Flask:
    """Application factory to create and configure the Flask app.

    Loads the trained model bundle from the project root and registers routes.
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Resolve project root to load the model bundle regardless of CWD
    package_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(package_dir, os.pardir))
    model_path = os.path.join(project_root, "model.pkl")

    with open(model_path, "rb") as f:
        model_bundle = pickle.load(f)

    # Store model and encoders in app config for blueprint access
    app.config["MODEL"] = model_bundle["model"]
    app.config["LE_FUEL_TYPE"] = model_bundle["le_fuel_type"]
    app.config["LE_NUM_CYL"] = model_bundle["le_num_cyl"]
    app.config["LE_FUEL_SYS"] = model_bundle["le_fuel_sys"]

    # Register blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app


