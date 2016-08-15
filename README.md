# pokemon-csv-to-map
Converts a pogom database to a csv file, that is easily readable by google maps.    
Can help with identifying nests.

# Example usage:

`csvparse.py pogom.db -n 2 -t Eevee` - outputs all places in which Eevee spawned at least 2 times to Eevee.csv.    
`csvparse.py pogom.db -t 16 -o out.csv` - outputs all places in which Pidgey (pokedex no. 16) spawned at least 2 times to out.csv.    
`csvparse.py pogom.db -o allpokemon.csv` - outputs every place in which at least 1 pokemon spawned to allpokemon.csv.    
`csvparse.py pogom.db -n 10 -o allpokemon10.csv` - outputs every place in which at least 10 pokemon spawned to allpokemon10.csv.

# Example map output:

![map](http://puu.sh/qC9Wy/b1f18057aa.png)
