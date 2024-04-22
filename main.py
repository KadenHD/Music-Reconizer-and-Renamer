import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt
from asyncio import run
from ShazamRecognizer import ShazamRecognizer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shazam Recognizer")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.drop_label = QLabel("Click here or Drop folder here", alignment=Qt.AlignCenter)
        layout.addWidget(self.drop_label)

        self.recognizer = ShazamRecognizer()

        self.setAcceptDrops(True)

        self.drop_label.mousePressEvent = self.open_folder_dialog

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            for url in urls:
                file_path = url.toLocalFile()
                if file_path and os.path.isdir(file_path):
                    run(self.recognize_songs_in_directory(file_path))
                    break
        event.accept()

    async def recognize_songs_in_directory(self, directory_path):
        await self.recognizer.recognize_songs_in_directory(directory_path)
        QApplication.quit()

    def open_folder_dialog(self, event):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder_path:
            run(self.recognize_songs_in_directory(folder_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
