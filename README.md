# Automobile Price Prediction
<img width="975" height="493" alt="image" src="https://github.com/user-attachments/assets/07a68052-2dd5-42f8-a697-2ac461d3db9b" />
<img width="317" height="392" alt="image" src="https://github.com/user-attachments/assets/a1a44531-23be-496f-ad2c-1442942572a7" />


This project is a web application that predicts the price of an automobile based on user input features using a machine learning model trained on real-world data.

## Features
- Predicts car price based on:
  - Fuel Type
  - Number of Cylinders
  - Engine Size (cc)
  - Fuel System
  - Horsepower
  - City-mpg
  - Highway-mpg
- User-friendly web interface built with Flask
- Input validation and error handling
- Results displayed in Indian Rupees (₹)

## Setup Instructions
1. **Clone the repository:**
   ```sh
   git clone https://github.com/gitXsingh/PriceMyCar.git
   cd PriceMyCar/Flask_automobile_pred
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   *(If requirements.txt is missing, install: flask, numpy, pandas, scikit-learn)*
3. **Run the app:**
   ```sh
   python app.py
   ```
4. **Open your browser:**
   Go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage
- Fill in the car details in the form.
- Click 'Predict' to see the estimated price.

## Credits
- Data: UCI Machine Learning Repository (Automobile Data Set)
- Model: Linear Regression (scikit-learn)
- App: Flask, HTML/CSS

---

**Author:** gitXsingh

For any issues or contributions, please open an issue or pull request on GitHub. 
