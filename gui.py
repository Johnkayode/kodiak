import json
from PyQt6.QtWidgets import *

from components import Label, FileFormatComboBox, FileDialog, JSONDisplayBox, HeaderCheckBox
from converter import Converter

class Application(QApplication):
    def __init__(self):
        super().__init__([])
        self.window = QWidget()
        self.window.setFixedSize(800, 600)
        self.window.setWindowTitle('Kodiak')


        self.default_file_format = "Excel"
        self.file_extensions = {
            "Excel": "Excel File (*.xlsx *.xls)",
            "Csv": "CSV File (*.csv)"
        }
        self.selected_file_format = self.default_file_format
        self.converter = Converter()
        self.json_data = ""
        self.header = True

        self.select_btn = QPushButton('Select File')
        self.select_btn.clicked.connect(self.select_file)

        self.file_format_combo_box = FileFormatComboBox(default_file_format=self.default_file_format)
        self.file_format_combo_box.file_format_changed.connect(self.on_file_format_changed)

        self.header_check_box = HeaderCheckBox()
        self.header_check_box.header_btn_checked.connect(self.on_header_checked)
        
        self.text_box = JSONDisplayBox()

        self.download_btn = QPushButton('Download JSON')
        self.download_btn.setStyleSheet("background-color : #0d6efd; padding: 5;")
        self.download_btn.clicked.connect(self.save_file)

        layout = QGridLayout()
        # layout.addWidget(Label('File Format:'))
        # layout.addWidget(self.file_format_combo_box)
        # layout.addWidget(Label('Header (Set if first row is header)'))
        # layout.addWidget(self.header_check_box)
        # layout.addWidget(self.select_btn)
        # layout.addWidget(self.text_box)
        # layout.addWidget(self.download_btn)
        grid = (
            ((0, 5, Label('File Format:')), (5, 7, self.file_format_combo_box)),
            ((0, 5, Label('Header (Set if first row is header)')), (5, 7, self.header_check_box)),
            ((0, 12, self.select_btn),),
            ((0, 12, self.text_box),),
            ((0, 12, self.download_btn),),
        )
        for (row_index, row) in enumerate(grid):
            for (_, cell) in enumerate(row):
                (col_offset, col_width, widget) = cell
                layout.addWidget(widget, row_index, col_offset, 1, col_width)

        self.window.setLayout(layout)

       

        self.window.show()

    def select_file(self):
        file_path, _ = FileDialog(file_filter = self.file_extensions[self.selected_file_format]).get_file()
        if file_path:
            if self.selected_file_format == "Excel":
                json_data = self.converter.convert_excel_to_json(file_path)
            elif self.selected_file_format == "Csv":
                json_data = self.converter.convert_csv_to_json(file_path, header=self.header)
            self.json_data = json_data
            self.text_box.setText(json_data)

    def save_file(self):
        file_path, _ = FileDialog(file_filter = "JSON File (*.json)").get_download_path()
        if file_path:
            self.converter.save_json_to_path(self.json_data, file_path)

    def on_file_format_changed(self, file_format: str):
        self.selected_file_format = file_format

    def on_header_checked(self, checked: bool):
        self.header = checked
        


