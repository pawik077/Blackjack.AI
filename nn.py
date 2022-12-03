import getopt
import sys

def nn1(setName: str):
	with open(f'datasets/{setName}-c.data', 'r') as f:
		data = [int(l.rstrip()) for l in f.readlines()]
	with open(f'datasets/{setName}-c.tags', 'r') as f:
		tags = [(1 if l.rstrip() == 'h' else 0) for l in f.readlines()] # that one-liner is fucking beautiful (｡◕‿‿◕｡)

	pass

def nn2(setName: str) :
	with open(f'datasets/{setName}-c.data', 'r') as f:
		data = [list(map(int,x)) for x in [l.rstrip()[1:-1].replace(' ', '').split(',') for l in f.readlines()]] # that one too (ʘ‿ʘ)
	with open(f'datasets/{setName}-c.tags', 'r') as f:
		tags = [(1 if l.rstrip() == 'h' else 0) for l in f.readlines()]

	pass

def nn3(setName: str):
	with open(f'datasets/{setName}-c.data', 'r') as f:
		data = [list(map(int,x)) for x in [l.rstrip()[1:-1].replace(' ', '').split(',') for l in f.readlines()]]
	with open(f'datasets/{setName}-c.tags', 'r') as f:
		tags = [(1 if l.rstrip() == 'h' else 0) for l in f.readlines()] 

	pass


if __name__ == '__main__':
	try:
		opts, args = getopt(sys.argv[1:], 'l:d:', ['level=', 'dataset='])
	except getopt.GetoptError as err:
		print(f'Error: {err}')
		sys.exit(2)

	nn = ''
	dataset = ''

	for o,a in opts:
		if o in ('-n'):
			nn = a
		elif o in ('-d'):
			dataset = a

	if nn == '' or dataset == '':
		print('Usage: python3 nn.py -l <level> -d <dataset>')
		sys.exit(1)
	else:
		match nn:
			case '1':
				nn1(dataset)
			case '2':
				nn2(dataset)
			case '3':
				nn3(dataset)
			case _:
				print('Usage: python3 nn.py -l <level> -d <dataset>')
				sys.exit(1)