# Chemical Equipment Visualizer

This is a project to visualize parameters from chemical equipment data. It has a Django backend and two frontends: a web app (React) and a desktop app (PyQt5).

## Project Structure
- `backend/`: Django REST API
- `frontend-web/`: React application
- `frontend-desktop/`: Desktop application (Python)

## Demo Video
Google Drive : <a href="https://drive.google.com/file/d/1_RXmh9drfqIRbcniLiV_flBEGMjkiBIR/view?usp=sharing">Link</a>

## How to Run

### 1. Backend (Start this first)

```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```
The server runs at `http://localhost:8000`.

### 2. Web App

```bash
cd frontend-web
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

### 3. Desktop App

```bash
cd frontend-desktop
python main.py
```

## Features
- Upload CSV files containing equipment data
- View charts for average flowrate, pressure, and temperature
- See the distribution of equipment types
- Download a PDF report
- Login system (Basic Auth)

## UI/UX
<p align="center">
<img width="1470" height="956" alt="Screenshot 2025-11-22 at 11 12 36 PM" src="https://github.com/user-attachments/assets/b9767f46-8f26-4aff-aed4-3a04fbd30310" />
(React based Frontend)
</p>

<p align="center">
<img width="4409" height="1732" alt="fosse_desk" src="https://github.com/user-attachments/assets/b9885407-61ec-47c2-a17e-2d94f87b7f2f" />
(PyQt5 based Desktop App)
</p>



