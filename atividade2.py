# Os funcionários de uma empresa chegam a uma taxa de até 30 pessoas por minuto, variando uniformemente.
# Cada elevador tem capacidade máxima de 10 pessoas e demora 2 minutos para subir e descer.
# No prédio trabalham 1000 pessoas.
# O elevador parte quando a lotação máxima é atingida ou quando ficar 1 minuto parado.
# Problema: Determinar qual o número de elevadores necessário para que o
# tempo de espera não seja maior que 1 minuto.


import random
import time
import datetime
import numpy as np


def simular(total_elevadores=1):
    hora_inicio = datetime.datetime(2018, 1, 1, 8, 0, 0, 0)
    hora_chegada = datetime.datetime(2018, 1, 1, 8, 0, 0, 0)
    # datetime.datetime.now() - datetime.timedelta(minutes=15)
    funcionarios_total = 1000
    max_por_min = 30
    min_por_min = 0

    fila = []
    trabalhando = []

    elevadores = []
    for x in range(total_elevadores):
        elevadores.append({'ultima_partida': None,
                           'tempo_viagem': None,
                           'passageiros': [],
                           'quebrado_hora': None,
                           'viagens': 0})

    # hr de chegada individual
    while funcionarios_total > 0:
        chegou = random.randint(min_por_min, max_por_min)
        if (funcionarios_total - chegou) < 0:
            chegou = funcionarios_total
        funcionarios_total -= chegou
        if chegou > 0:
            tec = float(60) / float(chegou)
        else:
            tec = 0
        while chegou > 0:
            fila.append({'hora_chegada': hora_chegada,
                         'hora_elevador': None})
            hora_chegada = hora_chegada + datetime.timedelta(seconds=tec)
            chegou -= 1
        if chegou == 0:
            hora_chegada = hora_chegada + datetime.timedelta(minutes=1)

    # viagens do elevador conforme chegada
    while len(fila) > 0:
        indice = 0
        sorted(elevadores, key=lambda k: len(k['passageiros']), reverse=True)
        for e in elevadores:
            if e['quebrado_hora'] and e['quebrado_hora'] + datetime.timedelta(minutes=20) == hora_inicio:
                # print('arrumou', e['quebrado_hora'], hora_inicio)
                e['quebrado_hora'] = None
            tempo_viagem = np.random.normal(2, 0.1, 1)
            tempo_viagem = tempo_viagem[0]
            if e['ultima_partida'] is not None and e['ultima_partida'] + datetime.timedelta(minutes=((e['tempo_viagem'] or 2) + 1)) == hora_inicio and not(e['quebrado_hora']):
                # print('partiu', tempo_viagem)
                quebrar = np.random.choice([0, 1], p=[0.99, 0.01])
                e['ultima_partida'] = hora_inicio
                e['tempo_viagem'] = tempo_viagem
                e['passageiros'] = []
                e['viagens'] += 1
                if quebrar:
                    # print('quebrou')
                    e['quebrado_hora'] = hora_inicio
                # print('partiu %s' % hora_inicio.strftime("%Y-%m-%d %H:%M"))
            elif len(e['passageiros']) == 10 and not(e['quebrado_hora']):
                # print('partiu', tempo_viagem)
                quebrar = np.random.choice([0, 1], p=[0.99, 0.01])
                e['ultima_partida'] = hora_inicio
                e['tempo_viagem'] = tempo_viagem
                e['passageiros'] = []
                e['viagens'] += 1
                if quebrar:
                    # print('quebrou')
                    e['quebrado_hora'] = hora_inicio
                # print('partiu %s' % hora_inicio.strftime("%Y-%m-%d %H:%M"))
            indice += 1
        if(fila[0]['hora_chegada'] <= hora_inicio):
            for e in elevadores:
                if (not(e['ultima_partida']) or ((e['ultima_partida'] + datetime.timedelta(minutes=(e['tempo_viagem'] or 2))) <= hora_inicio)) and not(e['quebrado_hora']):
                    # print('embarcou', hora_inicio, fila[0]['hora_chegada'])
                    passegeiro = fila.pop(0)
                    passegeiro['hora_elevador'] = hora_inicio
                    e['passageiros'].append(passegeiro)
                    trabalhando.append(passegeiro)
                    break
        hora_inicio = hora_inicio + datetime.timedelta(seconds=1)
        # time.sleep(0.01)
    tempo_espera = None
    for x in trabalhando:
        if not tempo_espera:
            tempo_espera = x['hora_elevador'] - x['hora_chegada']
        if tempo_espera < x['hora_elevador'] - x['hora_chegada']:
            tempo_espera = x['hora_elevador'] - x['hora_chegada']
    tempo_espera = str(tempo_espera).split(':')
    print('Tempo de espera: %s horas, %s minutos, %s segundos' %
          (tempo_espera[0], tempo_espera[1], tempo_espera[2]))
    # print([x['viagens'] for x in elevadores])
ne = input('Até quantos elevadores?\n')
for y in range(1, int(ne) + 1):
    print('Elevadores %s' % (y)) 
    for x in range(10):
        simular(int(y))
