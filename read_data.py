import csv
##csvを読み込むクラス
class Read_Data:

    def __init__(self, file_name):

        self.file_name = file_name

    def read_data(self):

        read_csv_data = []
        with open(self.file_name, "r") as f:

            reader = csv.reader(f)

            for row in reader:

                read_csv_data.append(row)

        return read_csv_data
