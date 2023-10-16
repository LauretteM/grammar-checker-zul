import sys
import nltk
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGraphicsDropShadowEffect, QMessageBox, QGroupBox, QSizePolicy, QFrame
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from nltk.tokenize import sent_tokenize, word_tokenize
from enum import Enum

# Download NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Error checking the downloads
try:
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
except Exception as e:
    print("Error occurred during NLTK data download:", e)
    
# tokenize the input text into sentences
def tokenize_and_tag(input_text):
    sentences = sent_tokenize(input_text)
    
    # Tokenize each sentence into words and perform part-of-speech tagging
    tokenized_and_tagged_text = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        pos_tags = nltk.pos_tag(words) # perform part-of-speech tagging
        tokenized_and_tagged_text.append(pos_tags)
    
    return tokenized_and_tagged_text

class GrammarResult(Enum):
    CORRECT = "This sentence looks good."
    NO_ERRORS_FOUND = "Could not identify agreement errors."

    QUAL_ADJ_AGREEMENT = "Check the agreement between the noun/pronoun and its qualifying adjective."
    QUAL_ID_NP_AGREEMENT = "Check the agreement between the noun/pronoun and its qualifying noun."
    QUAL_ASSOC_NP_AGREEMENT = "Check the agreement between the noun/pronoun and its qualifying associative noun."
    QUAL_LOC_AGREEMENT = "Check the agreement between the noun/pronoun and its qualifying locative expression."
    QUAL_VERB_AGREEMENT = "Check the agreement between the noun/pronoun and its qualifying verb phrase."
    
    SUBJ_ADJ_AGREEMENT = "Check the agreement between the noun/pronoun and the predicative adjective."
    SUBJ_ID_NP_AGREEMENT = "Check the agreement between the noun/pronoun and the predicate noun."
    SUBJ_ASSOC_NP_AGREEMENT = "Check the agreement between the noun/pronoun and the associative noun."
    SUBJ_LOC_AGREEMENT = "Check the agreement between the noun/pronoun and the locative predicate."
    SUBJ_VERB_AGREEMENT = "Check the agreement between the subject and verb."

class GrammarCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and dimensions
        self.setWindowTitle("isiZulu Grammar Checker")
        window_width = 1400
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
            margin-top: 20px;
            margin-bottom: 7px;
        """)

        # Create app description
        description_label = QLabel("Start typing below for error-free grammar.", self)

        # Customize app description
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
            border: 0.5px solid #CCCCCC;
            border-radius: 10px; /* Create rounded corners */
            font-size: 16px;
            margin-left: 30px;
            margin-right: 30px;
            margin-bottom: 2px;
            margin-top: 10px;
            """
        )

        # Roné, if you see this, please check how you think this looks with and without the shading by uncommenting the code below :) I'm torn. Lmk what you think
        # Genévieve, I like the shading and uncommented it but let me know if you prefer it without.
        input_area_shadow = QGraphicsDropShadowEffect(self)
        input_area_shadow.setColor(QColor(128, 128, 128, 128))
        input_area_shadow.setBlurRadius(40)
        input_area_shadow.setXOffset(7)
        input_area_shadow.setYOffset(7)
        self.input_text_edit.setGraphicsEffect(input_area_shadow)

        input_layout.addWidget(self.input_text_edit, alignment=Qt.AlignmentFlag.AlignCenter)

        """
        Create a dynamic "Suggestions section.
        """

        self.suggestions_layout = QHBoxLayout()
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
                margin-bottom: 0x;
                margin-top: 5px;
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
        self.clearAll_button = QPushButton("Clear All", self)
    
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
                margin-bottom: 20px;
                margin-top: 0px;

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

    def init_suggestions_container(self):
        # Create the suggestions container
        self.suggestions_container = QGroupBox()
        self.suggestions_container_layout = QVBoxLayout()
        self.suggestions_container.setFixedWidth(600)  # Set a fixed width
        self.suggestions_container.setFixedHeight(450)  # Set a fixed height
        self.suggestions_container.setStyleSheet(
            """
            QGroupBox {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 10px;
                padding: 0px;
                margin-left: 10px;
                margin-right: 100px;
                margin-bottom: 20px;
                margin-top: 5px;

            }
            """
        )
        self.suggestions_container.setLayout(self.suggestions_container_layout)
        self.suggestions_container.hide()

    def suggestion(self):
        # Disable "Check Grammar" button and set input box to ReadOnly while returning suggestions
        self.check_button.setEnabled(False)
        self.input_text_edit.setReadOnly(True)

        suggestions_text = ["Suggestion 1", "Suggestion 2", "Suggestion 3"]
        incorrect_phrase = "Test 1"
        correct_phrase = "Test 2"

        if suggestions_text:
            # There are suggestions, clear any previous content and show the container
            for suggestion_text in suggestions_text:
                self.add_suggestions(suggestion_text, incorrect_phrase, correct_phrase)
            # Show the container after adding suggestions
            self.suggestions_container.show()
        else:
            self.suggestions_container.hide()
            self.no_errors_message()

    def no_errors_message(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("No Errors Found")
        msg_box.setText("No grammar errors were found in the text.")
        msg_box.exec()

    def add_suggestions(self, suggestion_text, incorrect_phrase, correct_phrase):
        suggestion_style = """
            QLabel {
                color: #333333;
                font-size: 14px;
                margin: 10px;
            }
            """
        suggestions_layout = QHBoxLayout()

        suggestion_label = QLabel(suggestion_text)
        suggestion_label.setStyleSheet(suggestion_style)

        parts_label = QLabel(f"{incorrect_phrase} --> {correct_phrase}")
        label_font = QFont("Helvetica Neue", 5)
        parts_label.setFont(label_font)
        parts_label.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 11px;
                margin: 10px;
            }
            """)

        button_container = QWidget()
        button_container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        suggestion_button = """
            QPushButton {
                background-color: white;
                color: black;
                border: 1px inset #666666;
                border-radius: 10px;
                padding: 10px 10px;
                margin-left: 2px;
                margin-right: 10px;
            }

            QPushButton:hover {
                background-color: #EEEEEE;
            }
            """
        suggestion_box = QWidget()

        button_font = QFont("Helvetica Neue", 10) 

        accept_button = QPushButton("Accept")
        accept_button.setFont(button_font)
        accept_button.setStyleSheet(suggestion_button)
        accept_button.clicked.connect(lambda: None)          
        
        reject_button = QPushButton("Reject")
        reject_button.setFont(button_font)
        reject_button.setStyleSheet(suggestion_button)
        reject_button.clicked.connect(lambda: self.remove_suggestion(suggestion_box))
    
        button_layout = QVBoxLayout()
        button_layout.addWidget(accept_button)
        button_layout.addWidget(reject_button)
        button_container.setLayout(button_layout)
        
        suggestions_layout.addWidget(suggestion_label)
        suggestions_layout.addWidget(parts_label)
        suggestions_layout.addWidget(button_container)
        self.suggestions_layout.addWidget(suggestion_box)

        suggestion_box.setLayout(suggestions_layout)

        self.suggestions.append(suggestion_box)
        self.suggestions_container_layout.addWidget(suggestion_box)

    def remove_suggestion(self, suggestion_box):
        self.suggestions_layout.removeWidget(suggestion_box)
        suggestion_box.deleteLater()
        self.suggestions.remove(suggestion_box)

    def clear_all_suggestions(self):
        for suggestion in self.suggestions:
            self.suggestions_container_layout.removeWidget(suggestion)
            suggestion.deleteLater()
        self.suggestions.clear()

        self.check_button.setEnabled(True)
        self.input_text_edit.setReadOnly(False)

    def clear_text(self):
        self.input_text_edit.clear()
        self.clear_all_suggestions()
        self.suggestions_container.hide()

def main():
    app = QApplication(sys.argv)
    window = GrammarCheckerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
