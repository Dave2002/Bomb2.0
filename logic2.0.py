import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class GameSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.game_modes = ["Bomb", "Flag", "Bunker"]
        self.difficulties = ["Easy", "Medium", "Hard"]
        self.times = ["5min", "10min", "15min"]

        self.selection_index = 0

        self.selected_game_mode = None
        self.selected_difficulty = None
        self.selected_time = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Press 'Enter' to start selecting Game Mode")

        layout.addWidget(self.label)

        self.setLayout(layout)
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('Game Selector')
        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.select_next()
        elif event.key() == Qt.Key_Backspace:
            self.goBack()

    def select_next(self):
        if self.selection_index == 0:
            self.select_game_mode()
        elif self.selection_index == 1:
            self.select_difficulty()
        elif self.selection_index == 2:
            self.select_time()

    def select_game_mode(self):
        game_mode, ok = GameSelectorDialog.get_selection("Select Game Mode", self.game_modes)
        if ok:
            self.selected_game_mode = game_mode
            self.selection_index += 1
            self.update_label()

    def select_difficulty(self):
        difficulty, ok = GameSelectorDialog.get_selection("Select Difficulty", self.difficulties)
        if ok:
            self.selected_difficulty = difficulty
            self.selection_index += 1
            self.update_label()

    def select_time(self):
        time, ok = GameSelectorDialog.get_selection("Select Time", self.times)
        if ok:
            self.selected_time = time
            self.update_label()

    def goBack(self):
        if self.selection_index > 0:
            self.selection_index -= 1
        self.update_label()

    def update_label(self):
        if self.selection_index == 0:
            text = "Press 'Enter' to select Game Mode"
        elif self.selection_index == 1:
            text = f"Selected Game Mode: {self.selected_game_mode}\nPress 'Enter' to select Difficulty"
        elif self.selection_index == 2:
            text = f"Selected Game Mode: {self.selected_game_mode}\nSelected Difficulty: {self.selected_difficulty}\nPress 'Enter' to select Time"
        else:
            text = f"Selected Game Mode: {self.selected_game_mode}\nSelected Difficulty: {self.selected_difficulty}\nSelected Time: {self.selected_time}"

        self.label.setText(text)

class GameSelectorDialog(QWidget):
    @staticmethod
    def get_selection(title, options):
        selection, ok = GameSelectorDialog.show_dialog(title, options)
        return selection, ok

    @staticmethod
    def show_dialog(title, options):
        dialog = GameSelectorDialog(title, options)
        result = dialog.exec_()
        return dialog.selected_item, result == dialog.Accepted

    def __init__(self, title, options):
        super().__init__()

        self.selected_item = None

        self.init_ui(title, options)

    def init_ui(self, title, options):
        layout = QVBoxLayout()

        self.label = QLabel(title)
        layout.addWidget(self.label)

        self.list_widget = QLabel("\n".join(options))
        layout.addWidget(self.list_widget)

        self.setLayout(layout)
        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle(title)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.move_selection(-1)
        elif event.key() == Qt.Key_Down:
            self.move_selection(1)
        elif event.key() == Qt.Key_Return:
            self.accept()
        elif event.key() == Qt.Key_Backspace:
            self.reject()

    def move_selection(self, direction):
        current_row = self.list_widget.text().split('\n').index(self.selected_item) if self.selected_item else -1
        new_row = (current_row + direction) % len(self.list_widget.text().split('\n'))
        self.selected_item = self.list_widget.text().split('\n')[new_row]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameSelector()
    sys.exit(app.exec_())
