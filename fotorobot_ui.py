# Form implementation generated from reading ui file 'fotorobot.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import settings
from utils import Database

fotorobot_db = Database(settings.db_path)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1045, 914)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabs = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabs.setGeometry(QtCore.QRect(550, 0, 491, 831))
        self.tabs.setObjectName("tabs")
        categories = [i for i in settings.b.keys()]

        self.el_list_widgets = []

        f_apply_buttons = []
        f_reset_buttons = []

        for category in categories:
            f_list_combos = []

            tab = QtWidgets.QWidget()
            tab.setObjectName(f"{category}_tab")
            self.tabs.addTab(tab, "")
            layoutWidget = QtWidgets.QWidget(parent=tab)
            layoutWidget.setGeometry(QtCore.QRect(0, 10, 481, 211))
            tab_v_layout = QtWidgets.QVBoxLayout(layoutWidget)
            tab_v_layout.setContentsMargins(0, 0, 0, 0)
            filters_group_box = QtWidgets.QGroupBox(parent=layoutWidget)
            filters_group_box.setMinimumSize(QtCore.QSize(0, 0))
            filters_group_box.setTitle("Фильтры")
            layoutWidget1 = QtWidgets.QWidget(parent=filters_group_box)
            layoutWidget1.setGeometry(QtCore.QRect(5, 20, 471, 181))

            filters_v_layout = QtWidgets.QVBoxLayout(layoutWidget1)
            filters_v_layout.setContentsMargins(0, 0, 0, 0)
            filters_v_layout.setSpacing(5)

            self.tabs.setTabText(self.tabs.indexOf(tab), settings.b[category]["translate"])
            for property in settings.b[category]["properties"]:
                filter_h_layout = QtWidgets.QHBoxLayout()
                filter_h_layout.setSpacing(20)
                property_label = QtWidgets.QLabel(parent=layoutWidget1)
                property_label.setText(property["translate"].capitalize())
                filter_h_layout.addWidget(property_label)

                property_names = fotorobot_db.execute(f"SELECT name FROM {property['table']}")
                property_names = [i[0].capitalize() for i in property_names]
                property_names.append("Любой")

                property_combo = QtWidgets.QComboBox(parent=layoutWidget1)
                property_combo.setEditable(False)
                for i in property_names:
                    property_combo.addItem(i)
                property_combo.setCurrentText("Любой")
                property_combo.setProperty("property", property)

                f_list_combos.append(property_combo)

                filter_h_layout.addWidget(property_combo)
                filters_v_layout.addLayout(filter_h_layout)

            f_buttons_layout = QtWidgets.QHBoxLayout()
            f_apply_button = QtWidgets.QPushButton(parent=layoutWidget1)
            f_buttons_layout.addWidget(f_apply_button)
            f_reset_button = QtWidgets.QPushButton(parent=layoutWidget1)
            f_buttons_layout.addWidget(f_reset_button)
            f_apply_button.setText("Применить")
            f_reset_button.setText("Сбросить")

            f_reset_buttons.append(f_reset_button)
            f_apply_buttons.append(f_apply_button)

            st_widget = QtWidgets.QStackedWidget(tab)
            st_widget.setGeometry(QtCore.QRect(0, 220, 480, 550))

            back_button = QtWidgets.QPushButton(parent=tab)
            back_button.setText("<< Назад")
            back_button.setGeometry(QtCore.QRect(0, 770, 93, 28))

            next_button = QtWidgets.QPushButton(parent=tab)
            next_button.setText("Вперёд >>")
            next_button.setGeometry(QtCore.QRect(390, 770, 93, 28))

            page_number_label = QtWidgets.QLabel(parent=tab)
            page_number_label.setGeometry(QtCore.QRect(90, 776, 301, 20))
            page_number_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            filters_v_layout.addLayout(f_buttons_layout)
            tab_v_layout.addWidget(filters_group_box)
            self.el_list_widgets.append({"tab_text": settings.b[category]["translate"],
                                         "tab": tab,
                                         "tab_index": self.tabs.indexOf(tab),
                                         "filter_combos": f_list_combos,
                                         "apply_buttons": f_apply_buttons,
                                         "reset_buttons": f_reset_buttons,
                                         "stacked_widget": st_widget,
                                         "page_widgets": (back_button, page_number_label, next_button)})

        self.refresh_list = QtWidgets.QPushButton(parent=self.centralwidget)
        self.refresh_list.setGeometry(QtCore.QRect(950, 830, 93, 28))
        self.refresh_list.setObjectName("refresh_list")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1045, 26))
        self.menubar.setObjectName("menubar")
        self.datebase = QtWidgets.QMenu(parent=self.menubar)
        self.datebase.setObjectName("datebase")
        self.add_element = QtWidgets.QMenu(parent=self.datebase)
        self.add_element.setObjectName("add_element")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.add_mouth = QtGui.QAction(parent=MainWindow)
        self.add_mouth.setObjectName("add_mouth")
        self.add_nose = QtGui.QAction(parent=MainWindow)
        self.add_nose.setObjectName("add_nose")
        self.add_hair = QtGui.QAction(parent=MainWindow)
        self.add_hair.setObjectName("add_hair")
        self.add_eyes = QtGui.QAction(parent=MainWindow)
        self.add_eyes.setCheckable(False)
        self.add_eyes.setObjectName("add_eyes")
        self.add_eyebrows = QtGui.QAction(parent=MainWindow)
        self.add_eyebrows.setObjectName("add_eyebrows")
        self.add_chin = QtGui.QAction(parent=MainWindow)
        self.add_chin.setObjectName("add_chin")
        # self.add_moustache = QtGui.QAction(parent=MainWindow)
        # self.add_moustache.setObjectName("add_moustache")
        # self.add_hat = QtGui.QAction(parent=MainWindow)
        # self.add_hat.setObjectName("add_hat")
        # self.add_clothes = QtGui.QAction(parent=MainWindow)
        # self.add_clothes.setObjectName("add_clothes")
        self.add_ears = QtGui.QAction(parent=MainWindow)
        self.add_ears.setObjectName("add_ears")
        # self.add_wrinkles = QtGui.QAction(parent=MainWindow)
        # self.add_wrinkles.setObjectName("add_wrinkles")
        # self.add_glasses = QtGui.QAction(parent=MainWindow)
        # self.add_glasses.setObjectName("add_glasses")
        # self.delete_element = QtGui.QAction(parent=MainWindow)
        # self.delete_element.setObjectName("delete_element")
        # self.edit_element = QtGui.QAction(parent=MainWindow)
        # self.edit_element.setObjectName("edit_element")
        self.add_element.addAction(self.add_eyes)
        self.add_element.addAction(self.add_mouth)
        self.add_element.addAction(self.add_nose)
        self.add_element.addAction(self.add_hair)
        self.add_element.addAction(self.add_eyebrows)
        self.add_element.addAction(self.add_chin)
        # self.add_element.addAction(self.add_moustache)
        # self.add_element.addAction(self.add_hat)
        # self.add_element.addAction(self.add_clothes)
        self.add_element.addAction(self.add_ears)
        # self.add_element.addAction(self.add_wrinkles)
        # self.add_element.addAction(self.add_glasses)
        self.datebase.addAction(self.add_element.menuAction())
        # self.datebase.addAction(self.delete_element)
        # self.datebase.addAction(self.edit_element)
        self.menubar.addAction(self.datebase.menuAction())

        self.image_b_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.image_b_widget.setGeometry(QtCore.QRect(330, 710, 197, 90))
        self.img_layout = QtWidgets.QVBoxLayout(self.image_b_widget)
        self.img_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QtWidgets.QLabel(parent=self.image_b_widget)
        self.label.setText("Выбранное изображение")
        self.img_layout.addWidget(self.label)
        self.h_layout_image_buttons = QtWidgets.QHBoxLayout()

        self.increase_button = QtWidgets.QPushButton(parent=self.image_b_widget)
        self.increase_button.setText("Увеличить")
        self.h_layout_image_buttons.addWidget(self.increase_button)
        self.decrease_button = QtWidgets.QPushButton(parent=self.image_b_widget)
        self.decrease_button.setText("Уменьшить")
        self.h_layout_image_buttons.addWidget(self.decrease_button)
        self.img_layout.addLayout(self.h_layout_image_buttons)
        self.delete_button = QtWidgets.QPushButton(parent=self.image_b_widget)
        self.delete_button.setText("Удалить")
        self.img_layout.addWidget(self.delete_button)

        # с новым годом!
        # self.deco = QtWidgets.QLabel(parent=self.centralwidget)
        # self.deco.setGeometry(QtCore.QRect(26, 705, 501, 81))
        # self.deco.setText("")
        # self.deco.setPixmap(QtGui.QPixmap("resources/deco1.png"))
        # self.deco.setScaledContents(True)
        # self.deco.setObjectName("deco")

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Фоторобот"))
        self.refresh_list.setText(_translate("MainWindow", "Обновить"))
        self.datebase.setTitle(_translate("MainWindow", "База данных"))
        self.add_element.setTitle(_translate("MainWindow", "Добавить элемент"))
        self.add_mouth.setText(_translate("MainWindow", "Рот"))
        self.add_nose.setText(_translate("MainWindow", "Нос"))
        self.add_hair.setText(_translate("MainWindow", "Волосы"))
        self.add_eyes.setText(_translate("MainWindow", "Глаза"))
        self.add_eyebrows.setText(_translate("MainWindow", "Брови"))
        self.add_chin.setText(_translate("MainWindow", "Подбородок"))
        # self.add_moustache.setText(_translate("MainWindow", "Усы"))
        # self.add_hat.setText(_translate("MainWindow", "Головной убор"))
        # self.add_clothes.setText(_translate("MainWindow", "Одежда"))
        self.add_ears.setText(_translate("MainWindow", "Уши"))
        # self.add_wrinkles.setText(_translate("MainWindow", "Морщины"))
        # self.add_glasses.setText(_translate("MainWindow", "Очки"))
        # self.delete_element.setText(_translate("MainWindow", "Удалить элемент"))
        # self.edit_element.setText(_translate("MainWindow", "Изменить элемент"))
