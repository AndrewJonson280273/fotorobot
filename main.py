import sys
import sqlite3
import shutil
from os import curdir, path

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *

from utils import Database
from fotorobot_ui import Ui_MainWindow
import settings

from a import GraphicView

fotorobot_db = Database(settings.db_path)


class ClickedLabel(QLabel):
    clicked = QtCore.pyqtSignal()

    def mouseDoubleClickEvent(self, e):
        super().mouseDoubleClickEvent(e)

        self.clicked.emit()


class Fotorobot(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('fotorobot.ui', self)  # Загружаем дизайн
        self.setupUi(self)  # загружаем дизайн

        # заносим все действия в список, чтобы удобно было подлючать функции циклом(?)
        self.db_add_actions = [self.add_nose, self.add_mouth, self.add_eyes, self.add_hair, self.add_glasses,
                               self.add_chin, self.add_wrinkles,
                               self.add_eyebrows, self.add_moustache, self.add_hat, self.add_clothes, self.add_ears]
        for a in self.db_add_actions:
            a.triggered.connect(self.db_add_element)  # если трегерим - вызываем метод добавления в бд

        self.refresh_list.clicked.connect(self.update_list)  # если нажимаем - вызываем метод обновления списк
        self.tabs.currentChanged.connect(self.update_list)

        self.pages = []
        self.a = []

        self.ui_widgets = None
        for i in self.el_list_widgets:
            if i["tab_index"] == self.tabs.currentIndex():
                self.ui_widgets = i
                break

        for i in self.ui_widgets["apply_buttons"]:
            i.clicked.connect(self.update_list)
        for i in self.ui_widgets["reset_buttons"]:
            i.clicked.connect(self.clear_filters)

        self.graphic_view = GraphicView(self)
        # self.graphic_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.graphic_view.setGeometry(QtCore.QRect(25, 40, 500, 700))
        self.check_graphics()
        self.graphic_view.scene.selectionChanged.connect(self.check_graphics)

        # self.list_grid = QGridLayout(self)
        # self.list_frame.setLayout(self.list_grid)



        self.delete_button.clicked.connect(self.graphic_view.remove_image)
        self.increase_button.clicked.connect(self.graphic_view.increase_scale)
        self.decrease_button.clicked.connect(self.graphic_view.decrease_scale)

        for el in self.el_list_widgets:
            back_button, page_label, next_button = el["page_widgets"]
            back_button.clicked.connect(self.change_page)
            next_button.clicked.connect(self.change_page)

        self.update_list()  # обновляем получается

    def check_graphics(self):
        graphics = self.graphic_view
        if graphics.scene.selectedItems():
            self.image_b_widget.setHidden(False)
        else:
            self.image_b_widget.setHidden(True)

    def db_add_element(self):
        # создаём новую форму для добавления элементов
        self.form_add_element = DatabaseForm(self)
        self.form_add_element.show()

    # обновление списка
    def update_list(self):
        for i in self.el_list_widgets:
            if i["tab_index"] == self.tabs.currentIndex():
                self.ui_widgets = i
                break
        ui_widgets = self.ui_widgets
        self.stacked_widget = ui_widgets["stacked_widget"]
        try:

            # определяем в какой вкладке находимся
            tab = ui_widgets["tab_text"]
            table = ""
            for key, v in settings.b.items():
                if v["translate"] == tab:
                    table = v["base_table"]

            # считываем выбранные фильтры
            filters = [(combo.currentText(), combo.property("property")["table"]) for combo in
                       ui_widgets["filter_combos"] if combo.currentText() != "Любой"]
            # print(filters) # [('Женский', 'gender'), ('Миндалевидный', 'eye_fissure_contour')]
            filters_sql = ''
            if filters:
                filters = [f[1] + " = " + f"(SELECT id FROM {f[1]} WHERE name = '" + f[0].lower() + "')" for f in
                           filters]
                filters_sql = f" WHERE {' AND '''.join(filters)}"
                print(filters_sql)
            # получение элементов из бд
            raw = fotorobot_db.execute(f"SELECT * FROM {table}{filters_sql}")
            elements = [r for r in raw if path.exists(r[-1])]

            for i in self.a:
                self.stacked_widget.removeWidget(i)

            # создаём многостраничность (pagination)

            if not elements:
                self.page_label.setText("Нет результатов")
                self.back_button.setHidden(True)
                self.next_button.setHidden(True)
                return

            self.back_button, self.page_label, self.next_button = ui_widgets["page_widgets"]

            # создаём список страниц
            count = 0
            page = []
            pages = []
            for i in elements:
                count += 1
                if count <= 8:
                    page.append(i)
                else:
                    pages.append(page)
                    page = []
                    page.append(i)
                    count = 1
            if page:
                pages.append(page)
            self.pages = pages

            # добавляем страницы
            for page in pages:
                # создаём рамку
                list_frame = QFrame(parent=ui_widgets["tab"])
                list_frame.setFrameShape(QFrame.Shape.StyledPanel)
                list_frame.setFrameShadow(QFrame.Shadow.Raised)
                # создаём сетку с рамке
                list_grid = QGridLayout(list_frame)
                list_frame.setLayout(list_grid)

                # добавляем картинки в сетку
                w, h = 2, 4  # размер сетки
                positions = [(i, j) for i in range(h) for j in range(w)]  # список позиций
                for position, el in zip(positions, page):  # рассортировка по полочкам всего
                    element = ClickedLabel(self)  # надпись
                    image = el[-1]
                    element.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)  # показываем пальчиk
                    wid = draw_image1(200, 150, image, element)[0]  # функция творит шедевры
                    wid.clicked.connect(self.image_click)
                    wid.setProperty("element", el)
                    # аккуратненько складываем
                    list_grid.addWidget(wid, *position, QtCore.Qt.AlignmentFlag.AlignCenter)
                self.a.append(list_frame)
                self.stacked_widget.addWidget(list_frame)
            self.stacked_widget.setCurrentIndex(0)
            current_index = self.stacked_widget.currentIndex()
            self.back_button.setHidden(not current_index > 0)
            self.next_button.setHidden(not current_index < len(self.pages) - 1)
            self.page_label.setText(f"Страница {current_index + 1}/{len(self.pages)}")

        except Exception as err:
            self.show_error(err)  # ой ошибочка вышла...

    def change_page(self):
        print(1)
        button = self.sender()
        current_index = self.stacked_widget.currentIndex()
        if button == self.back_button:
            self.stacked_widget.setCurrentIndex(current_index - 1)
        elif button == self.next_button:
            self.stacked_widget.setCurrentIndex(current_index + 1)
        current_index = self.stacked_widget.currentIndex()
        self.back_button.setHidden(not current_index > 0)
        self.next_button.setHidden(not current_index < len(self.pages) - 1)
        self.page_label.setText(f"Страница {current_index + 1}/{len(self.pages)}")

    def image_click(self):
        print(self.sender())
        self.graphic_view.add_image(self.sender().property("element")[-1])

    def clear_filters(self):
        for i in self.ui_widgets["filter_combos"]:
            i.setCurrentText("Любой")
        self.update_list()

    # ошибка
    def show_error(self, err, close=False):
        msg = QMessageBox(self)  # бокс
        msg.setText("Произошла ошибка: " + str(err))  # оправдываемся
        msg.setWindowTitle("База данных")  # с кем дело имеем?
        msg.setIcon(QMessageBox.Icon.Critical)  # иконочка
        msg.exec()  # работаем
        if close:
            self.close()  # хотим - закрываем, хотим - нет

    # успех
    def show_success(self, close=False):
        ex.update_list()  # обновим уж раз такое дело
        msg = QMessageBox(self)
        msg.setText("Элемент успешно добавлен!")  # радуемся
        msg.setWindowTitle("База данных")  # я с кем разговариваю?
        msg.setIcon(QMessageBox.Icon.Information)  # информируем
        msg.exec()  # работаем
        if close:
            self.close()  # хотим - закрываем, хотим - нет


class DatabaseForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        # uic.loadUi('fotorobot_add_element.ui', self)  # Загружаем дизайн
        self.fname = ""
        self.initUi()
        self.cancel_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self.save_to_db)

        # self.select_properties_layout.addWidget()

    def initUi(self):
        tab = self.sender().text()
        property_list = []
        for key, v in settings.b.items():
            if v["translate"] == tab:
                property_list = v["properties"]
                self.table = v["base_table"]

        self.properties = []

        self.image_preview = QLabel(self)
        self.image_preview.move(370, 30)
        self.image_preview.resize(312, 256)
        lens = len(property_list) * 30 + 80
        if lens < 345:
            self.resize(712, 345)
        else:
            self.resize(712, lens)
        self.layoutWidget = QWidget(self)
        self.layoutWidget.setGeometry(30, 30, 303, lens)
        self.layoutWidget.setObjectName("layoutWidget")
        self.select_properties_layout = QFormLayout(self.layoutWidget)
        self.select_properties_layout.setContentsMargins(0, 0, 0, 0)
        self.select_properties_layout.setSpacing(5)
        self.select_properties_layout.setObjectName("select_properties_layout")
        for property in property_list:
            property_title = QLabel(self.layoutWidget)
            property_title.setText(property["translate"].capitalize())

            property_combo = QComboBox(self.layoutWidget)
            property_combo.setEditable(False)
            property_combo.setFixedHeight(25)

            property_names = fotorobot_db.execute(f"SELECT name FROM {property['table']}")
            property_names = [i[0] for i in property_names]
            property_names.append("Не задано")

            for name in property_names:
                property_combo.addItem(name.capitalize())

            property_combo.setCurrentText("Не задано")

            self.select_properties_layout.addRow(property_title, property_combo)
            self.properties.append((property, property_combo))

        self.select_image_button = QPushButton(self.layoutWidget)
        self.select_image_button.setMinimumSize(QtCore.QSize(200, 0))
        self.select_image_button.setCheckable(False)
        self.select_image_button.clicked.connect(self.select_image)
        self.select_properties_layout.addRow(self.select_image_button)
        self.layoutWidget1 = QWidget(self)
        self.layoutWidget1.setGeometry(QtCore.QRect(370, 300, 315, 30))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.buttons_add_layout = QHBoxLayout(self.layoutWidget1)
        self.buttons_add_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_add_layout.setSpacing(20)
        self.buttons_add_layout.setObjectName("buttons_add_layout")
        self.save_button = QPushButton(self.layoutWidget1)
        self.save_button.setMinimumSize(QtCore.QSize(200, 0))
        self.save_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.save_button.setObjectName("save_button")
        self.buttons_add_layout.addWidget(self.save_button)
        self.cancel_button = QPushButton(self.layoutWidget1)
        self.cancel_button.setMinimumSize(QtCore.QSize(0, 0))
        self.cancel_button.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cancel_button.setObjectName("cancel_button")
        self.buttons_add_layout.addWidget(self.cancel_button)
        self.header_label = QLabel(self)
        self.header_label.setGeometry(30, 10, 301, 16)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.header_label.setFont(font)
        self.header_label.setObjectName("header_label")
        self.header_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.select_image_button.setText("Выбрать изображение")
        self.select_image_button.setMinimumHeight(30)
        self.save_button.setText("Сохранить в Базу данных")
        self.cancel_button.setText("Отмена")
        self.header_label.setText(self.sender().text())
        self.setWindowTitle("Добавление в Базу данных")

    def save_resources(self) -> str:
        filepath = self.fname
        filename = filepath.split("/")[-1]
        currentd = path.abspath(curdir).replace("\\", "/")
        resourcesd = currentd + settings.element_images_path
        new_filepath = resourcesd + filename

        if path.exists(resourcesd + filename):
            new_filename = filename[:]
            i = 1
            while path.exists(resourcesd + new_filename):
                name, ext = filename.split('.')
                symb = i
                name += str(symb)
                new_filename = name + "." + ext
                i += 1
            new_filepath = resourcesd + new_filename

        return shutil.copy2(filepath, new_filepath)

        # current_dir = path.abspath(curdir)
        # current_dir += settings.element_images_path
        #
        # ext = self.fname.split(".")[-1]
        # file_name = self.fname.split("/")[-1].split(".")[-2]
        # dir = current_dir + "\\" + file_name + "." + ext
        # print(dir)
        # if path.exists(dir):
        #     i = 0
        #     while not path.exists(dir):
        #         if i <= 9:
        #             ext = dir.split("\\")[-1].split(".")[-1]
        #             file_name = dir.split("\\")[-1].split(".")[-2] + i
        #             dir = current_dir + "\\" + file_name + "." + ext
        #             print(dir)
        #         else:
        #             self.show_error("Имя выбранного файла уже используется")
        #         i += 1
        # dest = shutil.copy2(self.fname, f"{dir}")

    def save_to_db(self):
        try:
            dest = self.save_resources()
            count = 0
            params = {}
            for property in self.properties:
                property, obj = property
                if obj.currentText() == "Не задано":
                    count += 1
                    continue
                params[property["table"]] = obj.currentText().lower()

            params["image"] = "\\".join(dest.split("/")[dest.split("/").index("resources"):])
            # хотите продолжить??
            if count > 1:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("База данных")
                dlg.setText(f"Вы не задали {count} параметров! Вы действительно хотите сохранить этот элемент?")
                dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                dlg.setIcon(QMessageBox.Icon.Warning)
                button = dlg.exec()

                if button == QMessageBox.StandardButton.No:
                    pass
                else:
                    try:
                        fotorobot_db.add_element(params, self.table)
                        self.show_success()
                        self.image_preview.clear()
                    except Exception as error:
                        self.show_error(error)
            else:
                try:
                    fotorobot_db.add_element(params, self.table)
                    self.show_success()
                    self.image_preview.clear()
                except Exception as error:
                    self.show_error(error)
        except Exception as error:
            self.show_error(error)

    def select_image(self):
        self.fname = QFileDialog.getOpenFileName(
            self, 'Выбрать изображение', '',
            'Все файлы (*);;Фото (*.png);;Фото (*.jpg)')[0]  # получение пути к файлу
        # pm = QPixmap(self.fname)
        # pm = pm.scaled(312, 256, aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        # if pm.width() < self.image_preview.width():  # проверка поместиться ли?
        #     self.image_preview.move(self.image_preview.x() + (self.image_preview.width() - pm.width()) // 2,
        #                             self.image_preview.y())
        # else:
        #     self.image_preview.move(370, 30)
        # self.image_preview.setPixmap(pm)
        draw_image(370, 30, 312, 256, self.fname, self.image_preview)

    def show_error(self, err, close=False):
        msg = QMessageBox(self)
        msg.setText("Произошла ошибка: " + str(err))
        msg.setWindowTitle("База данных")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.exec()
        if close:
            self.close()

    def show_success(self, close=False):
        ex.update_list()
        msg = QMessageBox(self)
        msg.setText("Элемент успешно добавлен!")
        msg.setWindowTitle("База данных")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
        if close:
            self.close()


def draw_image1(w: int, h: int, path_to_image: str, object: QLabel):
    # object = QLabel(self)
    object.resize(w, h)
    pm = QPixmap(path_to_image)
    pm = pm.scaled(w, h, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
    object.setPixmap(pm)
    return object, pm


def draw_image(x: int, y: int, w: int, h: int, path_to_image: str, object: QLabel):
    # image = QLabel(self)
    object.move(x, y)
    object.resize(w, h)
    pm = QPixmap(path_to_image)
    pm = pm.scaled(w, h, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
    if pm.width() < object.width():  # проверка поместиться ли?
        object.move(x + (object.width() - pm.width()) // 2, y)
    else:
        object.move(x, y)
    object.setPixmap(pm)
    return object, pm


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Fotorobot()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
