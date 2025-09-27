from __future__ import annotations

import numpy as np
from flask import Blueprint, current_app, jsonify, render_template, request


bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    return render_template("index.html", prediction_text=None)


@bp.route("/predict", methods=["POST"])
def predict():
    try:
        fuel_type = request.form["fuel-type"]
        num_cyl = request.form["num-of-cylinders"]
        engine_size = float(request.form["engine-size"])
        fuel_sys = request.form["fuel-system"]
        horsepower = float(request.form["horsepower"])
        city_mpg = float(request.form["city-mpg"])
        highway_mpg = float(request.form["highway-mpg"])
    except Exception:
        return render_template("index.html", prediction_text="Please enter valid values for all fields.")

    if any(x <= 0 for x in [engine_size, horsepower, city_mpg, highway_mpg]):
        return render_template("index.html", prediction_text="Please enter valid positive numbers for all numeric fields.")

    try:
        fuel_type_enc = current_app.config["LE_FUEL_TYPE"].transform([fuel_type])[0]
        num_cyl_enc = current_app.config["LE_NUM_CYL"].transform([num_cyl])[0]
        fuel_sys_enc = current_app.config["LE_FUEL_SYS"].transform([fuel_sys])[0]
    except Exception:
        return render_template("index.html", prediction_text="Invalid categorical value entered.")

    features = np.array([[fuel_type_enc, num_cyl_enc, engine_size, fuel_sys_enc, horsepower, city_mpg, highway_mpg]])
    prediction = current_app.config["MODEL"].predict(features)
    output = round((prediction[0] / 10) / 4, 2)
    output_inr = round(output * 83, 2)
    if output_inr < 0:
        output_inr = 0
    return render_template("index.html", prediction_text=f"The Car Price should be ₹ {output_inr}")


@bp.route("/predict_api", methods=["POST"])
def predict_api():
    data = request.get_json(force=True)
    prediction = current_app.config["MODEL"].predict([np.array(list(data.values()))])
    output = prediction[0]
    return jsonify(output)


