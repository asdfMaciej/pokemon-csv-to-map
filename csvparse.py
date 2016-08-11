import csv
import datetime


class Mainclass:
	def __init__(self):
		with open('pokemony.txt', 'r') as poksy_f:
			self.poksy = poksy_f.readlines()

	def despawn_to_spawn(self, time_str):
		date_object = datetime.datetime.strptime(time_str, '%H:%M:%S')
		date_object = date_object.replace(year=2016)
		date_object = date_object - datetime.timedelta(minutes=15)
		return date_object.strftime('%H:%M:%S')

	def parse_nest(self, place, wanted_pokemon='', nest=False):
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
				if wanted_pokemon and poke_str != wanted_pokemon:
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
			if nest:
				if int(poke_dict[wanted_pokemon]) > 1:
					return place_array
			else:
				return place_array
		
		return None

csvparse = Mainclass()

csvfile = open('testestst.csv', 'rb')
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

sorted_dict = [['latitude', 'longitude', 'pokemon', 'appear_times', 'disappear_times']]
for useless, place in dict_.iteritems():
	place_array = csvparse.parse_nest(place, wanted_pokemon='Drowzee', nest=True)
	if place_array:
		sorted_dict.append(place_array)

end_result = ""
for line in sorted_dict:
	end_result += ','.join(line)+'\n'

koncowe = open('drowzee.csv', 'w')
koncowe.write(end_result)
koncowe.close()




#for x in sorted_dict:
#	print x + ', spawns: ' + str(dict_[x])