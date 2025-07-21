import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model_bundle = pickle.load(open('model.pkl', 'rb'))
model = model_bundle['model']
le_fuel_type = model_bundle['le_fuel_type']
le_num_cyl = model_bundle['le_num_cyl']
le_fuel_sys = model_bundle['le_fuel_sys']

@app.route('/')
def home():
    return render_template('index.html', prediction_text=None)

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    try:
        fuel_type = request.form['fuel-type']
        num_cyl = request.form['num-of-cylinders']
        engine_size = float(request.form['engine-size'])
        fuel_sys = request.form['fuel-system']
        horsepower = float(request.form['horsepower'])
        city_mpg = float(request.form['city-mpg'])
        highway_mpg = float(request.form['highway-mpg'])
    except Exception:
        return render_template('index.html', prediction_text='Please enter valid values for all fields.')
    # Validate numeric fields
    if any(x <= 0 for x in [engine_size, horsepower, city_mpg, highway_mpg]):
        return render_template('index.html', prediction_text='Please enter valid positive numbers for all numeric fields.')
    # Encode categorical fields
    try:
        fuel_type_enc = le_fuel_type.transform([fuel_type])[0]
        num_cyl_enc = le_num_cyl.transform([num_cyl])[0]
        fuel_sys_enc = le_fuel_sys.transform([fuel_sys])[0]
    except Exception:
        return render_template('index.html', prediction_text='Invalid categorical value entered.')
    features = np.array([[fuel_type_enc, num_cyl_enc, engine_size, fuel_sys_enc, horsepower, city_mpg, highway_mpg]])
    prediction = model.predict(features)
    output = round((prediction[0] / 10) / 4, 2)
    output_inr = round(output * 83, 2)
    if output_inr < 0:
        output_inr = 0
    return render_template('index.html', prediction_text='The Car Price should be ₹ {}'.format(output_inr))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)