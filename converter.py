import os
import csv
import json
import pyexcel

from pathlib import Path
from typing import Union, Any
from utils import JSONEncoder





class Converter:
    """ Convert receives a excel/csv file and returns it in json format and vice versa """

    def __init__(self):
        self.status = 0

    def convert_excel_to_json(self, file_path: Union[str, Path]) -> Union[str, Any]:
        """
        Converts Excel (xlsx, xls) data to json

        :param str, Path file_path: Absolute file path of the excel file
        """

        records = pyexcel.iget_records(file_name=file_path)
        data = []
        for record in records:
            print(dict(record))
            data.append(dict(record))
        return json.dumps(data, ensure_ascii=False, indent=4, cls=JSONEncoder)

    def convert_csv_to_json(self, file_path: Union[str, Path], header: bool = True) -> Union[str, Any]:
        """
        Converts CSV data to json

        :param str, Path file_path: Absolute file path of the csv file
        :param bool header: If the csv data contains an header row. Default value is True and uses the first row as header
        """

        data = []
        with open(file_path, encoding="utf-8", errors="ignore") as csvFile:
            csvReader = csv.reader(csvFile, delimiter=",")
            if header:
                header = next(csvReader)
            else:
                ncol = len(next(csvReader)) # Read first line and count columns
                csvFile.seek(0) # Go back to beginning of file
                header = [n+1 for n in range(ncol)]
        
            for row in csvReader:
                rowObject = {}
                for i, field in enumerate(row):
                    rowObject[header[i]] = field
                data.append(rowObject)

        return json.dumps(data, ensure_ascii=False, indent=4, cls=JSONEncoder)

    def convert_json_to_xlsx(self, json_path: Union[str, Path], output_path: Union[str, Path]):
        """
        Writes data from json file to excel file

        :param str, Path json_path: Input path for json file
        :param str, Path output_path: Output path for excel file
        """
        with open(json_path, encoding="utf-8", errors="ignore") as jsonFile:
            data = json.load(jsonFile)
            pyexcel.save_as(records=data, dest_file_name=output_path)

    def save_json_to_path(self, json_data: Union[str, Any], output_path: Union[str, Path]):
        """ 
        Writes json data to file

        :param str json_data: Json string
        :param str, Path output_path: Output path for json file
        """
        with open(output_path, 'w') as out_file:
           out_file.write(json_data)
        


json_data = Converter().convert_csv_to_json("/Users/nerdthejohn/Downloads/sample2.csv")
Converter().save_json_to_path(json_data, "/Users/nerdthejohn/Downloads/res.json")
Converter().convert_json_to_xlsx("/Users/nerdthejohn/Downloads/res.json", "/Users/nerdthejohn/Downloads/res.xlsx")