from pprint import pprint

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.Qt import QPixmap, QImage, Qt

from ui_window import Ui_MainWindow

import requests
import sys

STATIC_API_URL = 'http://static-maps.yandex.ru/1.x/'
GEOCODER_API_URL = "http://geocode-maps.yandex.ru/1.x/"
GEOCODER_API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"
SEARCH_URL = "https://search-maps.yandex.ru/v1/"
SEARCH_KEY = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"


def point_to_str(p):
    """convert point to http format"""
    return "%.8f" % p[0] + "," + "%.8f" % p[1]


class MainWindow(QWidget, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.static_api_params = {'l': 'map',
                                  'size': '450,450'}

        self._z = 4
        self._ll = 37.588392, 55.734036
        self.apply_cords()

        self.found_toponym = None  # Store toponym json if found

        # Connect layouts buttons
        self.rb_map.toggled.connect(self.change_layouts)
        self.rb_sat.toggled.connect(self.change_layouts)
        self.cb_trf.stateChanged.connect(self.change_layouts)
        self.cb_skl.stateChanged.connect(self.change_layouts)

        self.bt_search.clicked.connect(self.search_by_button)
        self.bt_clean.clicked.connect(self.clean_result)

        self.cb_pcd.stateChanged.connect(self.show_info)

    @property
    def ll(self):
        return self._ll

    @property
    def z(self):
        return self._z

    def apply_cords(self):
        """Translate (z, ll) to (spn, ll)  and update image"""
        x, y = self.ll
        e = 2
        scale_e = e / (2 ** self.z)
        delta = (360 - e) / (2 ** self.z)
        lower_corner = [x - delta / 2, y - delta / 2]
        upper_corner = [x + delta / 2, y + delta / 2]

        # Check borders and move map if get out
        if lower_corner[0] <= -180:
            xd = lower_corner[0] + 180 - scale_e
            x -= xd
        elif upper_corner[0] >= 180:
            xd = upper_corner[0] - 180 + scale_e
            x -= xd

        if lower_corner[1] < -90:
            yd = lower_corner[1] + 90 - scale_e
            y -= yd
        elif upper_corner[1] > 90:
            yd = upper_corner[1] - 90 + scale_e
            y -= yd

        self.static_api_params["ll"] = point_to_str((x, y))
        self.static_api_params["spn"] = point_to_str((delta, delta))
        self.update_image()

    @ll.setter
    def ll(self, ll):
        # Change center of map
        if not (-180 <= ll[0] <= 180 and -90 <= ll[1] <= 90):
            return
        self._ll = ll
        self.apply_cords()

    @z.setter
    def z(self, z):
        # Change scale of map
        if not (3 <= z <= 20):
            return
        self._z = z
        self.apply_cords()

    def update_image(self):
        print(f"z: {self.z}, ll: {self.ll}")
        pprint(self.static_api_params)

        # Get image from staticAPI
        response = requests.get(STATIC_API_URL, params=self.static_api_params)
        self.map_container.clear()
        if response is None:
            # Report an error
            self.map_container.setText("Connection Failed")
        else:
            # Set image
            img = QPixmap.fromImage(QImage.fromData(response.content))
            self.map_container.setPixmap(img)

    def move_map(self, dx, dy):
        x, y = self.ll
        move_delta = 360 / (2 ** self.z)
        x = (x + move_delta * 2 * dx) % 360
        if x > 180:
            x -= 360
        y = (y + move_delta * dy) % 180
        if y > 90:
            y -= 180
        self.ll = x, y

    def change_scale(self, d: int):
        # d - {1, -1}
        self.z += d

    def change_layouts(self):
        # Update layouts information from buttons
        layouts = ['map' if self.rb_map.isChecked() else 'sat']  # main layout
        if self.cb_trf.isChecked():  # Traffic jams
            layouts.append('trf')
        if self.cb_skl.isChecked():  # Toponyms name
            layouts.append('skl')

        self.static_api_params["l"] = ','.join(layouts)
        self.update_image()

    def search_by_button(self):
        self.clean_result()  # Delete  info about past toponym

        toponym_to_find = self.le_search.text()

        # Make search attributes
        search_params = {
            "apikey": SEARCH_KEY,
            "text": toponym_to_find,
            "lang": 'ru_RU'}
        # And get response
        search_response = requests.get(SEARCH_URL, params=search_params)

        if not search_response:
            return

        search_response_json = search_response.json()

        # Get list of toponyms for checking found toponym
        search_toponyms = search_response_json['features']

        if len(search_toponyms):  # Check if the search couldn't found
            toponym_coordinates = tuple(map(float, search_toponyms[0]["geometry"]["coordinates"]))

            self.found_toponym = search_toponyms[0]
            self.show_info()
        else:  # If the toponym weren't found
            return  # Exit

        # Make a point on the map
        self.static_api_params['pt'] = f'{",".join(map(str, toponym_coordinates))},org'
        self.ll = toponym_coordinates  # Update coords of founded toponym

    def show_info(self):
        self.pt_info.clear()

        if self.found_toponym is None:  # If no toponym
            return

        info_to_show = []
        toponym = self.found_toponym['properties']
        if 'GeocoderMetaData' in toponym.keys():  # Checking type of toponym: org. or geoobj.
            info_to_show.append(toponym['GeocoderMetaData']['text'])
        else:
            info_to_show.append(toponym['CompanyMetaData']['address'])

        if self.cb_pcd.isChecked():
            # Searching object's postal code
            geocoder_params = {
                "apikey": GEOCODER_API_KEY,
                "geocode": info_to_show[0],
                "format": "json"}
            response = requests.get(GEOCODER_API_URL, params=geocoder_params)
            json_response = response.json()
            try:
                postal_code = json_response["response"]["GeoObjectCollection"]["featureMember"][0] \
                    ["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
            except KeyError:  # If toponym has not postal code
                postal_code = 'Not found'

            info_to_show.append(f'Индекс: {postal_code}')

        for string in info_to_show:  # Append toponym's info to pt_info (PlainTextEdit)
            self.pt_info.appendPlainText(string)

    def clean_result(self):
        self.remove_point()
        self.clean_info()

    def remove_point(self):  # Delete all info about points on map
        if 'pt' in self.static_api_params:
            del self.static_api_params['pt']

    def clean_info(self):  # Clean showed in pt_info (PlainTextEdit) address
        self.found_toponym = None
        self.pt_info.clear()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_PageUp:
            self.change_scale(1)
        elif a0.key() == Qt.Key_PageDown:
            self.change_scale(-1)
        elif a0.key() == Qt.Key_Up:
            self.move_map(0, 1)
        elif a0.key() == Qt.Key_Down:
            self.move_map(0, -1)
        elif a0.key() == Qt.Key_Left:
            self.move_map(-1, 0)
        elif a0.key() == Qt.Key_Right:
            self.move_map(1, 0)
        elif a0.key() == Qt.Key_Enter:
            self.map_container.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
