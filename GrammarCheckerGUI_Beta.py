import sys
import nltk
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGraphicsDropShadowEffect, QMessageBox, QGroupBox, QSizePolicy, QFrame
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
import nltk
import requests
from grammar_checker import check_sentence

# # Download NLTK data
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

# # Error checking the downloads
# try:
#     nltk.download('punkt')
#     nltk.download('averaged_perceptron_tagger')
# except Exception as e:
#     print("Error occurred during NLTK data download:", e)


ACCEPT = 'accept'
REJECT = 'reject'
    

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
            """)

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
            """)
        self.check_button.clicked.connect(self.suggestion)

        """
        Add a clear all button
        """
        self.clearAll_button = QPushButton("Clear all", self)
    
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
            """)
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
            """)
        self.suggestions_container.setLayout(self.suggestions_container_layout)
        self.suggestions_container.hide()

    def suggestion(self):
        # Disable "Check Grammar" button and set input box to ReadOnly while returning suggestions
        self.check_button.setEnabled(False)
        self.input_text_edit.setReadOnly(True)

        input_text = self.input_text_edit.toPlainText()
        sentences = nltk.sent_tokenize(input_text)
        decap_sentences = []
        for s in sentences:
            decap_s = s[0].lower() + s[1:]
            decap_sentences.append((s,decap_s))

        print(decap_sentences)

        suggestions_text = []

        for s,d in decap_sentences:
            sentence_html = d.replace(' ','+')
            url = f'https://ngiyaqonda-nlg.qfrency.com/check_sentence?sentence={sentence_html}'
            print(url)
            r = requests.get(url)
            s_result = r.json()
            # s_result = check_sentence(d)
            print(s_result)
            suggestions_text.append(s_result)

            if suggestions_text:
                # There are suggestions, clear any previous content and show the container
                self.add_suggestions(s_result['suggestion'], s_result['incorrect'], s_result['correct'],s)
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

    def add_suggestions(self, suggestion_text, incorrect_phrase, correct_phrase, user_sentence):
        suggestion_style = """
            QLabel {
                color: #333333;
                font-size: 13px;
                margin: 5px 10px 0 10px;
            }
            """
        suggestions_layout = QHBoxLayout()

        suggestion_label = QLabel(suggestion_text)
        suggestion_label.setStyleSheet(suggestion_style)
        suggestion_label.setWordWrap(True)

        parts_label = QLabel(f"{incorrect_phrase} --> {correct_phrase}")
        parts_label.setWordWrap(True)
        label_font = QFont("Helvetica Neue", 5)
        parts_label.setFont(label_font)
        parts_label.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 11px;
                margin: 10px 10px 5px 10px;
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

        self.accept_button = QPushButton("Accept")
        self.accept_button.setFont(button_font)
        self.accept_button.setStyleSheet(suggestion_button)
        self.accept_button.clicked.connect(lambda: self.accept_suggestion(user_sentence,correct_phrase,incorrect_phrase))      # should call accept_suggestion     
        
        reject_button = QPushButton("Reject")
        reject_button.setFont(button_font)
        reject_button.setStyleSheet(suggestion_button)
        reject_button.clicked.connect(lambda: self.remove_suggestion(suggestion_box))

        # A container for the suggestion and correct/incorrect phrase
        suggestion_correction_container = QGroupBox() 
        suggestion_correction_container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed) #**
        suggestion_correction_container.setFixedWidth(350) 
        suggestion_correction_container.setFixedHeight(110) 
        suggestion_correction_container.setStyleSheet(
            """
            QGroupBox {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 10px;
                padding: 0px;
                margin-left: 20px;
                margin-right: 20px;
                margin-bottom: 5px;
                margin-top: 5px;

            }
            """)

        suggestion_correction_layout = QVBoxLayout()
        suggestion_correction_layout.addWidget(suggestion_label)
        suggestion_correction_layout.addWidget(parts_label)
        suggestion_correction_container.setLayout(suggestion_correction_layout)
    
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.accept_button)
        button_layout.addWidget(reject_button)
        button_container.setLayout(button_layout)
        
        suggestions_layout.addWidget(suggestion_correction_container)
        suggestions_layout.addWidget(button_container)
        self.suggestions_layout.addWidget(suggestion_box)

        suggestion_box.setLayout(suggestions_layout)

        self.suggestions.append(suggestion_box)
        self.suggestions_container_layout.addWidget(suggestion_box)

    # To retrieve harvest, get https://ngiyaqonda-nlg.qfrency.com/retrieve_harvest
    def submit_suggestion(self,user_sentence=None,correct=None,incorrect=None,user_classification=None):
        user_sentence_html = 'user_sentence='+user_sentence.replace(' ','+')+'&' if user_sentence else ''
        correct_html = 'correct='+correct.replace(' ','+')+'&' if correct else ''
        incorrect_html = 'incorrect='+incorrect.replace(' ','+')+'&' if incorrect else '' 
        user_classification_html = 'user_classification='+user_classification.replace(' ','+') if user_classification else ''
        url = f'https://ngiyaqonda-nlg.qfrency.com/harvest?{user_sentence_html}{correct_html}{incorrect_html}{user_classification_html}'
        print(url)
        requests.get(url)

    def accept_suggestion(self,user_sentence=None,correct=None,incorrect=None):
        self.submit_suggestion(user_sentence,correct,incorrect,ACCEPT)

        # Turn accept button black and disable once clicked
        self.accept_button.setStyleSheet(           
            """
            QPushButton {
                background-color: black;
                color: white;
                border: 1px inset #666666;
                border-radius: 10px;
                padding: 10px 10px;
                margin-left: 2px;
                margin-right: 10px;
            }
            """)
        self.accept_button.setEnabled(False)

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
