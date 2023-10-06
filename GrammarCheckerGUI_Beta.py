import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class GrammarCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        """
        Setting up the window and central widget
        And adding formatting
        """

        # Set window title and dimensions
        self.setWindowTitle("isiZulu Grammar Checker")
        window_width = 800
        window_height = 750

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

        # Create a layout for the central widget
        main_layout = QVBoxLayout()

        """
        Create a title for the application
        """

        # Create a title label
        title_label = QLabel("isiZulu Grammar Checker", self)

        # Create a QFont object using "Inter" font family
        title_font = QFont("Helvetica Neue", 40)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            background-color: #FFFFFF;
            color: black;
            padding: 0px;
            """)
        
        """
        Creating a space to add a text description
        * Note that the copy is not final, I just added whatever sounded okay
        """

        # Create app description
        description_label = QLabel("Start typing below for error-free grammar.", self)

        # Customise text
        description_font = QFont("Helvetica Neue", 16)
        description_label.setFont(description_font)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet("""
            QLabel {
                color: black;
                padding-top: 0px;
                padding-bottom: 15px;                  
            }
            """
            )
        
        """
        Create a textbox for user input
        And add formatting to create a more "modern" feel
        """

        # Create a layout for the input text area and button
        input_layout = QVBoxLayout()

        # Create an input widget and layout
        input_widget = QWidget()
        input_widget_layout = QVBoxLayout()

        # Create a text input area (QTextEdit) for input text
        self.input_text_edit = QTextEdit(self)
        input_text_font = QFont("Helvetica Neue", 16)
        self.input_text_edit.setFont(input_text_font)
        self.input_text_edit.setFixedWidth(500)  # Set a fixed width
        self.input_text_edit.setFixedHeight(150)  # Set a fixed height
        self.input_text_edit.setStyleSheet(
            """
            color: black;
            background-color: white;
            border: 0.5px solid #808080;
            border-radius: 10px; /* Create rounded corners
            font-size: 16px;
            """
        )

        # Create a 3D "shadow effect" behind the textbox
        input_area_shadow = QGraphicsDropShadowEffect(self)
        input_area_shadow.setColor(QColor(128, 128, 128, 200))
        input_area_shadow.setBlurRadius(20)
        input_area_shadow.setXOffset(7)
        input_area_shadow.setYOffset(7)
        self.input_text_edit.setGraphicsEffect(input_area_shadow)

        # Align input widget to the center of the screen
        input_widget_layout.addWidget(self.input_text_edit)

        """
        Create a button to check the grammar
        """

        # Create a button for grammar check
        self.check_button = QPushButton("Check my grammar")

        # Set the styling for the button
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

        # Connect the clear_text function to the clearAll_button when clicked
        self.check_button.clicked.connect(self.check_grammar)

        # Add check button to input layout
        input_layout.addWidget(self.check_button)
        
        # Set layout of input_widget to input_widget_layout
        input_widget.setLayout(input_widget_layout)

        # Add input_widget to input_layout
        input_layout.addWidget(input_widget)

        """
        Create an output box
        ** WIP to add functionality discussed in meeting
        """

        # Create a layout for the output text area
        output_layout = QHBoxLayout()

        # Create a text output area (QTextEdit) for displaying results or suggestions
        self.output_text_edit = QTextEdit(self)
        output_text_font = QFont("Helvetica Neue", 16)
        self.output_text_edit.setFont(output_text_font)
        self.output_text_edit.setReadOnly(True)  # Make it read-only
        self.output_text_edit.setFixedWidth(500)  # Set a fixed width
        self.output_text_edit.setFixedHeight(150)  # Set a fixed height
        self.output_text_edit.setStyleSheet(
            """
            color: black;
            background-color: white;
            border: 0.5px solid #808080;
            border-radius: 10px; /* Create rounded corners
            padding: 40px; /* Add some padding for space */
            font-size: 16px;
            """
        )

        # Create a 3D "shadow effect" behind the textbox
        output_area_shadow = QGraphicsDropShadowEffect(self)
        output_area_shadow.setColor(QColor(128, 128, 128, 200))
        output_area_shadow.setBlurRadius(20)
        output_area_shadow.setXOffset(7)
        output_area_shadow.setYOffset(7)
        self.output_text_edit.setGraphicsEffect(output_area_shadow)

        # Create the second text output area for additional content (adjust dimensions as needed)
        self.additional_text_edit = QTextEdit(self)
        additional_text_font = QFont("Helvetica Neue", 16)
        self.additional_text_edit.setFont(additional_text_font)
        self.additional_text_edit.setReadOnly(True)  # Make it read-only
        self.additional_text_edit.setFixedWidth(500)  # Set a fixed width
        self.additional_text_edit.setFixedHeight(150)  # Set a fixed height
        self.additional_text_edit.setStyleSheet(
            """
            color: black;
            background-color: white;
            border: 0.5px solid #808080;
            border-radius: 10px; /* Create rounded corners */
            padding: 40px; /* Add some padding for space */
            font-size: 16px;
            """
        )

        # Create a 3D "shadow effect" behind the second textbox
        additional_area_shadow = QGraphicsDropShadowEffect(self)
        additional_area_shadow.setColor(QColor(128, 128, 128, 200))
        additional_area_shadow.setBlurRadius(20)
        additional_area_shadow.setXOffset(7)
        additional_area_shadow.setYOffset(7)
        self.additional_text_edit.setGraphicsEffect(additional_area_shadow)

        # Add both text areas to the output layout
        output_layout.addWidget(self.output_text_edit)
        output_layout.addWidget(self.additional_text_edit)

        #output_layout.addWidget(self.output_text_edit, alignment=Qt.AlignmentFlag.AlignCenter)

        # # Create a button for copying text with an icon
        # self.copy_button = QPushButton("Copy text")

        # # Set the font for the button
        # button_font = QFont("Helvetica Neue", 16)
        # self.copy_button.setFont(button_font)

        # self.copy_button.setStyleSheet(
        #     """
        #     QPushButton {
        #         background-color: white;
        #         color: black;
        #         border: 1px inset #666666;
        #         border-radius: 10px;
        #         padding: 10px;
        #         margin-left: 300px;
        #         margin-right: 300px;
        #     }

        #     QPushButton:hover {
        #         background-color: #666666;
        #     }
        #     """
        # )
        # self.copy_button.clicked.connect(self.copy_text)

        # output_layout.addWidget(self.copy_button)

        """
       Creating a button to clear all text
       Link to clear_text functioin
       """
       
       # Create a QPushButton widget labelled "Clear text"
        self.clearAll_button = QPushButton("Clear text", self)
    
        # Set the styling for the button
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

        # Connect the clear_text function to the clearAll_button when clicked
        self.clearAll_button.clicked.connect(self.clear_text)

        # # Add clear_All button to the output area
        # output_layout.addWidget(self.clearAll_button)

        """
        Creating two widgets on the main layout
        The top is white, the bottom is black
        Places exisitng widgets on the top or bottom half
        """

        # Create a widget for the top half (white background)
        top_half_widget = QWidget(self)
        top_half_widget.setStyleSheet("background-color: white")

        # Create a widget for the bottom half (black background)
        bottom_half_widget = QWidget(self)
        bottom_half_widget.setStyleSheet("background-color: black")

        # Create layouts for top and bottom halves
        top_layout = QVBoxLayout()
        bottom_layout = QVBoxLayout()

        # Add widgets to layouts
        top_layout.addWidget(title_label)
        top_layout.addWidget(description_label)
        top_layout.addWidget(self.input_text_edit, alignment=Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.check_button)

        bottom_layout.addWidget(self.output_text_edit, alignment=Qt.AlignmentFlag.AlignCenter)
        bottom_layout.addWidget(self.additional_text_edit, alignment=Qt.AlignmentFlag.AlignCenter)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.clearAll_button)
        bottom_layout.addLayout(button_layout)

        # Set layouts for top and bottom halves
        top_half_widget.setLayout(top_layout)
        bottom_half_widget.setLayout(bottom_layout)

        # Create a layout for the central widget
        main_layout = QVBoxLayout()

        # Add top and bottom halves to main layout
        main_layout.addWidget(top_half_widget)
        main_layout.addWidget(bottom_half_widget)

        # Set the layout for the central widget
        central_widget.setLayout(main_layout)

        """
        Functions 
        """

    def check_grammar(self):
        # Get the text from the input area
        input_text = self.input_text_edit.toPlainText()

        # Perform grammar checking: We will have to work on this part
        # For now we assume the grammar is correct
        is_grammar_correct = True

        if is_grammar_correct:
            result_text = "Grammar is correct!"
        else:
            # In case of errors
            result_text = "Grammar has errors. Suggestions: [Suggestions go here]"

        # Display the result or suggestions in the output text area
        self.output_text_edit.setPlainText(result_text)

    # A function to clear user text from the screen
    def clear_text(self):
        self.input_text_edit.clear()

    # In case we want a copy function
    # def copy_text(self):
    #     text_to_copy = self.output_text_edit.toPlainText()

    #     clipboard = QApplication.clipboard()

    #     clipboard.setText(text_to_copy)

def main():
    app = QApplication(sys.argv)
    window = GrammarCheckerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()