import sys, os, shutil, subprocess
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout
from PySide6.QtCore import Qt
from helpers.csv import CSVHelper

class CookieLoaderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.cookies_folder = "cookies"
        self.data_csv = "data.csv"
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cookie Loader')
        self.setGeometry(300, 300, 800, 600)

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.load_button = QPushButton('Load Cookie')
        self.load_button.clicked.connect(self.load_cookies)
        button_layout.addWidget(self.load_button)

        self.refresh_button = QPushButton('Refresh data')
        self.refresh_button.clicked.connect(self.refresh_devices_and_csv)
        button_layout.addWidget(self.refresh_button)
        layout.addLayout(button_layout)

        self.status_label = QLabel('')
        layout.addWidget(self.status_label)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Model', 'Serial', 'Username', 'Cookie File'])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.refresh_table()

    def load_cookies(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("Text files (*.txt)")
        file_dialog.setViewMode(QFileDialog.ViewMode.List)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()

            if not os.path.exists(self.cookies_folder):
                os.makedirs(self.cookies_folder)

            copied_files = []
            for file_path in selected_files:
                filename = os.path.basename(file_path)
                destination = os.path.join(self.cookies_folder, filename)
                shutil.copy2(file_path, destination)
                copied_files.append(destination)

            self.status_label.setText(f'Successfully loaded {len(copied_files)} cookie files')

    def get_devices_with_model(self):
        try:
            out = subprocess.check_output(["adb", "devices", "-l"], text=True)
            lines = out.strip().splitlines()[1:]

            devices = []
            for line in lines:
                if "device" not in line:
                    continue

                parts = line.split()
                serial = parts[0]

                model = "UNKNOWN"
                for p in parts:
                    if p.startswith("model:"):
                        model = p.split("model:")[1]
                        break

                devices.append({
                    "serial": serial,
                    "model": model,
                    "raw": line
                })

            return devices
        except Exception as e:
            print(f"Error getting devices: {e}")
            return []

    def refresh_table(self):
        try:
            try:
                rows = CSVHelper.read_csv(self.data_csv)
            except FileNotFoundError:
                rows = []

            num_rows = len(rows)
            if num_rows == 0:
                self.table.setRowCount(0)
                self.status_label.setText('No data in CSV found')
                return

            self.table.setRowCount(num_rows)
            self.table.setColumnCount(4)

            for row_idx in range(num_rows):
                model = rows[row_idx][0] if row_idx < len(rows) and len(rows[row_idx]) > 0 else ""
                self.table.setItem(row_idx, 0, QTableWidgetItem(model))

                serial = rows[row_idx][1] if row_idx < len(rows) and len(rows[row_idx]) > 1 else ""
                self.table.setItem(row_idx, 1, QTableWidgetItem(serial))

                username = rows[row_idx][2] if row_idx < len(rows) and len(rows[row_idx]) > 2 else ""
                self.table.setItem(row_idx, 2, QTableWidgetItem(username))

                cookie_file = rows[row_idx][3] if row_idx < len(rows) and len(rows[row_idx]) > 3 else ""
                self.table.setItem(row_idx, 3, QTableWidgetItem(cookie_file))

            self.table.resizeColumnsToContents()

            self.status_label.setText(f'Loaded {len(rows)} rows from CSV')

        except Exception as e:
            self.status_label.setText(f'Error refreshing table: {str(e)}')
            print(f"Error details: {e}")

    def refresh_devices_and_csv(self):
        try:
            devices = self.get_devices_with_model()

            cookie_files = []
            if os.path.exists(self.cookies_folder):
                for file in os.listdir(self.cookies_folder):
                    if file.endswith('.txt'):
                        cookie_files.append(file)

            rows = []
            max_rows = max(len(devices), len(cookie_files))

            from utils.username import detect_username_from_cookie_filename
            for i in range(max_rows):
                model = devices[i]["model"] if i < len(devices) else ""
                serial = devices[i]["serial"] if i < len(devices) else ""
                cookie_file = cookie_files[i] if i < len(cookie_files) else ""
                username = detect_username_from_cookie_filename(cookie_file) if cookie_file else ""
                rows.append([model, serial, username, cookie_file])

            CSVHelper.write_csv(self.data_csv, rows)

            self.refresh_table()
            self.status_label.setText(f'Updated CSV with {len(devices)} devices and {len(cookie_files)} cookie files')

        except Exception as e:
            self.status_label.setText(f'Error refreshing devices: {str(e)}')
            print(f"Error details: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = CookieLoaderGUI()
    gui.show()
    sys.exit(app.exec())