import csv


poksy_f = open('pokemony.txt', 'r')
poksy = poksy_f.readlines()
poksy_f.close()

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
	dict_[row[1]].append(add_)

sorted_dict = [['latitude', 'longitude', 'pokemon', 'times']]
for useless, place in dict_.iteritems():
	place_array = []
	place_array.append(place[0][0])
	place_array.append(place[0][1])

	poke_dict = {}
	disappear_list = []

	for item in place:
		if item[2] != 'pokemon_id':
			poke_str = poksy[int(item[2])-1][:-1]
			if poke_str not in poke_dict:
				poke_dict[poke_str] = 0
			poke_dict[poke_str] += 1
			ddd = item[3].split(' ')[1].split('.')[0]
			disappear_list.append(ddd)

	poke_str = ""
	disappear_str = ""

	for pokemon_n, quantity in poke_dict.iteritems():
		poke_str += pokemon_n + " x " + str(quantity) + " | "
	for d in disappear_list:
		disappear_str += d + " | "
	
	place_array.append(poke_str)
	place_array.append(disappear_str)
	sorted_dict.append(place_array)

end_result = ""
for line in sorted_dict:
	end_result += ','.join(line)+'\n'

koncowe = open('final.csv', 'w')
koncowe.write(end_result)
koncowe.close()



#for x in sorted_dict:
#	print x + ', spawns: ' + str(dict_[x])