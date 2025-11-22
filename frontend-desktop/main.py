import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, 
                             QTabWidget, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

API_URL = "http://localhost:8000/api/"

class LoginDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Chemical Visualizer")
        self.resize(300, 150)
        self.layout = QVBoxLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)
        
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)
        self.layout.addWidget(self.login_btn)
        
        self.setLayout(self.layout)
        self.auth = None

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username and password:
            self.auth = (username, password)
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Please enter username and password")

class MainWindow(QMainWindow):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.resize(800, 600)
        
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)
        
        self.init_upload_tab()
        self.init_viz_tab()
        
        self.current_upload_id = None

    def init_upload_tab(self):
        self.upload_tab = QWidget()
        layout = QVBoxLayout()
        
        upload_layout = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        upload_layout.addWidget(self.file_label)
        
        self.select_btn = QPushButton("Select CSV")
        self.select_btn.clicked.connect(self.select_file)
        upload_layout.addWidget(self.select_btn)
        
        self.upload_btn = QPushButton("Upload")
        self.upload_btn.clicked.connect(self.upload_file)
        upload_layout.addWidget(self.upload_btn)
        
        layout.addLayout(upload_layout)
        
        layout.addWidget(QLabel("Recent Uploads:"))
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_summary)
        layout.addWidget(self.history_list)
        
        self.refresh_btn = QPushButton("Refresh History")
        self.refresh_btn.clicked.connect(self.refresh_history)
        layout.addWidget(self.refresh_btn)
        
        self.upload_tab.setLayout(layout)
        self.central_widget.addTab(self.upload_tab, "Upload & History")
        
        self.refresh_history()

    def init_viz_tab(self):
        self.viz_tab = QWidget()
        layout = QVBoxLayout()
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.stats_label = QLabel("Select an upload to view stats")
        layout.addWidget(self.stats_label)
        
        self.viz_tab.setLayout(layout)
        self.central_widget.addTab(self.viz_tab, "Visualization")

    def select_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '.', "CSV files (*.csv)")
        if fname:
            self.file_path = fname
            self.file_label.setText(fname)

    def upload_file(self):
        if not hasattr(self, 'file_path'):
            return
        
        files = {'file': open(self.file_path, 'rb')}
        try:
            response = requests.post(f"{API_URL}upload/", files=files, auth=self.auth)
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "File uploaded successfully")
                self.refresh_history()
            else:
                QMessageBox.critical(self, "Error", f"Upload failed: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def refresh_history(self):
        try:
            response = requests.get(f"{API_URL}history/", auth=self.auth)
            if response.status_code == 200:
                self.history_list.clear()
                for item in response.json():
                    list_item = QListWidgetItem(f"{item['filename']} ({item['uploaded_at']})")
                    list_item.setData(Qt.UserRole, item['id'])
                    self.history_list.addItem(list_item)
        except Exception as e:
            print(f"Error fetching history: {e}")

    def load_summary(self, item):
        upload_id = item.data(Qt.UserRole)
        self.current_upload_id = upload_id
        
        try:
            response = requests.get(f"{API_URL}summary/{upload_id}/", auth=self.auth)
            if response.status_code == 200:
                data = response.json()
                self.update_viz(data)
                self.central_widget.setCurrentIndex(1)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_viz(self, data):
        self.figure.clear()
        
        ax1 = self.figure.add_subplot(121)
        ax2 = self.figure.add_subplot(122)
        
        params = ['Flowrate', 'Pressure', 'Temperature']
        values = [data['avg_flowrate'], data['avg_pressure'], data['avg_temperature']]
        ax1.bar(params, values, color=['red', 'blue', 'orange'])
        ax1.set_title('Average Parameters')
        
        types = [d['equipment_type'] for d in data['type_distribution']]
        counts = [d['count'] for d in data['type_distribution']]
        ax2.pie(counts, labels=types, autopct='%1.1f%%')
        ax2.set_title('Equipment Type Distribution')
        
        self.canvas.draw()
        
        self.stats_label.setText(f"Total Equipment: {data['total_count']} | File: {data['filename']}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    login = LoginDialog()
    login.show()
    
    app.exec_()
    
    if login.auth:
        window = MainWindow(login.auth)
        window.show()
        sys.exit(app.exec_())
