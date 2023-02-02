#Per Tests:
do_test = True
write_in_file = True
check_disorg = False
check_dup = False
if (do_test):
    time_series_file = CSVTimeSeriesFile(name='data.csv')
    time_series = time_series_file.get_data()
    output = compute_daily_max_difference(time_series)
    print('\n{}\n'.format(output))
    if write_in_file:
        with open("result.txt", "w") as f:
            for line in output:
                f.write(f"{line}\n")
if check_disorg:
    time_series_file_disorg = CSVTimeSeriesFile(
        name='data_ruined_2_disorg.csv')
    time_series = time_series_file_disorg.get_data()
if check_dup:
    time_series_file_dup = CSVTimeSeriesFile(name='data_ruined_2_dup.csv')
    time_series = time_series_file_dup.get_data()

import datetime


def test_timestamp(lista):
    lista_ridot = lista[:50]
    lista_epoch = [riga[0] for riga in lista_ridot]
    lista_time_pre = [
        datetime.datetime.fromtimestamp(epoch) for epoch in lista_epoch
    ]

    print(lista_time_pre)
    print('\n\nDOPO:')
    lista_epoch = [(epoch - (epoch % 86400)) for epoch in lista_epoch]
    lista_time_post = [
        datetime.datetime.fromtimestamp(epoch) for epoch in lista_epoch
    ]
    print(lista_time_post)
    return None
