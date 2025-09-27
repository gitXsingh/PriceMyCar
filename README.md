# PriceMyCar — Automobile Price Prediction (Flask)

A Flask app that predicts automobile prices using a pre-trained scikit-learn model bundle.

## Repository Overview

```
PriceMyCar/
├─ app.py                      # App entrypoint; imports factory and runs the dev server
├─ model.pkl                   # Trained model + label encoders (pickle bundle)
├─ pricemycar/
│  ├─ __init__.py             # Application factory; loads model.pkl and registers routes
│  ├─ routes.py               # Routes: GET /, POST /predict, POST /predict_api
│  ├─ templates/
│  │  └─ index.html          # UI form view (uses url_for('main.predict'))
│  └─ static/
│     └─ css/
│        └─ style.css        # Styles for the UI
```

### File-by-File Details
- `app.py`
  - Minimal runner that creates the Flask app via `pricemycar.create_app()` and starts the dev server.
  - Use `python app.py` during development.
- `model.pkl`
  - A pickled dictionary containing:
    - `model`: `sklearn.linear_model.LinearRegression`
    - `le_fuel_type`, `le_num_cyl`, `le_fuel_sys`: `sklearn.preprocessing.LabelEncoder` instances used at inference to encode categorical fields.
- `pricemycar/__init__.py`
  - Implements `create_app()` (Flask application factory pattern).
  - Resolves the project root and loads `model.pkl` regardless of current working directory.
  - Stores the model and encoders in `app.config` for access in routes.
- `pricemycar/routes.py`
  - `GET /` → Renders `index.html` with an empty state or prediction result.
  - `POST /predict` → Reads and validates form fields, encodes categories with saved encoders, calls the model, and renders the result.
  - `POST /predict_api` → Accepts JSON (for programmatic use). It directly calls the model; prefer the form route for best validation/encoding.
- `pricemycar/templates/index.html`
  - The HTML form page. Posts to `url_for('main.predict')` since routes are registered under the `main` blueprint.
  - Uses external CSS via `{{ url_for('static', filename='css/style.css') }}` and also includes an inline style block for layout.
- `pricemycar/static/css/style.css`
  - Stylesheet used by the UI.

## Endpoints
- `GET /`
  - Returns the prediction form.
- `POST /predict`
  - Form fields (all required):
    - `fuel-type`: `gas` | `diesel`
    - `num-of-cylinders`: `two` | `three` | `four` | `five` | `six` | `eight` | `twelve`
    - `engine-size`: number (> 0)
    - `fuel-system`: `mpfi` | `2bbl` | `idi` | `1bbl` | `spdi` | `4bbl` | `mfi` | `spfi`
    - `horsepower`: number (> 0)
    - `city-mpg`: number (> 0)
    - `highway-mpg`: number (> 0)
  - Response: renders `index.html` with the predicted price text.
- `POST /predict_api`
  - Body: JSON. Values are read in order and passed to the model. Prefer the form route for robust encoding/validation.

## How Predictions Work (High Level)
1. Categorical inputs are label-encoded using the encoders saved in `model.pkl`.
2. Numeric inputs are validated to be positive.
3. The linear regression model predicts price; output is then scaled/rounded for display.

## Run Locally

### 1) Clone
```bash
# Replace REPO_URL with the actual repository URL
git clone REPO_URL
cd PriceMyCar
```

### 2) Create and activate a virtual environment
- Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
- macOS/Linux (bash/zsh):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install --upgrade pip
pip install flask==3.1.2 numpy==2.2.6 scikit-learn==1.7.2 pandas==2.3.2
# Optional: match the original training version to remove the pickle warning
# pip install scikit-learn==1.3.2
```

### 4) Start the server
```bash
python app.py
```
Open your browser at `http://127.0.0.1:5000/` (or the host/port shown in the console).

Stop with `Ctrl+C`.

## Tips & Troubleshooting
- scikit-learn version warning when loading `model.pkl`:
  - Expected if your installed version differs from the one used to create the pickle; functionally it works.
  - To silence it, install `scikit-learn==1.3.2` or re-save the model with your installed version.
- Port 5000 already in use:
  - Windows (PowerShell):
    ```powershell
    netstat -ano | Select-String ':5000'
    Stop-Process -Id <PID> -Force
    ```
  - macOS/Linux:
    ```bash
    lsof -i :5000
    kill -9 <PID>
    ```
- PowerShell execution policy blocks activation scripts:
  - Run as Administrator and set: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
  - Or run without activation using the interpreter path:
    - Windows: `.venv\Scripts\python.exe app.py`
    - macOS/Linux: `.venv/bin/python app.py`
- UI not updating after changes:
  - Hard refresh the browser (`Ctrl+F5`) to clear cached assets.

## License
Specify your license here (e.g., MIT).
