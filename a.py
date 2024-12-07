import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QPushButton,
    QFileDialog,
    QGraphicsItem
)
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QPointF, QRect
from PyQt6.QtGui import QPixmap, QPainter, QPen, QImage
from PIL import Image


class MovingObjectPhoto(QGraphicsPixmapItem):
    def __init__(self, path, id):
        super().__init__()
        self.setPixmap(QPixmap(path))
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)  # Включаем поддержку выделения
        self._show_border = False
        self._is_selected = False  # Флаг для отслеживания выделения
        self.id = id  # Уникальный идентификатор изображения

    # mouse hover event
    def hoverEnterEvent(self, event):
        QApplication.instance().setOverrideCursor(Qt.CursorShape.PointingHandCursor)
        self._show_border = True
        self.update()  # Обновляем элемент, чтобы перерисовать его с рамкой

    def hoverLeaveEvent(self, event):
        QApplication.instance().restoreOverrideCursor()
        if not self._is_selected:
            self._show_border = False
            self.update()  # Обновляем элемент, чтобы убрать рамку

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self._show_border or self._is_selected:
            rect = self.boundingRect()
            pen = QPen(Qt.GlobalColor.blue)
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawRect(rect)

    # Обработчик нажатия левой кнопки мыши
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_selected = True
            self._show_border = True
            self.update()  # Обновляем элемент, чтобы показать рамку
        super().mousePressEvent(event)

    # Обработчик отпускания левой кнопки мыши
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_selected = False
            self._show_border = False
            self.update()  # Обновляем элемент, чтобы скрыть рамку
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            original_cursor_position = event.lastScenePos()
            updated_cursor_position = event.scenePos()

            original_position = self.scenePos()

            updated_cursor_x = updated_cursor_position.x() - original_cursor_position.x() + original_position.x()
            updated_cursor_y = updated_cursor_position.y() - original_cursor_position.y() + original_position.y()
            self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
        super().mouseMoveEvent(event)


class GraphicView(QGraphicsView):
    def __init__(self, parent):
        scene = QGraphicsScene()
        super().__init__(scene, parent)

        self.setBackgroundBrush(Qt.GlobalColor.white)

        self.scene = scene
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 1, 1)

        self.next_id = 0  # Идентификатор для новых изображений
        self.images = {}  # Словарь для хранения всех изображений

        # Кнопка для добавления изображения
        # add_button = QPushButton("Add Image")
        # add_button.clicked.connect(self.add_image)
        # self.add_button_proxy = self.scene.addWidget(add_button)
        # self.add_button_proxy.setPos(0, 0)

        # Кнопка для удаления изображения
        # remove_button = QPushButton("Remove Image")
        # remove_button.clicked.connect(self.remove_image)
        # self.remove_button_proxy = self.scene.addWidget(remove_button)
        # self.remove_button_proxy.setPos(80, 0)
        #
        # # Кнопки для изменения масштаба
        # increase_button = QPushButton("Increase Scale")
        # increase_button.clicked.connect(self.increase_scale)
        # self.increase_button_proxy = self.scene.addWidget(increase_button)
        # self.increase_button_proxy.setPos(160, 0)
        #
        # decrease_button = QPushButton("Decrease Scale")
        # decrease_button.clicked.connect(self.decrease_scale)
        # self.decrease_button_proxy = self.scene.addWidget(decrease_button)
        # self.decrease_button_proxy.setPos(240, 0)

    def add_image(self, file_path):
        # file_path, _ = QFileDialog.getOpenFileName(
        #     None, "Select Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            # Обработка изображения
            image = Image.open(file_path).convert('RGBA')
            data = image.getdata()
            new_data = []
            for item in data:
                if 100 <= item[0] <= 255 and 100 <= item[1] <= 255 and 100 <= item[2] <= 255:
                    new_data.append((item[0], item[1], item[2], 255 - item[0]))
                else:
                    new_data.append(item)
            image.putdata(new_data)

            # Преобразуем обработанное изображение в формат QImage
            qimage = QImage(image.tobytes(), image.size[0], image.size[1], QImage.Format.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimage)

            # Создаём объект MovingObjectPhoto с обработанным изображением
            new_image = MovingObjectPhoto(pixmap, self.next_id)
            self.images[self.next_id] = new_image
            self.scene.addItem(new_image)
            new_image.setPos(-pixmap.width()//2,-pixmap.height()//2)
            # new_image.setPos(50 * (self.next_id % 10), 50 * (self.next_id // 10))
            self.next_id += 1

    def remove_image(self):
        selected_items = self.scene.selectedItems()
        for item in selected_items:
            if isinstance(item, MovingObjectPhoto):
                image_id = item.id
                self.scene.removeItem(item)
                del self.images[image_id]

    def increase_scale(self):
        self.scale_image(1.05)  # Увеличение масштаба на 5%

    def decrease_scale(self):
        self.scale_image(0.95)  # Уменьшение масштаба на 5%

    def scale_image(self, scale_factor):
        selected_items = self.scene.selectedItems()
        for item in selected_items:
            if isinstance(item, MovingObjectPhoto):
                transform = item.transform()
                transform.scale(scale_factor, scale_factor)
                item.setTransform(transform)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


#
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Application")
        self.resize(1280, 720)

        scene = QGraphicsScene()

        self.graphic_view = GraphicView(self)
        # self.graphic_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.graphic_view.setGeometry(QRect(40, 10, 471, 651))
        # self.setCentralWidget(self.graphic_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
