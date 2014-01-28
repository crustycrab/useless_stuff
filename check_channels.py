import argparse
import shelve
import json

try:
	from urllib.request import urlopen
	from urllib.parse import urlencode
except ImportError:
	from urllib2 import urlopen
	from urllib import urlencode

DATAFILE = '.data'


def parse_streams(count, **params):
	streams = []
	url = 'https://api.twitch.tv/kraken/streams?%s'%urlencode(params)
	count_pages = count // 100
	while True:
		data = urlopen(url).read()
		data = data.decode('utf-8')
		info = json.loads(data)
		streams += info['streams']
		if len(info['streams']) == 0 or info['streams'][len(info['streams']) - 1]['viewers'] == 0 or count_pages == 0:
			break
		url = info['_links']['next']
		count_pages -= 1

	for i in range(len(streams)):
		if streams[-1]['viewers'] == 0:
			del streams[-1]
	if len(streams) > count:
		streams = streams[0:count]
	return streams


def get_by_favs(favs):
	favorites = ([], [])
	url = 'https://api.twitch.tv/kraken/streams/'
	for fav in favs:
		data = urlopen(url + fav).read()
		data = data.decode('utf-8')
		info = json.loads(data)['stream']
		if info != None:
			favorites[0].append(info)
		else:
			favorites[1].append(fav)
	return favorites


def store_favs(favs, data):
	if data.get('favs') == None:
		data['favs'] = []
	if favs != None:
		for fav in favs:
			streamer = fav.replace(
				'http://www.twitch.tv/', '').replace('/', '')
			if streamer not in data['favs']:
				data['favs'] = data['favs'] + [streamer]


def del_favs(favs, data):
	if favs != None:
		for fav in favs:
			if fav in data['favs']:
				delIndex = data['favs'].index(fav)
				data['favs'] = data['favs'][
					0:delIndex] + data['favs'][-1:delIndex:-1]


def table_streams(streams, pad=0, game=None):
	max_name = 0
	max_viewers = 0
	table_streams = []
	for stream in streams:
		max_name = max(max_name, len(stream['channel']['display_name']))
	if game != None:
		table_streams.append([('{:>%d}'%(max_name)).format(game), ''])
	for stream in streams:
		table_streams.append(
			[('{:<%d} ' % (max_name+pad)).format(stream['channel']['display_name']),
			 '{}'.format(stream['viewers'])])
	return table_streams


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-a', '--add', action='append', help='Add ur favorite player')
	parser.add_argument(
		'-d', '--delete', action='append', help='Delete ur unloved player')
	parser.add_argument(
		'-g', '--game', action='store', help='Sorted streams by game')
	parser.add_argument(
		'-f', '--favs', action='store_true', help='Sorted streams by game')
	parser.add_argument('-c', '--count', type=int, action='store')
	parser.add_argument('-p', '--padding', type=int, action='store')

	args = parser.parse_args()

	data = shelve.open(DATAFILE)
	store_favs(args.add, data)
	del_favs(args.delete, data)

	if args.count == None:
		args.count = -1
	if args.padding == None:
		args.padding = 0

	if args.game != None:
		streams = parse_streams(args.count, game=args.game, limit=100)
		buf_streams = table_streams(streams, args.padding, args.game)
		for stream in buf_streams:
			print(stream[0] + stream[1])
	if args.favs == True:
		favorites = get_by_favs(data['favs'])
		buf_streams = table_streams(favorites[0], args.padding)
		if buf_streams == 0:
			print('zZZzzz... Ugh, noone of ur favorites streaming right now :(')
		for stream in buf_streams:
			print(stream[0] + stream[1])
		for stream in favorites[1]:
			print('%s .. Offline' % stream)

	data.close()

if __name__ == '__main__':
	main()
