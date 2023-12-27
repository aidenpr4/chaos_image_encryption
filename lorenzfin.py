import os
import matplotlib.image as mpimg
from scipy.integrate import odeint
from PIL import Image
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox
import time
import matplotlib.pyplot as plt

# Encryption function
def encrypt(img, key, itera):
    img = np.resize(img, (img.shape[0], img.shape[1] * img.shape[2]))

    def logistic(r, x):
        return r * x * (1 - x)

    n = 10000
    r = np.linspace(2.5, 4.0, n)
    iterations = 1000
    last = 100
    x = 1e-5 * np.ones(n)

    for i in range(iterations):
        x = logistic(r, x)

    key.append(key[0] * key[1])

    def lorenz(in_, t, sigma, b, r):
        x = in_[0]
        y = in_[1]
        z = in_[2]

        return [sigma * (y - x), r * x - y - x * z, x * y - b * z]

    def get_solution(in_0, tmax, nt, args_tuple):
        t = np.linspace(0, tmax, nt)
        soln = odeint(lorenz, in_0, t, args=args_tuple).T
        return t, soln

    in_0 = key
    t_max = 20
    t_steps = 50000000
    t, [solx, soly, solz] = get_solution(in_0, t_max, t_steps, (10.0, 8/3, 28))

    tm = np.zeros((img.shape[1], img.shape[1]))

    for i in range(img.shape[1]):
        for j in range(img.shape[1]):
            if (i % 3 == 0):
                tm[i][j] = int(abs(solx[itera] * 2344))
            elif (i % 3 == 1):
                tm[i][j] = int(abs(soly[itera] * 37265))
            elif (i % 3 == 2):
                tm[i][j] = int(abs(solz[itera] * 3589))
            itera += 3

            # else:
            # # Limit itera to the last index of solx
            #     itera = len(solx) - 1
            #     tm[i][j] = 0

    temp = int(key[0] * key[2] * 87435)
    temp = temp % 1000
    log_key = x[temp]
    print("temp = ", temp)
    tm = tm * log_key

    tm = tm % 256

    encrypt_img = np.matmul(img, tm)
    encrypt_img = np.transpose(encrypt_img)
    print(encrypt_img.shape)
    return encrypt_img

# Decryption function
def decrypt(e_img, key, itera):
    def logistic(r, x):
        return r * x * (1 - x)

    n = 10000
    r = np.linspace(2.5, 4.0, n)
    iterations = 1000
    last = 100
    x = 1e-5 * np.ones(n)

    for i in range(iterations):
        x = logistic(r, x)

    e_img = np.transpose(e_img)
    key.append(key[0] * key[1])

    def lorenz(in_, t, sigma, b, r):
        x = in_[0]
        y = in_[1]
        z = in_[2]

        return [sigma * (y - x), r * x - y - x * z, x * y - b * z]

    def get_solution(in_0, tmax, nt, args_tuple):
        t = np.linspace(0, tmax, nt)
        soln = odeint(lorenz, in_0, t, args=args_tuple).T
        return t, soln

    in_0 = key
    t_max = 20
    t_steps = 50000000
    t, [solx, soly, solz] = get_solution(in_0, t_max, t_steps, (10.0, 8/3, 28))

    tm = np.zeros((e_img.shape[1], e_img.shape[1]))

    for i in range(e_img.shape[1]):
        for j in range(e_img.shape[1]):
            if (i % 3 == 0):
                tm[i][j] = int(abs(solx[itera] * 2344))
            elif (i % 3 == 1):
                tm[i][j] = int(abs(soly[itera] * 37265))
            elif (i % 3 == 2):
                tm[i][j] = int(abs(solz[itera] * 3589))
            itera += 3

    temp = int(key[0] * key[2] * 87435)
    temp = temp % 1000
    log_key = x[temp]
    print("temp = ", temp)
    tm = tm * log_key
    tm = tm % 256

    tm_inv = np.linalg.pinv(tm)
    print(e_img.shape)
    print(tm_inv.shape)
    decrypt_img = np.matmul(e_img, tm_inv)

    decrypt_img = np.around(decrypt_img)
    decrypt_img = decrypt_img.astype(int)
    decrypt_img = np.resize(decrypt_img, (decrypt_img.shape[0], decrypt_img.shape[1] // 3, 3))
    return decrypt_img

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1204, 771)
        self.key1 = 0  # Initialize with default values
        self.key2 = 0
        self.key3 = 0
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(290, 20, 631, 111))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(60, 180, 381, 381))
        self.photo.setText("")
        self.photo.setPixmap(QtGui.QPixmap("noimg.png"))
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.key_1_label = QtWidgets.QLabel(self.centralwidget)
        self.key_1_label.setGeometry(QtCore.QRect(90, 590, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.key_1_label.setFont(font)
        self.key_1_label.setObjectName("key_1_label")
        self.key_2_label = QtWidgets.QLabel(self.centralwidget)
        self.key_2_label.setGeometry(QtCore.QRect(90, 630, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.key_2_label.setFont(font)
        self.key_2_label.setObjectName("key_2_label")
        self.key_3_label = QtWidgets.QLabel(self.centralwidget)
        self.key_3_label.setGeometry(QtCore.QRect(90, 670, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.key_3_label.setFont(font)
        self.key_3_label.setObjectName("key_3_label")
        self.encrypt_button = QtWidgets.QPushButton(self.centralwidget)
        self.encrypt_button.setGeometry(QtCore.QRect(550, 280, 101, 41))
        self.encrypt_button.setObjectName("encrypt_button")
        self.encrypt_button.setStyleSheet("background-color: green; color: white;")
        self.decrypt_button = QtWidgets.QPushButton(self.centralwidget)
        self.decrypt_button.setGeometry(QtCore.QRect(550, 360, 101, 41))
        self.decrypt_button.setObjectName("decrypt_button")
        self.decrypt_button.setStyleSheet("background-color: blue; color: white;")
        self.photo1 = QtWidgets.QLabel(self.centralwidget)
        self.photo1.setGeometry(QtCore.QRect(760, 180, 381, 381))
        self.photo1.setText("")
        self.photo1.setPixmap(QtGui.QPixmap("noimg.png"))
        self.photo1.setScaledContents(True)
        self.photo1.setObjectName("photo1")
        self.img_label = QtWidgets.QLabel(self.centralwidget)
        self.img_label.setGeometry(QtCore.QRect(430, 630, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.img_label.setFont(font)
        self.img_label.setObjectName("img_label")
        self.img_info_label = QtWidgets.QLabel(self.centralwidget)
        self.img_info_label.setGeometry(QtCore.QRect(500, 630, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.img_info_label.setFont(font)
        self.img_info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.img_info_label.setObjectName("img_info_label")
        self.img_info_label.setText("Select an image to be encrypted")
        self.select_button = QtWidgets.QPushButton(self.centralwidget)
        self.select_button.setGeometry(QtCore.QRect(810, 630, 111, 41))
        self.select_button.setObjectName("select_button")
        self.select_button.setStyleSheet("background-color: orange; color: white;")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1204, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.select_button.clicked.connect(self.set_image)
        self.encrypt_button.clicked.connect(self.encrypt_photo)
        self.decrypt_button.clicked.connect(self.decrypt_photo)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title_label.setText(_translate("MainWindow", "    ChaosCrypt "))
        self.encrypt_button.setText(_translate("MainWindow", "Encrypt"))
        self.decrypt_button.setText(_translate("MainWindow", "Decrypt"))
        self.img_label.setText(_translate("MainWindow", " "))
        self.select_button.setText(_translate("MainWindow", "Select"))

    def set_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(None, "Select Image", "", "Images (*.png *.jpg *.bmp);;All Files (*)", options=options)

        if file_name:
            global path
            self.path = file_name
            self.photo.setPixmap(QtGui.QPixmap(self.path))

    def encrypt_photo(self):
        if not  self.path:
            error_message = QMessageBox(self.centralwidget)
            error_message.setIcon(QMessageBox.Critical)
            error_message.setText("Please select an image first.")
            error_message.setWindowTitle("Error")
            error_message.addButton(QMessageBox.Ok)
            error_message.exec_()
            return

        try:
            key1, ok1 = QInputDialog.getDouble(self.centralwidget, "Enter Key 1", "Key 1:")
            key2, ok2 = QInputDialog.getDouble(self.centralwidget, "Enter Key 2", "Key 2:")
            key3, ok3 = QInputDialog.getInt(self.centralwidget, "Enter Key 3", "Key 3:")

            if ok1 and ok2 and ok3:
                self.key1 = key1
                self.key2 = key2
                self.key3 = key3
                img = Image.open(self.path)
                p = np.array(img)
                final = encrypt(p, [self.key1, self.key2], self.key3)

                encrypted_folder = "encrypted_images"
                if not os.path.exists(encrypted_folder):
                    os.makedirs(encrypted_folder)

                encrypted_file_name = os.path.join(encrypted_folder, "encrypted_{}.npy".format(int(time.time())))
                np.save(encrypted_file_name, final)

                encrypted_png_file = encrypted_file_name.replace(".npy", ".png")
                mpimg.imsave(encrypted_png_file, final)
                self.photo1.setPixmap(QtGui.QPixmap(encrypted_png_file))
        except Exception as e:
            QMessageBox.critical(self.centralwidget, "Error", str(e))

    def decrypt_photo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        encrypted_file_name, _ = QFileDialog.getOpenFileName(None, "Select Encrypted File", "", "Numpy Files (*.npy);;All Files (*)", options=options)

        if encrypted_file_name:
            encrypted_folder = "decrypted_images"
            if not os.path.exists(encrypted_folder):
                os.makedirs(encrypted_folder)

            encrypted_png_file = encrypted_file_name.replace(".npy", ".png")
            self.photo.setPixmap(QtGui.QPixmap(encrypted_png_file))

            try:
                key1, ok1 = QInputDialog.getDouble(self.centralwidget, "Enter Key 1", "Key 1:")
                key2, ok2 = QInputDialog.getDouble(self.centralwidget, "Enter Key 2", "Key 2:")
                key3, ok3 = QInputDialog.getInt(self.centralwidget, "Enter Key 3", "Key 3:")

                if ok1 and ok2 and ok3:
                    keys = [key1, key2]
                    key3 = int(key3)
                    p = np.load(encrypted_file_name, allow_pickle=True)
                    final = decrypt(p, keys, key3)
                    final = final.astype(np.uint8)  # Convert to uint8

                    decrypted_file_name = os.path.join(encrypted_folder, "decrypted_{}.jpg".format(int(time.time())))
                    Image.fromarray(final).save(decrypted_file_name)

                    self.photo1.setPixmap(QtGui.QPixmap(decrypted_file_name))

            except Exception as e:
                QMessageBox.critical(self.centralwidget, "Error", str(e))

# Application entry point
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

