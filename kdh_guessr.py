import cv2, json, random, sys, time
import decord, numpy as np

import PyQt6.QtCore as core, PyQt6.QtGui as gui, PyQt6.QtWidgets as widgets

random.seed(time.time())

KDH_PATH = 'K-Pop Demon Hunters.mkv'
SAVE_FILE = 'kdh_guessr_save.json'
START_TIMESTAMP = 0 * 60 + 33
END_TIMESTAMP = 1 * 3600 + 28 * 60 + 39

class KDH_Guessr:
    def __init__(self, path: str) -> None:
        self.vr = decord.VideoReader(path)
        fps = self.vr.get_avg_fps()
        self.minFrameIndex = round(START_TIMESTAMP * fps)
        self.maxFrameIndex = round(END_TIMESTAMP * fps)
        self.length = END_TIMESTAMP - START_TIMESTAMP
        self.timestamps = self.vr.get_frame_timestamp(range(len(self.vr))).mean(-1)

    def pick(self) -> tuple[np.ndarray, float]:
        i = random.randint(self.minFrameIndex, self.maxFrameIndex - 1)
        frame = self.vr[i]
        minutestamp = self.timestamps[i] / 60
        return frame.asnumpy(), minutestamp
    
    def save(self, frame: np.ndarray, path: str) -> None:
        cv2.imwrite(path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        
class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.score = 0
    
class Game:
    def __init__(self, kdh: KDH_Guessr) -> None:
        self.rounds = []
        self.kdh = kdh

    def register_round(self, guesses: list[tuple[Player, int]], timestamp: float) -> list[tuple[Player, int, float]]:
        results = []
        for player, guess in guesses:
            roundScore, diff = self.handle_guess(player, guess, timestamp)
            results.append((player, roundScore, diff))
        self.rounds.append(results)
        return results
    
    def handle_guess(self, player: Player, guess: int, timestamp: float) -> tuple[int, float]:
        diff = abs(guess - timestamp)
        maxDiff = max(timestamp, self.kdh.length - timestamp)
        relativeScore = diff * 1000 / maxDiff
        score = round(max(0, 1000 - relativeScore))
        player.score += score
        return score, round(diff, 2)
    
    def scoreboard(self) -> list[tuple[str, int]]:
        players = [player for player, _, _ in self.rounds[-1]]
        return sorted([(player.name, player.score) for player in players], key=lambda x: x[1], reverse=True)
    
    def ser(self) -> dict:
        return {
            'rounds': [[(player.name, roundScore, diff) for player, roundScore, diff in round] for round in self.rounds],
            'scoreboard': self.scoreboard()
        }

class UI(widgets.QStackedWidget):
    addPlayer = core.pyqtSignal()
    removePlayer = core.pyqtSignal()
    newGame = core.pyqtSignal()
    submitGuesses = core.pyqtSignal()
    nextRound = core.pyqtSignal()
    gameOver = core.pyqtSignal()
    returnToLobby = core.pyqtSignal()

    # INITIALIZATION

    def __init__(self, kdh: KDH_Guessr) -> None:
        super().__init__()
        self.kdh = kdh
        self.game = None
        self.currentStamp = None
        self.playerLineEdits = [PlayerLineEdit(0)]
        self.initUI()
        self.initEvents()
    
    def initUI(self) -> None:
        # LOBBY UI
        playersGroupBox = widgets.QGroupBox('Players')

        self.playersLayout = widgets.QVBoxLayout()
        playersGroupBox.setLayout(self.playersLayout)
        self.playersLayout.addWidget(self.playerLineEdits[0])

        self.removePlayerButton = widgets.QPushButton('Remove last player')
        self.removePlayerButton.clicked.connect(self.removePlayer.emit)
        self.removePlayerButton.setEnabled(False)
        self.addPlayerButton = widgets.QPushButton('Add new player')
        self.addPlayerButton.clicked.connect(self.addPlayer.emit)

        self.startGameButton = widgets.QPushButton('Start game')
        self.startGameButton.clicked.connect(self.newGame.emit)

        self.lobbyLayout = widgets.QVBoxLayout()
        self.lobbyLayout.addWidget(playersGroupBox)
        self.lobbyLayout.addWidget(self.removePlayerButton)
        self.lobbyLayout.addWidget(self.addPlayerButton)
        self.lobbyLayout.addWidget(self.startGameButton)

        # GAME UI
        self.imageLabel = widgets.QLabel()

        self.guessesGroupBox = widgets.QGroupBox('Guesses')
        self.submitGuessesButton = widgets.QPushButton('Submit guesses')
        self.submitGuessesButton.clicked.connect(self.submitGuesses.emit)

        # scoreboard


        self.nextRoundButton = widgets.QPushButton('Next round')
        self.nextRoundButton.clicked.connect(self.nextRound.emit)
        self.nextRoundButton.setEnabled(False)

        panelLayout = widgets.QHBoxLayout()
        panelLayout.addWidget(self.nextRoundButton)
        self.gamelayout = widgets.QVBoxLayout()
        self.gamelayout.addWidget(self.imageLabel)
        self.gamelayout.addLayout(panelLayout)

        # ---
        lobbyWidget = widgets.QWidget()
        lobbyWidget.setLayout(self.lobbyLayout)
        gameWidget = widgets.QWidget()
        gameWidget.setLayout(self.gamelayout)
        self.addWidget(lobbyWidget)
        self.addWidget(gameWidget)

    def initEvents(self) -> None:
        self.addPlayer.connect(self.add_player)
        self.removePlayer.connect(self.remove_player)
        self.newGame.connect(self.start_game)
        #self.submitGuesses.connect(self.submit_guesses)
        self.nextRound.connect(self.next_round)

    # UI

    def set_image(self, frame: np.ndarray) -> None:
        height, width, _ = frame.shape
        image = gui.QImage(frame.data, width, height, gui.QImage.Format.Format_RGB888)
        pixmap = gui.QPixmap.fromImage(image).scaledToWidth(1080, core.Qt.TransformationMode.SmoothTransformation)
        self.imageLabel.setPixmap(pixmap)

    # GAME EVENTS

    def add_player(self) -> None:
        self.playerLineEdits.append(PlayerLineEdit(len(self.playerLineEdits)))
        self.playersLayout.addWidget(self.playerLineEdits[-1])
        if len(self.playerLineEdits) > 1:
            self.removePlayerButton.setEnabled(True)

    def remove_player(self) -> None:
        if len(self.playerLineEdits) > 1:
            ple = self.playerLineEdits.pop()
            ple.setParent(None)
            ple.deleteLater()
        if len(self.playerLineEdits) == 1:
            self.removePlayerButton.setEnabled(False)

    def start_game(self) -> None:
        print('Starting game with players:', [ple.get_player().name for ple in self.playerLineEdits])
        self.game = Game(self.kdh)
        players = self.get_players()

        self.setCurrentIndex(1)
        self.nextRoundButton.setEnabled(True)
        self.nextRound.emit()

    def next_round(self) -> None:
        assert self.game is not None, 'Game has not been started yet'
        frame, minutestamp = self.game.kdh.pick()
        self.set_image(frame)
        self.currentStamp = minutestamp

    # DATA

    def get_players(self) -> list[Player]:
        return [ple.get_player() for ple in self.playerLineEdits]

class PlayerLineEdit(widgets.QWidget):
    def __init__(self, index: int) -> None:
        super().__init__()
        self.index = index
        self.initUI()
    
    def initUI(self) -> None:
        self.nameLineEdit = widgets.QLineEdit()
        self.nameLineEdit.setPlaceholderText(f'Player{self.index + 1}')
        layout = widgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.nameLineEdit)
        self.setLayout(layout)

    def get_player(self) -> Player:
        name = self.nameLineEdit.text().strip()
        if not name:
            name = f'Player{self.index + 1}'
        return Player(name)
    
class PlayerGuessLineEdit(widgets.QWidget):
    def __init__(self, player: Player) -> None:
        super().__init__()
        self.player = player
        self.initUI()
    
    def initUI(self) -> None:
        self.nameLabel = widgets.QLabel(self.player.name)
        self.guessLineEdit = widgets.QSpinBox()
        self.guessLineEdit.setRange(round(START_TIMESTAMP / 60), round(END_TIMESTAMP / 60))

        layout = widgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.nameLabel)
        layout.addStretch()
        layout.addWidget(self.guessLineEdit)

        self.setLayout(layout)

    def get_guess(self) -> tuple[Player, int]:
        guess = self.guessLineEdit.value()
        return self.player, guess

if __name__ == '__main__':
    app = widgets.QApplication(sys.argv)
    window = widgets.QMainWindow()
    window.setWindowTitle('KDH Guessr')

    window.setCentralWidget(UI(KDH_Guessr(KDH_PATH)))

    window.show()
    app.exec()