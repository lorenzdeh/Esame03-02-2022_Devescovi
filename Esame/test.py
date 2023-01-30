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