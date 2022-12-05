from PyQt5 import QtWidgets, QtGui, QtTest
from PyQt5.QtCore import pyqtSignal, QThread, QObject, Qt, QRectF, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush, QTransform, QIcon
from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QLabel, QProgressBar, QAction, qApp, QWidget, \
    QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from funciones_auxiliares import nueva_posicion
import sys
from random import choice, randint
import time


class MoveMyImageEvent:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y


class Bot(QThread):
    trigger = pyqtSignal(MoveMyImageEvent)

    def __init__(self, parent, x, y, tipo, ProgressBar):
        super().__init__()
        self.progressbar = ProgressBar
        self.image = QLabel(parent)
        self.image.setGeometry(200, 100, 100, 100)
        self.image.setPixmap(QPixmap("Sprites/worker/0.png"))
        self.image.show()
        self.image.setVisible(False)
        self.trigger.connect(parent.actualizar_imagen)
        self.position = (x, y)
        self.vivo = True

        self.pixmap_mirar = QPixmap("Sprites/{}/{}.png".format(tipo, 0))

        self.pixmap_mover = [QPixmap("Sprites/{}/{}.png".format(tipo, i)) for i in range(0, 7)]

        self.pixmap_atacar = [QPixmap("Sprites/{}/{}.png".format(tipo, i)) for i in range(72, 76)]

        self.pixmap_morir = [QPixmap("Sprites/{}/{}.png".format(tipo, i)) for i in range(117, 122)]

        self.velocidad = 12
        self._angulo = 11.25

        self.pausa = False

    @property
    def angulo(self):
        return self._angulo

    @angulo.setter
    def angulo(self, valor):
        if valor >= 360:
            nuevo_valor = valor - 360
            self._angulo = valor - 360
            print(self._angulo)

        if valor < 0:

            self._angulo = 360 - abs(valor)

        else:
            self._angulo = valor

    @property
    def orientacion(self):
        return int(self.angulo // 22.5) + 1

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

        self.trigger.emit(MoveMyImageEvent(
            self.image, self.position[0], self.position[1]
        ))

    def rotar(self):
        QtTest.QTest.qWait(50)
        self.angulo += randint(0, 12)
        if self.angulo > 360:
            self.angulo -= 360
        pixmap = self.pixmap_mirar.transformed(QTransform().rotate(self.angulo).scale(-1, 1))
        self.image.setPixmap(pixmap)

    def moverse(self):

        for i in range(0, len(self.pixmap_mover)):
            self.image.setPixmap(self.pixmap_mover[i].transformed(QTransform().rotate(self.angulo).scale(-1, 1)))
            self.position = nueva_posicion(self.position, self.angulo, self.velocidad / len(self.pixmap_mover), "w")
            QtTest.QTest.qWait(50)

        self.progressbar.move(self.position[0] - 7, self.position[1] + 15)

    def run(self):
        while self.pausa is False:
            QtTest.QTest.qWait(50)
            self.rotar()
            self.moverse()


class Bomba(QThread):
    pass


class Personaje(QThread, QGraphicsPixmapItem):
    trigger = pyqtSignal(MoveMyImageEvent)

    def __init__(self, parent, x, y, ProgressBar, tipo="lobo"):
        super().__init__()
        self.progressbar = ProgressBar

        self.mover_abajo = False
        self.mover_arriba = False
        self.mover_izquierda = False
        self.mover_derecha = False

        self.image = QLabel(parent)
        self.size = 1
        self.image.setGeometry(200, 100, 100, 100)
        self.image.setPixmap(QPixmap("Sprites/lobo/0.png").transformed(QTransform().scale(-self.size, self.size)))
        self.image.show()
        self.image.setVisible(False)
        self.trigger.connect(parent.actualizar_imagen)
        self.position = (x, y)
        self.vivo = True

        self.pixmap_mirar = QPixmap("Sprites/{}/{}.png".format(tipo, 0))
        self.pixmap_mover = [QPixmap("Sprites/{}/{}.png".format(tipo, i)) for i in range(1, 4)]
        self.pixmap_atacar = [QPixmap("Sprites/{}/{}.png".format(tipo, i)) for i in range(5, 9)]
        self.pixmap_morir = [QPixmap("Sprites/{}/{}.png".format(tipo, i)) for i in range(0, 1)]

        self.velocidad = 6
        self._angulo = 11.25
        self._orientacion = 1
        self.pausa = False

    @property
    def angulo(self):
        return self._angulo

    @angulo.setter
    def angulo(self, valor):
        if valor >= 360:
            self._angulo = valor - 360
            print(self._angulo)

        if valor < 0:

            self._angulo = 360 - abs(valor)

        else:
            self._angulo = valor

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

        self.trigger.emit(MoveMyImageEvent(
            self.image, self.position[0], self.position[1]
        ))

    def rotar(self, tecla):
        QtTest.QTest.qWait(50)
        if tecla is "a":
            self.angulo -= 3
        elif tecla is "d":
            self.angulo += 3
            if self.angulo > 360:
                self.angulo -= 360

        pixmap = self.pixmap_mirar.transformed(QTransform().rotate(self.angulo).scale(-1, 1))
        self.image.setPixmap(pixmap)

    def moverse(self, tecla):

        if tecla is "w":
            for i in range(0, len(self.pixmap_mover)):
                self.image.setPixmap(self.pixmap_mover[i].transformed(QTransform().rotate(self.angulo).scale(-1, 1)))
                self.position = nueva_posicion(self.position, self.angulo, self.velocidad / len(self.pixmap_mover), "w")
                QtTest.QTest.qWait(50)

            print(self.position)



        elif tecla is "s":

            for i in range(0, len(self.pixmap_mover)):
                self.image.setPixmap(self.pixmap_mover[i].transformed(QTransform().rotate(self.angulo).scale(-1, 1)))
                self.position = nueva_posicion(self.position, self.angulo, self.velocidad / len(self.pixmap_mover), "s")
                QtTest.QTest.qWait(50)

        self.progressbar.move(self.position[0] - 7, self.position[1] + 15)

    def apretar_s(self):
        self.mover_abajo = True
        print(self.position)

    def apretar_w(self):
        self.mover_arriba = True

    def apretar_a(self):
        self.mover_izquierda = True

    def apretar_d(self):
        self.mover_derecha = True

    def soltar_s(self):
        self.mover_abajo = False

    def soltar_w(self):
        self.mover_arriba = False

    def soltar_a(self):
        self.mover_izquierda = False

    def soltar_d(self):
        self.mover_derecha = False

    def run(self):
        while self.pausa is False:
            if self.mover_abajo:
                if self.position[1] <= 450:
                    self.moverse("s")

            if self.mover_arriba:
                if self.position[1] > 0:
                    self.moverse("w")

            if self.mover_izquierda:
                self.rotar("a")

            if self.mover_derecha:
                self.rotar("d")


class Crear_bots(QObject):
    pass


class Poder(QGraphicsPixmapItem):
    def __init__(self, xy, parent=None):
        QGraphicsPixmapItem.__init__(self, parent)
        self.setPixmap(QPixmap("heart.png").transformed(QTransform().scale(-0.1, 0.1)))
        self.setFlags(QGraphicsPixmapItem.ItemIsSelectable | QGraphicsPixmapItem.ItemIsMovable)
        self.xy = xy
        self.setPos(self.xy[0], self.xy[1])
        self.angulo = 0

    def boundingRect(self):
        x, y = self.xy
        return QRectF(x * 30, y * 30, 28, 28)

    def game_update(self, keys_pressed):
        dx = 0
        dy = 0
        if Qt.Key_Left in keys_pressed:
            dx -= 5
        if Qt.Key_Right in keys_pressed:
            dx += 5
        if Qt.Key_Up in keys_pressed:
            dy -= 5
        if Qt.Key_Down in keys_pressed:
            dy += 5
        self.setPos(self.x() + dx, self.y() + dy)


def poner_bonus():
    new_bonus = Poder((randint(0, 500), randint(0, 300)))
    return new_bonus


class Tienda(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.scene = QGraphicsScene(self)
        self.poder = Poder((50, 50))
        self.poder.setPos((800 - self.poder.pixmap().width()) / 2,
                          (600 - self.poder.pixmap().height()) / 2)
        self.scene.addItem(self.poder)
        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.view.setFixedSize(800, 600)
        self.view.setSceneRect(0, 0, 800, 600)
        self.view.show()

        self.key = Qt.Key_Up

        self.timer_interval = 100
        self.timer = QTimer(self)
        self.button = QPushButton(self)
        self.button.setGeometry(100, 100, 100, 100)

    def initUI(self):
        self.setAcceptDrops(True)
        self.setWindowTitle("Tienda")
        self.setGeometry(100, 100, 800, 600)
        self.setVisible(False)

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):
        self.keys_pressed.remove(event.key())

    def timerEvent(self, event):
        self.game_update()
        self.update()

    def game_update(self):
        self.player.game_update(self.keys_pressed)
        for b in self.bullets:
            b.game_update(self.keys_pressed, self.player)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        self.button.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initGUI()

        self.stacked_layout = QtWidgets.QStackedLayout()
        self.stacked_layout.addWidget(self.select_option)
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)
        oImage = QImage("protoss.jpg")
        sImage = oImage.scaled(self.width(), self.height())  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

        COMPLETED_STYLE = """
                QProgressBar{
                   
                    text-align: center
                }

                QProgressBar::chunk {
                    background-color: red;
                    width: 4px;
                    margin: 1px;
                }
                """
        COMPLETED_STYLE1 = """
                        QProgressBar{

                            text-align: center
                        }

                        QProgressBar::chunk {
                            background-color: green;
                            width: 4px;
                            margin: 1px;
                        }
                        """

        self.progresscampeon = QProgressBar(self)
        self.progresscampeon.setGeometry(0, 0, 50, 8)
        self.progresscampeon.setValue(100)
        self.progresscampeon.setVisible(False)
        self.progresscampeon.setStyleSheet(COMPLETED_STYLE1)

        self.pbb = QProgressBar(self)
        self.pbb.setGeometry(0, 0, 50, 8)
        self.pbb.setValue(100)
        self.pbb.setVisible(False)
        self.pbb.setStyleSheet(COMPLETED_STYLE)

        self.shinobi = Personaje(self, 130, 40, self.progresscampeon)
        self.bot = Bot(self, 200, 80, "worker", self.pbb)
        self.tienda = Tienda()
        self.jugadores = []
        self.bots = []
        self.pausa = False

    def initGUI(self):
        self.button1 = QtWidgets.QPushButton("&Comenzar", self)
        self.button2 = QtWidgets.QPushButton("&Rankings", self)
        self.label1 = QtWidgets.QLabel("DCCells", self)

        self.button1.setGeometry(50, 50, 150, 200)
        self.button1.move(75, 200)
        self.button2.setGeometry(50, 50, 150, 200)
        self.button2.move(275, 200)
        self.label1.move(225, 100)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.button1)
        hbox.addWidget(self.button2)
        hbox.addStretch(1)
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.label1)
        hbox2.addStretch(1)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.initial_layout = vbox

        self.select_option = QtWidgets.QWidget()
        self.select_option.setLayout(self.initial_layout)
        self.button1.clicked.connect(self.comenzar)

        self.setGeometry(150, 100, 500, 400)
        self.setWindowTitle("DCCells")

    def comenzar(self):

        oImage = QImage("Creep_Tumor.png")
        sImage = oImage.scaled(self.width(), self.height())  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addStretch(1)

        self.comenzar_layout = QtWidgets.QVBoxLayout()
        self.comenzar_layout.addStretch(1)
        self.comenzar_layout.addLayout(hbox)
        self.comenzar_layout.addStretch(1)

        self.comenzar_option = QtWidgets.QWidget()
        self.comenzar_option.setLayout(self.comenzar_layout)
        self.stacked_layout.addWidget(self.comenzar_option)
        self.stacked_layout.setCurrentIndex(1)

        exitAct = QAction(QIcon("exit.ico"), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)

        pauseAct = QAction(QIcon("pause.png"), 'Exit', self)
        pauseAct.setShortcut("Ctrl+S")
        pauseAct.triggered.connect(self.pausar)

        storeAct = QAction(QIcon("shopcart.png"), 'Exit', self)
        storeAct.setShortcut("Ctrl+T")
        storeAct.triggered.connect(self.mostrar_tienda)

        self.scene = QGraphicsScene()

        self.toolbar = self.addToolBar('Exit')

        self.toolbar.addAction(exitAct)
        self.toolbar.addAction(pauseAct)
        self.toolbar.addAction(storeAct)
        self.toolbar.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Toolbar')
        self.show()
        self.moving_game()

    def crear_progress_bar(self):
        COMPLETED_STYLE = """
        QProgressBar{
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center
        }

        QProgressBar::chunk {
            background-color: red;
            width: 10px;
            margin: 1px;
        }
        """

    def pausar(self):
        if self.pausa is True:
            self.shinobi.pausa = False
            self.shinobi.start()
            self.pausa = False

        elif self.pausa is False:
            self.shinobi.pausa = True
            self.pausa = True

    def mostrar_tienda(self):
        self.tienda.setVisible(True)
        self.pausar()

    @staticmethod
    def actualizar_imagen(myImageEvent):
        label = myImageEvent.image
        label.move(myImageEvent.x, myImageEvent.y)

    def moving_game(self):
        self.shinobi.image.show()
        self.shinobi.image.setVisible(True)
        self.shinobi.start()
        self.progresscampeon.setVisible(True)
        self.bot.image.show()
        self.bot.image.setVisible(True)
        self.bot.start()
        self.pbb.setVisible(True)

        hbox = QtWidgets.QHBoxLayout()
        self.game_option = QtWidgets.QWidget()
        self.game_option.setLayout(hbox)
        self.stacked_layout.addWidget(self.game_option)
        self.stacked_layout.setCurrentIndex(2)

    def keyPressEvent(self, event):
        key = event.key()
        if key == 65:
            self.shinobi.apretar_a()

        elif key == 83:
            self.shinobi.apretar_s()

        elif key == 68:
            self.shinobi.apretar_d()

        elif key == 87:
            self.shinobi.apretar_w()

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == 65:
            self.shinobi.soltar_a()

        elif key == 83:
            self.shinobi.soltar_s()

        elif key == 68:
            self.shinobi.soltar_d()

        elif key == 87:
            self.shinobi.soltar_w()


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)


    sys.__excepthook__ = hook

    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
