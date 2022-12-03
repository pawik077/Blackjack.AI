import sys
from getopt import getopt

def cleanDataset(setName: str, outputName: str):
	'''Cleans the dataset by removing duplicate and conflicting entries'''
	with open(f'datasets/{setName}.data', 'r') as f:
		data = f.readlines()
	
	with open(f'datasets/{setName}.tags', 'r') as f:
		tags = f.readlines()

	print(f'Original dataset size: {len(data)}')

	dataFile = open(f'{outputName}.data', 'w')
	tagsFile = open(f'{outputName}.tags', 'w')
	init = {}
	seen = []
	total = 0

	# number of duplicates
	for i in range(len(data)):
		key = data[i].strip() + ':' + tags[i].strip()
		if key in init:
			init[key] += 1
		else:
			init[key] = 1

	for key in init:
		try:
			#print('key: ' + key + ' value: ' + str(init[key])) #debug
			if key[-1] == 'h':
				reverse = key[:-1] + 's'
			else:
				reverse = key[:-1] + 'h'
			#print('reverse: ' + reverse) #debug
			if key in seen:
				continue
			if reverse in init:
				# if the reverse is in the dataset, remove the one with the lower count
				if init[reverse] > init[key]:
					data = reverse.split(':')[0]
					tag = reverse.split(':')[1]
					dataFile.write(data + '\n')
					tagsFile.write(tag + '\n')
					seen.append(key)
					seen.append(reverse)
					total += 1
				else:
					data = key.split(':')[0]
					tag = key.split(':')[1]
					dataFile.write(data + '\n')
					tagsFile.write(tag + '\n')
					seen.append(key)
					total += 1
			else:
				data = key.split(':')[0]
				tag = key.split(':')[1]
				dataFile.write(data + '\n')
				tagsFile.write(tag + '\n')
				total += 1
		except Exception as ex:
			print(ex)
			print(key)
			print(init[key])
			return
	print(f'Cleaned dataset size: {total}')
	dataFile.close()
	tagsFile.close()

if __name__ == '__main__':
	opts, args = getopt(sys.argv[1:], 'd:o:', ['dataset=', 'output='])

	dataset = ''
	output = ''

	for o, a in opts:
		if o in ('-d', '--dataset'):
			dataset = a
		elif o in ('-o', '--output'):
			output = a
	
	if dataset == '':
		print('Usage: python data.py -d <dataset> [-o <output>]')
		exit(1)
	if output == '':
		output = f'{dataset}-c'

	cleanDataset(dataset, output)
