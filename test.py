import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, secondary_window):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)

        # Create a central widget and set a layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add a label to the main window
        label = QLabel("This is the main window.")
        layout.addWidget(label)

        # Store the reference to the secondary window
        self.secondary_window = secondary_window

        # Optionally, you can add a button or action to show the secondary window
        # For example, you can uncomment the following lines to add a button:
        # show_button = QPushButton("Show Secondary Window")
        # show_button.clicked.connect(self.show_secondary_window)
        # layout.addWidget(show_button)

    def show_secondary_window(self):
        self.secondary_window.show()

class SecondaryWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Secondary Window")
        self.setGeometry(200, 200, 300, 200)

        # Set the window flag to Qt.Tool to hide it from the taskbar
        #self.setWindowFlags(Qt.Tool)

        # Create a central widget and set a layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add a label to the secondary window
        label = QLabel("This is the secondary window.")
        layout.addWidget(label)

def main():
    app = QApplication(sys.argv)

    # Create the secondary window
    secondary_window = SecondaryWindow()

    # Create the main window and pass the secondary window to it
    main_window = MainWindow(secondary_window)

    # Show the main window
    main_window.show()

    # Show the secondary window
    secondary_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
