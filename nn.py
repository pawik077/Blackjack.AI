import getopt
import sys
import tensorflow as tf
import numpy as np
import os

def nn1(setName: str):
	with open(f'datasets/{setName}.data', 'r') as f:
		data = [int(l.rstrip()) for l in f.readlines()]
	with open(f'datasets/{setName}.tags', 'r') as f:
		tags = [(1 if l.rstrip() == 'h' else 0) for l in f.readlines()] # that one-liner is fucking beautiful (｡◕‿‿◕｡)
	
	datasize = int(len(data) * 0.75) # 75% of the data is used for training
	train_data = np.array(data[:datasize])
	train_tags = np.array(tags[:datasize])
	test_data = np.array(data[datasize:])
	test_tags = np.array(tags[datasize:])

	model = tf.keras.models.Sequential()
	model.add(tf.keras.layers.Dense(4096, input_dim=1))
	model.add(tf.keras.layers.Dense(2, activation='softmax'))
	model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	model.fit(train_data, train_tags, epochs=100)
	loss, accuracy = model.evaluate(test_data, test_tags)
	print(f'Accuracy: {accuracy}')

	model_json = model.to_json()
	os.makedirs('models', exist_ok=True)
	with open(f'models/{setName}.json', 'w') as json_file:
		json_file.write(model_json)
	model.save_weights(f'models/{setName}.h5')
	print('Saved model to disk')

def nn2(setName: str) :
	with open(f'datasets/{setName}.data', 'r') as f:
		data = [list(map(int,x)) for x in [l.rstrip()[1:-1].replace(' ', '').split(',') for l in f.readlines()]] # that one too (ʘ‿ʘ)
	with open(f'datasets/{setName}.tags', 'r') as f:
		tags = [(1 if l.rstrip() == 'h' else 0) for l in f.readlines()]

	datasize = int(len(data) * 0.75) # 75% of the data is used for training
	train_data = np.array(data[:datasize])
	train_tags = np.array(tags[:datasize])
	test_data = np.array(data[datasize:])
	test_tags = np.array(tags[datasize:])

	model = tf.keras.models.Sequential()
	model.add(tf.keras.layers.Dense(16, input_dim=2))
	model.add(tf.keras.layers.Dense(2, activation='softmax'))
	model.compile(loss='sparse_categorical_crossentropy', optimizer='nadam', metrics=['accuracy'])
	model.fit(train_data, train_tags, epochs=100)
	loss, accuracy = model.evaluate(test_data, test_tags)
	print(f'Accuracy: {accuracy}')

	model_json = model.to_json()
	os.makedirs('models', exist_ok=True)
	with open(f'models/{setName}.json', 'w') as json_file:
		json_file.write(model_json)
	model.save_weights(f'models/{setName}.h5')
	print('Saved model to disk')

def nn3(setName: str):
	with open(f'datasets/{setName}-c.data', 'r') as f:
		data = [list(map(int,x)) for x in [l.rstrip()[1:-1].replace(' ', '').split(',') for l in f.readlines()]]
	with open(f'datasets/{setName}-c.tags', 'r') as f:
		tags = [(1 if l.rstrip() == 'h' else 0) for l in f.readlines()] 

	datasize = int(len(data) * 0.75) # 75% of the data is used for training
	train_data = np.array(data[:datasize])
	train_tags = np.array(tags[:datasize])
	test_data = np.array(data[datasize:])
	test_tags = np.array(tags[datasize:])

	model = tf.keras.models.Sequential()
	model.add(tf.keras.layers.Dense(54, input_dim=54))
	model.add(tf.keras.layers.Dense(64, input_dim=54))
	model.add(tf.keras.layers.Dense(128, input_dim=64))
	model.add(tf.keras.layers.Dense(2, activation='softmax'))
	model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	model.fit(train_data, train_tags, epochs=50)
	loss, accuracy = model.evaluate(test_data, test_tags)
	print(f'Accuracy: {accuracy}')

	model_json = model.to_json()
	os.makedirs('models', exist_ok=True)
	with open(f'models/{setName}.json', 'w') as json_file:
		json_file.write(model_json)
	model.save_weights(f'models/{setName}.h5')
	print('Saved model to disk')

def print_strategy_1(setName: str):
	with open(f'models/{setName}.json', 'r') as json_file:
		model = tf.keras.models.model_from_json(json_file.read(), custom_objects={'GlorotUniform': tf.keras.initializers.glorot_uniform})
	model.load_weights(f'models/{setName}.h5')
	print(model.summary())
	print(f'Dataset: {setName}')
	for i in range(21):
		prediction = model.predict(np.array([i, 10]))
		if prediction[0][0] > prediction[0][1]:
			print(f'{i} -> s')
		else:
			print(f'{i} -> h')
	
def print_strategy_2(setName: str):
	with open(f'models/{setName}.json', 'r') as json_file:
		model = tf.keras.models.model_from_json(json_file.read(), custom_objects={'GlorotUniform': tf.keras.initializers.glorot_uniform})
	model.load_weights(f'models/{setName}.h5')
	print(model.summary())
	print(f'Dataset: {setName}')
	results = []
	for i in range(17):
		results.append([])
		for j in range(9):
			prediction = model.predict(np.array([[i + 5, j + 2]]))
			if prediction[0][0] > prediction[0][1]:
				results[i].append('s')
			else:
				results[i].append('h')
	print('   ', end='')
	for x in range(len(results[0])):
		print(f' {str((x + 4) % 10)}', end='')
	print()
	for i in range(len(results)):
		print(f'{i + 5}', end='')
		print('  ' if i + 5 < 10 else ' ', end='')
		for j in range(len(results[i])):
			print(f' {results[i][j]}', end='')
		print()



if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'l:d:pn', ['level=', 'dataset=', 'neural', 'print'])
	except getopt.GetoptError as err:
		print(f'Error: {err}')
		sys.exit(2)

	nn = False
	do_print = False
	level = 0
	dataset = ''

	for o,a in opts:
		if o in ('-l', '--level'):
			level = int(a)
		elif o in ('-d', '--dataset'):
			dataset = a
		elif o in ('-n', '--neural'):
			nn = True
		elif o in ('-p', '--print'):
			do_print = True
	if nn and do_print:
		print('Usage: python3 nn.py [-n | -p] -l <level> -d <dataset>')
		sys.exit(1)
	if level == 0 or dataset == '':
		print('Usage: python3 nn.py [-n | -p] -l <level> -d <dataset>')
		sys.exit(1)
	elif nn:
		match level:
			case '1':
				nn1(dataset)
			case '2':
				nn2(dataset)
			case '3':
				nn3(dataset)
			case _:
				print('Usage: python3 nn.py -l <level> -d <dataset>')
				sys.exit(1)
	elif do_print:
		match level:
			case '1':
				print_strategy_1(dataset)
			case '2':
				print_strategy_2(dataset)
			case _:
				print('Usage: python3 nn.py -l <level> -d <dataset>')
				sys.exit(1)