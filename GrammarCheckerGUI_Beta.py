import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLabel, QGraphicsDropShadowEffect, QMessageBox
from PyQt6.QtGui import QFont, QColor, QTextCursor, QTextCharFormat, QPalette, QTextBlockFormat
from PyQt6.QtCore import Qt

class GrammarCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and dimensions
        self.setWindowTitle("isiZulu Grammar Checker")
        window_width = 800
        window_height = 450

        # Calculate center of user's screen
        user_screen = QApplication.primaryScreen()
        screen_geometry = user_screen.geometry() # Access user's desktop and retrieve screen geometry

        x = (screen_geometry.width() - window_width) // 2 # Screen width - window width // 2
        y = (screen_geometry.height() - window_height) // 2 # Screen height - window height // 2
        
        # Set window position and size
        self.setGeometry(x, y, window_width, window_height)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: white;")

        # Create a layout for the central widget
        main_layout = QVBoxLayout()

        # Create a title label
        title_label = QLabel("isiZulu Grammar Checker", self)

        # Create a QFont object using "Inter" font family
        title_font = QFont("Helvetica Neue", 50)
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
        description_label.setStyleSheet("""
            QLabel {
                color: black;                
            }

        """)

        # Create a layout for the input text area and button
        input_layout = QVBoxLayout()

        # Create a text input area (QTextEdit) for input text
        self.input_text_edit = QTextEdit (self) #grammartextedit
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

        # input_layout.addWidget(self.input_text_edit)

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
        self.check_button.clicked.connect(self.grammar_check)

        input_layout.addWidget(self.input_text_edit, alignment=Qt.AlignmentFlag.AlignCenter)
        input_layout.addWidget(self.check_button)

       
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
                background-color: #666666;
            }
            """
        )
        self.clearAll_button.clicked.connect(self.clear_text)

        input_layout.addWidget(self.clearAll_button)

        # Add the title label, input layout, and output layout to the main layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(description_label)
        main_layout.addLayout(input_layout)

        # Set the layout for the central widget
        central_widget.setLayout(main_layout)

    # def check_grammar(self):
    #     # Get the text from the input area
    #     input_text = self.input_text_edit.toPlainText()

    #     # Perform grammar checking: We will have to work on this part
    #     # For now we assume the grammar is correct
    #     is_grammar_correct = True

    #     if is_grammar_correct:
    #         result_text = "Grammar is correct!"
    #     else:
    #         # In case of errors
    #         result_text = "Grammar has errors. Suggestions: [Suggestions go here]"

    #     # Display the result or suggestions in the output text area
    #     self.output_text_edit.setPlainText(result_text)

    def grammar_check(self):
        user_input = self.input_text_edit.toPlainText()
        words = user_input.split()

        for word in words:
            if not self.word_correct(word):
                self.incorrect_underline(word)

    def word_correct(self, word):
        return False
    
    def incorrect_underline(self, word):
        cursor = self.input_text_edit.textCursor()
        format = QTextCharFormat()
        format.setUnderlineColor(QColor("red"))  # Set the underline color to red
        format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.DashUnderline)  # Set the underline style
        cursor.setPosition(self.input_text_edit.toPlainText().index(word))
        cursor.setPosition(cursor.position() + len(word), QTextCursor.MoveMode.KeepAnchor)
        cursor.mergeCharFormat(format)

    def clear_text(self):
        self.input_text_edit.clear()

def main():
    app = QApplication(sys.argv)
    window = GrammarCheckerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()