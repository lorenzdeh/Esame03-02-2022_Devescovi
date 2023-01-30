class ExamException(Exception):
    pass


class CSVFile():

    def __init__(self, name):
        self.name = name

    def get_data(self):
        try:
            #'with' apre il file assegnandolo alla variabile file e lo chiude all'uscita dal blocco
            with open(self.name, 'r') as file:
                self.lines_ls = [row.split(',') for row in file.readlines()]
                self.lines_clean = []
                for line in self.lines_ls:
                    if len(line) >= 2:
                        line[1] = line[1].strip('\n')
                        self.lines_clean.append(line)
                if len(self.lines_clean[1:]) == 0:
                    return None
                return self.lines_clean[1:]
        except FileNotFoundError as e:
            self.file_check = False
            raise ExamException('Errore: {}'.format(e))


class CSVTimeSeriesFile(CSVFile):

    def __init__(self, name):
        super().__init__(name)

    def get_data(self):
        data = super().get_data()
        if data is not None:
            if self.controllo_no_duplicati(data):
                if self.controllo_ordine(data):
                    out_data = []
                    for line in data:
                        if self.is_num(line[0]) and self.is_num(line[1]):
                            line[0] = int(line[0])
                            line[1] = float(line[1])
                            out_data.append(line)
                        else:
                            print(
                                'Errore: non è stato possibile convertire: {}'.
                                format(line))
                    return out_data
                else:
                    raise ExamException('Errore: la lista è disordinata')
            else:
                raise ExamException(
                    'Errore: la lista contiene epoch dei duplicati')
        else:
            raise ExamException('Errore: file vuoto')

    #controlla che non ci siano epoch duplicati
    def controllo_no_duplicati(self, lista):
        lista_epoch = [riga[0] for riga in lista]
        return len(lista_epoch) == len(set(lista_epoch))

    #controlla che gli epoch siano in ordine
    def controllo_ordine(self, lista):
        lista_epoch = [riga[0] for riga in lista]
        return lista_epoch == sorted(lista_epoch)

    def is_num(self, ele):
        try:
            float(ele)
            return True
        except:
            return False


def compute_daily_max_difference(time_series):
    if time_series is not None:
        daily_diff = []
        temp_min = time_series[0][1]
        temp_max = time_series[0][1]
        time_series = [[(epoch[0] - (epoch[0] % 86400)), epoch[1]]
                       for epoch in time_series]
        current_day = time_series[0][0]
        counter = 0
        for line in time_series:
            if line[0] == current_day:
                counter += 1
                if (line[1] < temp_min):
                    temp_min = line[1]
                elif (line[1] > temp_max):
                    temp_max = line[1]
            else:
                if counter <= 1:
                    daily_diff.append(None)
                else:
                    daily_diff.append(round((temp_max - temp_min), 2))
                current_day = line[0]
                temp_max = line[1]
                temp_min = line[1]
                counter = 0
        if counter <= 1:
            daily_diff.append(None)
        else:
            daily_diff.append(round((temp_max - temp_min), 2))
        return daily_diff
    else:
        raise ExamException('Errore: la lista fornita è vuota')


#Per Tests:
time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()

output = compute_daily_max_difference(time_series)
print('\n{}\n'.format(output))

with open("result.txt", "w") as f:
    for line in output:
        f.write(f"{line}\n")

check_dis = False
check_dup = False

if (check_dis):
    time_series_file_disorg = CSVTimeSeriesFile(
        name='data_ruided_2_disorg.csv')
    time_series = time_series_file_disorg.get_data()
if (check_dup):
    time_series_file_dup = CSVTimeSeriesFile(name='data_ruided_2_dup.csv')
    time_series = time_series_file_dup.get_data()
