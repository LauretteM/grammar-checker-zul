import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGraphicsDropShadowEffect, QMessageBox, QDialog, QGroupBox, QComboBox, QSizePolicy, QSpacerItem
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class GrammarCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and dimensions
        self.setWindowTitle("isiZulu Grammar Checker")
        window_width = 1200
        window_height = 550

        # Calculate center of user's screen
        user_screen = QApplication.primaryScreen()
        screen_geometry = user_screen.availableGeometry() # Access user's desktop and retrieve screen geometry

        x = (screen_geometry.width() - window_width) // 2 # Screen width - window width // 2
        y = (screen_geometry.height() - window_height) // 2 # Screen height - window height // 2
        
        # Set window position and size
        self.setGeometry(x, y, window_width, window_height)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: white;")

        # Create a layout for the central widget
        self.main_layout = QVBoxLayout()

        # Create a title label
        title_label = QLabel("isiZulu Grammar Checker", self)

        # Create a QFont object using "Inter" font family
        title_font = QFont("Helvetica Neue", 45)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            background-color: #FFFFFF;
            color: black;
        """)

        # Create app description
        description_label = QLabel("Start typing below for error-free grammar.", self)

        # Customise app description
        description_font = QFont("Helvetica Neue", 16)
        description_label.setFont(description_font)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet(
            """
            QLabel {
                color: black;                
            }
            """
        )

        # Create a container for input-related items
        input_container = QGroupBox()
        input_container_layout = QVBoxLayout()

        input_container = QWidget(self)
        # Create a layout for the input text area and button

        input_layout = QHBoxLayout()

        # Create a text input area (QTextEdit) for input text
        self.input_text_edit = QTextEdit (self)
        input_text_font = QFont("Helvetica Neue", 16)
        self.input_text_edit.setFont(input_text_font)
        self.input_text_edit.setFixedWidth(600)  # Set a fixed width
        self.input_text_edit.setFixedHeight(250)  # Set a fixed height
        self.input_text_edit.setStyleSheet(
            """
            color: black;
            background-color: white;
            border: 0.5px solid #808080;
            border-radius: 10px; /* Create rounded corners
            font-size: 16px;
            """
        )
        input_area_shadow = QGraphicsDropShadowEffect(self)
        input_area_shadow.setColor(QColor(128, 128, 128, 200))
        input_area_shadow.setBlurRadius(20)
        input_area_shadow.setXOffset(7)
        input_area_shadow.setYOffset(7)
        self.input_text_edit.setGraphicsEffect(input_area_shadow)

        input_layout.addWidget(self.input_text_edit, alignment=Qt.AlignmentFlag.AlignCenter)

        """
        Create a dynamic "Suggestions section.
        """

        self.suggestions_layout = QVBoxLayout()
        self.suggestions = []

        """
        Create a button to check grammar text.
        """

        buttons_layout = QVBoxLayout()

        # Create a button for grammar check with an icon
        self.check_button = QPushButton("Check my grammar")

        # Set the font for the button
        button_font = QFont("Helvetica Neue", 16)
        self.check_button.setFont(button_font)

        self.check_button.setStyleSheet(
            """
            QPushButton {
                background-color: black;
                color: white;
                border: 1px inset #666666;
                border-radius: 10px;
                padding: 10px;
                margin-left: 300px;
                margin-right: 300px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            """
        )
        self.check_button.clicked.connect(self.suggestion)

        """
        Add a clear all button
        """
       
        self.clearAll_button = QPushButton("Clear text", self)
    
        # Set the font for the button
        button_font = QFont("Helvetica Neue", 16)
        self.clearAll_button.setFont(button_font)

        self.clearAll_button.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                color: black;
                border: 1px inset #666666;
                border-radius: 10px;
                padding: 10px;
                margin-left: 300px;
                margin-right: 300px;
            }

            QPushButton:hover {
                background-color: #BBBBBB;
            }
            """
        )
        self.clearAll_button.clicked.connect(self.clear_text)

        buttons_layout.addWidget(self.check_button, alignment=Qt.AlignmentFlag.AlignCenter)
        buttons_layout.addWidget(self.clearAll_button, alignment=Qt.AlignmentFlag.AlignCenter)

        input_container_layout.addLayout(input_layout)
        input_container_layout.addLayout(buttons_layout)
        input_container.setLayout(input_container_layout)

        self.init_suggestions_container()
        
        # Add the input container and suggestions container to the main layout side by side
        horizontal_container = QHBoxLayout()
        horizontal_container.addWidget(input_container)
        horizontal_container.addWidget(self.suggestions_container)

        # Add the title label, input layout, and output layout to the main layout
        self.main_layout.addWidget(title_label)
        self.main_layout.addWidget(description_label)
        self.main_layout.addLayout(horizontal_container)

        # Set the layout for the central widget
        
        central_widget.setLayout(self.main_layout)

    # Dummy check grammar code for HTTP request
    # Stores sentence everytime user clicks Check Grammar
    # def check_grammar(self):
    #     sentence = self.input_text_edit.toPlainText()
    #     self.store_sentence(sentence) 

    def init_suggestions_container(self):
        # Create the suggestions container
        self.suggestions_container = QGroupBox("Suggestions")
        self.suggestions_container_layout = QVBoxLayout()
        self.suggestions_container.setStyleSheet(
            """
            QGroupBox {
                border: 1px solid #CCCCCC;
                border-radius: 10px;
            }
            """
        )
        self.suggestions_container.setLayout(self.suggestions_container_layout)
        self.suggestions_container.hide()

    # Dummy suggestion code 
    def suggestion(self):
        suggestions_text = ["Does your verb agree with your noun?", "Blah?", "Blah 2?"]
        #suggestions_text = []
        
        #self.clear_suggestions()

        if suggestions_text:
        # There are suggestions, clear any previous content and show the container
            for suggestion_text in suggestions_text:
                self.add_suggestions(suggestion_text)
                    # Show the container after adding suggestions
            self.suggestions_container.show()

        else:
            self.suggestions_container.hide()
            self.no_errors_message()
            
    # Method to display a message window when the input is error-free
    def no_errors_message(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("No Errors Found")
        msg_box.setText("No grammar errors were found in the text.")
        msg_box.exec()

    # Method to add a suggestion to the dynamic suggestion box
    # Contains a Edit, Reject, and Report button
    def add_suggestions(self, suggestion_text):
        suggestion_box = QWidget()
        suggestions_layout = QHBoxLayout()
        suggestion_label = QLabel(suggestion_text)
        suggestion_label.setStyleSheet(
            """
            QLabel {
                color: #333333;
                font-size: 14px;
                margin: 10px;
            }
            """
        )

    # Create a container for the buttons
        button_container = QWidget()
        button_container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Button formatting
        suggestion_button = """
            QPushButton {
                background-color: white;
                color: black;
                border: 1px inset #666666;
                border-radius: 10px;
                padding: 10px;
                margin-left: 10px;
                margin-right: 10px;
            }

            QPushButton:hover {
                background-color: #EEEEEE;
            }
            """
        
        button_font = QFont("Helvetica Neue", 10)           
        
        reject_button = QPushButton("Reject")
        reject_button.setFont(button_font)
        reject_button.setStyleSheet(suggestion_button)
        reject_button.clicked.connect(lambda: self.remove_suggestion(suggestion_box))
    

        # Add buttons to the button container
        button_layout = QHBoxLayout()
        button_layout.addWidget(reject_button)
        button_container.setLayout(button_layout)
        
        suggestions_layout.addWidget(suggestion_label)
        suggestions_layout.addWidget(button_container)
        # suggestions_layout.addWidget(edit_button)
        # suggestions_layout.addWidget(reject_button)
        # suggestions_layout.addWidget(report_button)
        suggestion_box.setLayout(suggestions_layout)

        self.suggestions_container_layout.addWidget(suggestion_box)

    def remove_suggestion(self, suggestion_box):
        self.suggestions_layout.removeWidget(suggestion_box)
        suggestion_box.deleteLater()
        self.suggestions.remove(suggestion_box)
    
    # Method to clear suggestions when Clear All button is clicked
    def clear_all_suggestions(self):
        for suggestion in self.suggestions:
            self.suggestions_container_layout.removeWidget(suggestion)
            suggestion.deleteLater()
        self.suggestions.clear()

    # Method to clear text from input box
    def clear_text(self):
        self.input_text_edit.clear()
        self.clear_all_suggestions()
        self.suggestions_container.hide()

    def get_incorrect_sentence(self):
        return self.input_text_edit.toPlainText()

# def check_grammar(self):
#         # Get the text from the input area
#         input_text = self.input_text_edit.toPlainText()

#         # Call the grammar checking function from the imported module
#         error_messages = check_sentences(input_text)

#         if error_messages:
#             # If there are error messages, join them into a single string
#             result_text = "\n".join(error_messages)
#        
#         else:
#             # If there are no error messages, indicate that the grammar is correct
#             result_text = "Grammar is correct!"



def main():
    app = QApplication(sys.argv)
    window = GrammarCheckerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()