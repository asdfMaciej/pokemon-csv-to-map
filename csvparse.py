import csv
import datetime
import argparse
import sqlite3


class MainClass:
	def __init__(self):
		with open('pokemony.txt', 'r') as poksy_f:
			self.poksy = poksy_f.readlines()

	def despawn_to_spawn(self, time_str):
		date_object = datetime.datetime.strptime(time_str, '%H:%M:%S')
		date_object = date_object.replace(year=2016)
		date_object = date_object - datetime.timedelta(minutes=15)
		return date_object.strftime('%H:%M:%S')

	def parse_pokemon(self, place, wanted_pokemon='', nest=0):
		place_array = []
		place_array.append(place[0][0])
		place_array.append(place[0][1])

		poke_dict = {}
		disappear_list = []
		appear_list = []
		unique_ids = []

		for item in place:
			if item[2] != 'pokemon_id':
				if item[4] not in unique_ids:
					unique_ids.append(item[4])
				else:
					continue  # skip one loop iteration
				poke_str = self.poksy[int(item[2])-1][:-1]
				if wanted_pokemon not in ('', []):
					isin = False
					for poke in wanted_pokemon:
						if str(poke) in (poke_str, item[2]):
							isin = True
					if not isin:
						continue

				if poke_str not in poke_dict:
					poke_dict[poke_str] = 0
				poke_dict[poke_str] += 1
				ddd = item[3].split(' ')[1].split('.')[0]
				disappear_list.append(ddd)
				ddd_appear = self.despawn_to_spawn(ddd)
				appear_list.append(ddd_appear)

		poke_str = ""
		disappear_str = ""
		appear_str = ""

		for pokemon_n, quantity in poke_dict.iteritems():
			poke_str += pokemon_n + " x " + str(quantity) + " | "
		for d in disappear_list:
			disappear_str += d + " | "
		for d in appear_list:
			appear_str += d + " | "
		
		place_array.append(poke_str)
		place_array.append(appear_str)
		place_array.append(disappear_str)

		if place_array[2]:
			if wanted_pokemon:
				total_poke = 0
				for poke in wanted_pokemon:
					if poke.isdigit():
						poke_str = self.poksy[int(wanted_pokemon)-1][:-1]
					else:
						poke_str = poke

					try:
						total_poke += int(poke_dict[poke_str])
					except KeyError:
						pass

				if total_poke >= nest:
					return place_array
			else:
				total = 0
				for key, item in poke_dict.iteritems():
					total += int(item)
				if total >= nest:
					return place_array
		
		return None

	def parse_csv(self, filename):
		if '.db' in filename:
			conn = sqlite3.connect(filename)
			cursor = conn.cursor()
			cursor.execute("select * from pokemon;")
			new_filename = filename.split('.')[0]+'csv.csv'
			with open(new_filename, "wb") as csv_file:
				csv_writer = csv.writer(csv_file)
				csv_writer.writerow([i[0] for i in cursor.description]) # write headers
				csv_writer.writerows(cursor)
			csvfile = open(new_filename, 'rb')
		else:
			csvfile = open(filename)

		reader = csv.reader(csvfile, delimiter=',')
		csvarray = []
		for row in reader:
			csvarray.append(row)

		dict_ = {}
		for row in csvarray:
			if row[1] not in dict_:
				dict_[row[1]] = []
			add_ = []
			add_.append(row[3])  # latitude
			add_.append(row[4])  # longitude
			add_.append(row[2])  # pokemon
			add_.append(row[5])  # disappear time
			add_.append(row[0])  # encounter id
			dict_[row[1]].append(add_)

		return dict_

class InputHandler:
	def __init__(self):
		self.parser = argparse.ArgumentParser()
		self.parser.add_argument("input", help="The input csv file.")
		self.parser.add_argument(
			"-o", "--output",
			help="The output csv file, defaults to pokemon.csv.",
			default="pokemon.csv"
			)
		self.parser.add_argument(
			"-n", "--nest",
			help="Output only nests with specified amount of pokemon.",
			type=int, default=0
		)
		self.parser.add_argument(
			"-t", "--type",
			help="Output only certain pokemon, for ex. Zubat or 143.",
			default="",
			nargs="*"
		)

	def parse_args(self):
		return self.parser.parse_args()

class MainRunner:  
	def __init__(self):
		self.mainclass = MainClass()
		self.inputhandler = InputHandler()

	def run(self):
		args = self.inputhandler.parse_args()
		_input = args.input
		_output = args.output
		_type = args.type
		if _output == 'pokemon.csv' and _type:
			_output = ' '.join(_type)+'.csv'
		_nest = args.nest

 		dict_ = self.mainclass.parse_csv(_input)
		sorted_dict = [['latitude', 'longitude', 'pokemon', 'appear_times', 'disappear_times']]
		for useless, place in dict_.iteritems():
			place_array = self.mainclass.parse_pokemon(
				place, wanted_pokemon=_type, nest=_nest
			)
			if place_array:
				sorted_dict.append(place_array)

		end_result = ""
		for line in sorted_dict:
			end_result += ','.join(line)+'\n'

		koncowe = open(_output, 'w')
		koncowe.write(end_result)
		koncowe.close()

if __name__ == '__main__':
	main = MainRunner()
	main.run()
