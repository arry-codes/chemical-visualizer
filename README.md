# Chemical Equipment Visualizer

This is a project to visualize parameters from chemical equipment data. It has a Django backend and two frontends: a web app (React) and a desktop app (PyQt5).

## Project Structure
- `backend/`: Django REST API
- `frontend-web/`: React application
- `frontend-desktop/`: Desktop application (Python)

## How to Run

### 1. Backend (Start this first)
You need Python installed.
```bash
cd backend
pip install -r requirements.txt  # or install django djangorestframework pandas django-cors-headers reportlab
python manage.py migrate
python manage.py runserver
```
The server runs at `http://localhost:8000`.

### 2. Web App
You need Node.js installed.
```bash
cd frontend-web
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

### 3. Desktop App
```bash
cd frontend-desktop
pip install PyQt5 requests matplotlib
python main.py
```

## Features
- Upload CSV files containing equipment data.
- View charts for average flowrate, pressure, and temperature.
- See the distribution of equipment types.
- Download a PDF report.
- Login system (Basic Auth).

## Testing
You can use the `sample_equipment_data.csv` file to test the upload feature.
