# AGRI-MITRA: AI-Powered Precision Agriculture Platform

AGRI-MITRA is an end-to-end, production-grade agricultural decision support system built with Python, Flask, Scikit-Learn, SQLAlchemy, ReportLab, and modern UI/UX design. The platform leverages trained Machine Learning models to deliver real-time crop suitability classification and scientific fertilizer formulation recommendations tailored to field soil chemistry and ambient environmental conditions.

---

## 🌟 Key Features

### 🌾 Crop Suitability Prediction
- **Model**: Multi-class Random Forest Classifier (`models/ml/Crop_Prediction_RF.pkl`).
- **Input Parameters (7)**: Nitrogen (N), Phosphorus (P), Potassium (K), Temperature (°C), Humidity (%), Soil pH, and Rainfall (mm).
- **Target**: 22 agricultural crop classes (`rice`, `maize`, `chickpea`, `kidneybeans`, `pigeonpeas`, `mothbeans`, `mungbean`, `blackgram`, `lentil`, `pomegranate`, `banana`, `mango`, `grapes`, `watermelon`, `muskmelon`, `apple`, `orange`, `papaya`, `coconut`, `cotton`, `jute`, `coffee`).
- **Accuracy**: **99.91%** evaluated against cleaned dataset.
- **Baseline Fertilizer Advisory**: Generates crop-specific nutrient guidance following prediction.

### 🧪 Fertilizer Recommendation Advisor
- **Model**: Random Forest Classifier (`models/ml/Fertilizer_Recommendation_RF.pkl`).
- **Input Parameters**: Temperature (°C), Humidity (%), Soil Moisture (%), Soil Type, Crop Type, Nitrogen (N), Phosphorus (P), and Potassium (K).
- **Target Formulations**: `Urea`, `DAP`, `14-35-14`, `28-28`, `17-17-17`, `20-20`, `10-26-26`.
- **Accuracy**: **98.99%** evaluated against cleaned dataset.
- **Scientific Rationale (WHY)**: Synthesizes detailed agronomic justifications and application guidelines based on nutrient deficits.

### 📊 Comprehensive User & Admin Systems
- **User Authentication**: Secure scrypt/pbkdf2 password hashing, registration, login sessions, profile management, and password modification.
- **Prediction History**: Filterable archives for crop and fertilizer predictions with one-click deletion and inspection.
- **Export System**: Export user histories or full administrative databases to CSV format.
- **PDF Certification**: Generate official print-ready PDF advisory certificates with ReportLab.
- **Admin Operations Center**:
  - Live summary KPI telemetry.
  - Interactive 7-Day daily activity trend visualizer.
  - Top 5/Top 10 predicted crops with market share percentages.
  - Top 5/Top 10 recommended fertilizers.
  - Global prediction inspection with keyword search and filtering.
  - Farmer directory with contact details and activity metrics.

---

## 🏗️ Project Architecture

```
AGRI-MITRA/
├── app.py                     # Application entry point & blueprint registration
├── config.py                  # Environment configuration & model paths
├── requirements.txt           # Python dependency specifications
├── README.md                  # Comprehensive documentation
├── .env                       # Environment variables
├── .gitignore                 # Version control exclusions
│
├── instance/
│   └── agri_mitra.db          # SQLite relational database
│
├── models/
│   ├── database_models.py     # SQLAlchemy models (User, CropPrediction, FertilizerPrediction)
│   ├── candidate/             # Reproducibility training output directory
│   └── ml/
│       ├── Crop_Prediction_RF.pkl             # Production Crop ML model
│       ├── crop_encoder.pkl                   # Crop target label encoder
│       ├── Fertilizer_Recommendation_RF.pkl   # Production Fertilizer ML model
│       ├── fertilizer_encoder.pkl             # Fertilizer target label encoder
│       └── model_metadata.json                # Complete verified model metadata
│
├── datasets/
│   ├── raw/
│   │   ├── crop_dataset.csv                   # Raw crop training dataset
│   │   └── fertilizer_dataset.csv             # Raw fertilizer training dataset
│   ├── cleaned/
│   │   ├── crop_cleaned.csv                   # Validated & cleaned crop dataset
│   │   └── fertilizer_cleaned.csv             # Validated & cleaned fertilizer dataset
│   └── processed/
│       ├── crop_features.csv                  # Engineered features for crop model
│       └── fertilizer_features.csv            # Engineered features for fertilizer model
│
├── preprocessing/
│   ├── data_validation.py     # Reusable data & payload validation logic
│   ├── clean_crop_data.py     # Crop data cleaning pipeline
│   ├── clean_fertilizer_data.py # Fertilizer data cleaning pipeline
│   └── feature_engineering.py # Model feature alignment & array transformations
│
├── training/
│   ├── train_crop_model.py         # Candidate model reproducibility trainer
│   ├── train_fertilizer_model.py   # Candidate model reproducibility trainer
│   ├── evaluate_crop_model.py      # Production crop model evaluation script
│   └── evaluate_fertilizer_model.py# Production fertilizer model evaluation script
│
├── database/
│   ├── db.py                  # SQLAlchemy init & admin account auto-seeder
│   └── migrations/            # Migration tracking
│
├── routes/
│   ├── home_routes.py         # Landing & informational routes
│   ├── auth_routes.py         # Sign up, sign in, sign out
│   ├── dashboard_routes.py    # Farmer overview & KPI counters
│   ├── crop_routes.py         # Crop prediction submission & results
│   ├── fertilizer_routes.py   # Fertilizer recommendation submission & results
│   ├── history_routes.py      # Archive management & record deletion
│   ├── profile_routes.py      # Personal info & password security
│   ├── report_routes.py       # PDF generator endpoints & HTML report views
│   ├── export_routes.py       # User and admin CSV downloads
│   └── admin_routes.py        # Analytics, top metrics, user contact audits
│
├── services/
│   ├── auth_service.py        # Authentication & credential security
│   ├── crop_prediction_service.py # Inference & agronomic baseline logic
│   ├── fertilizer_recommendation_service.py # Inference & rationale generation
│   ├── history_service.py     # Unified and modular query handlers
│   ├── profile_service.py     # Account updates
│   ├── report_service.py      # ReportLab document templates & styling
│   ├── csv_export_service.py  # Streaming CSV response generation
│   └── admin_service.py       # Analytics, 7-day bucket queries, rankings
│
├── utils/
│   ├── decorators.py          # @login_required, @admin_required
│   ├── validators.py          # Input format & range validation
│   ├── security.py            # Password hashing & cryptographic tokens
│   ├── file_handler.py        # Secure filesystem handlers
│   └── helpers.py             # Agronomic guidelines & rationale dictionaries
│
├── templates/
│   ├── base.html              # Core navigation, flash alerts, and layout
│   ├── home/index.html        # Landing page
│   ├── auth/                  # login.html, signup.html
│   ├── dashboard/             # dashboard.html
│   ├── crop/                  # crop_form.html, crop_result.html
│   ├── fertilizer/            # fertilizer_form.html, fertilizer_result.html
│   ├── history/               # history.html, crop_history.html, fertilizer_history.html
│   ├── profile/               # profile.html, edit_profile.html, change_password.html
│   ├── reports/               # crop_report.html, fertilizer_report.html
│   ├── admin/                 # admin_login.html, admin_dashboard.html, top_crops.html,
│   │                          # top_fertilizers.html, user_predictions.html,
│   │                          # user_details.html, prediction_table.html
│   └── errors/                # 403.html, 404.html, 500.html
│
├── static/
│   ├── css/                   # style.css, responsive.css, dashboard.css,
│   │                          # crop.css, fertilizer.css, history.css,
│   │                          # profile.css, admin.css, report.css, auth.css
│   └── js/                    # main.js, crop.js, fertilizer.js, admin.js,
│                              # dashboard.js, history.js, profile.js, export.js
│
└── tests/
    ├── test_database.py       # Model & relationship testing
    ├── test_auth.py           # User authentication & registration testing
    ├── test_crop_prediction.py# Crop ML inference & advisory testing
    ├── test_fertilizer_recommendation.py # Fertilizer ML inference & rationale testing
    ├── test_history.py        # History querying & deletion testing
    ├── test_profile.py        # Profile & password change testing
    ├── test_admin.py          # Administrative analytics & queries testing
    ├── test_pdf_report.py     # ReportLab PDF generation verification
    └── test_csv_export.py     # CSV streaming verification
```

---

## 🔬 Machine Learning Pipeline & Model Compatibility

### Model Artifact Inspection
- **Crop Model (`models/ml/Crop_Prediction_RF.pkl`)**:
  - Encapsulated bundle with keys: `model`, `features`, `classes`.
  - Feature names and order: `['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']`.
  - Model outputs direct human-readable crop names (`str`).
  - Production pickle preserved untouched.

- **Fertilizer Model (`models/ml/Fertilizer_Recommendation_RF.pkl`)**:
  - Encapsulated bundle with keys: `model`, `features`, `classes`.
  - The model expects 6 numerical features: `['temperature', 'humidity', 'Moisture', 'N', 'K', 'K']`.
  - Features `N`, `P`, `K`, `soil_type`, and `crop_type` are collected from the user and stored in the database for complete agronomic records.
  - The feature engineering pipeline aligns incoming data into the exact 6-feature array expected by the model.
  - Production pickle preserved untouched.

---

## 🚀 Setup & Execution

### 1. Environment Preparation
Ensure Python 3.10+ is installed:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Configuration
Verify configuration variables in `.env`:
```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=agri-mitra-secure-secret-key-2026
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@agrimitra.com
ADMIN_PASSWORD=ChangeThisAdminPassword!2026
PORT=5001
```

### 3. Regenerating Datasets (Optional)
Run the preprocessing pipeline to refresh cleaned and processed datasets:
```bash
python3 preprocessing/clean_crop_data.py
python3 preprocessing/clean_fertilizer_data.py
python3 preprocessing/feature_engineering.py
```

### 4. Running the Model Evaluator
Evaluate production model accuracy and view full classification reports:
```bash
python3 training/evaluate_crop_model.py
python3 training/evaluate_fertilizer_model.py
```

### 5. Running the Application
Start the Flask application server:
```bash
python3 app.py
```
Access the application at `http://127.0.0.1:5001`.

### 6. Admin Login Credentials
- **URL**: `http://127.0.0.1:5001/admin/login`
- **Email**: `admin@agrimitra.com`
- **Password**: `ChangeThisAdminPassword!2026`

---

## 🧪 Automated Test Suite

Run all 27 unit and integration tests with `pytest`:
```bash
python3 -m pytest -v
```

All tests validate:
- Database schema, foreign key relations, cascade deletions.
- User signup, duplicate rejection, and password verification.
- Crop prediction validation, inference, and baseline advisory generation.
- Fertilizer recommendation validation, inference, and rationale synthesis.
- ReportLab PDF generation with standard `%PDF` header validation.
- CSV export generation for crop, fertilizer, user, and administrative datasets.
- Profile editing and password updating.
- Admin dashboard calculations, 7-day analytics, and user directory search.
