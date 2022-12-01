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
	nn2('train2')