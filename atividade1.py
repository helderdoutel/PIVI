# Os funcionários de uma empresa chegam a uma taxa de até 30 pessoas por minuto, variando uniformemente.
# Cada elevador tem capacidade máxima de 10 pessoas e demora 2 minutos para subir e descer.
# No prédio trabalham 1000 pessoas.
# O elevador parte quando a lotação máxima é atingida ou quando ficar 1 minuto parado.
# Problema: Determinar qual o número de elevadores necessário para que o tempo de espera não seja maior que 1 minuto.


import random
import time
import datetime

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
						   'passageiros': []})

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
		for e in elevadores:
			if e['ultima_partida'] is not None and e['ultima_partida'] + datetime.timedelta(minutes=3) == hora_inicio:
				e['ultima_partida'] = hora_inicio
				e['passageiros'] = []
				# print('partiu %s' % hora_inicio.strftime("%Y-%m-%d %H:%M"))
			elif len(e['passageiros']) == 10:
				e['ultima_partida'] = hora_inicio
				e['passageiros'] = []
				# print('partiu %s' % hora_inicio.strftime("%Y-%m-%d %H:%M"))
		if(fila[0]['hora_chegada'] <= hora_inicio):
			for e in elevadores:
				if not(e['ultima_partida']) or (e['ultima_partida'] + datetime.timedelta(minutes=2) < hora_inicio):
					# print('embarcou')
					passegeiro = fila.pop(0)
					passegeiro['hora_elevador'] = hora_inicio
					e['passageiros'].append(passegeiro)
					trabalhando.append(passegeiro)
					break
		hora_inicio = hora_inicio + datetime.timedelta(seconds=1)
		# time.sleep(1)
	tempo_espera = None 
	for x in trabalhando:
		if not tempo_espera:
			tempo_espera = x['hora_elevador'] - x['hora_chegada']
		if tempo_espera < x['hora_elevador'] - x['hora_chegada']:
			tempo_espera = x['hora_elevador'] - x['hora_chegada']
	tempo_espera = str(tempo_espera).split(':')
	print('Tempo de espera: %s horas, %s minutos, %s segundos' % (tempo_espera[0], tempo_espera[1], tempo_espera[2]))
ne = input('Quantos elevadores?\n')
simular(int(ne))