#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import requests
import xml.etree.ElementTree as ET
import time

file_in = "collection_id.csv"
file_out = "collection_bgg.csv"

URL_DEF = 'http://www.boardgamegeek.com/xmlapi2/thing?id='

def get_game(id):
  try:
    error = True
    while error:
      r = requests.get(URL_DEF + id)
      tree = ET.fromstring(r.text.encode('utf8'))
      if tree.tag == 'error':
        time.sleep(10)
      else: 
        error = False
        
    minplayers = tree.find('item/minplayers')
    maxplayers = tree.find('item/maxplayers')
    minplaytime = tree.find('item/minplaytime')
    maxplaytime = tree.find('item/maxplaytime')
    minage = tree.find('item/minage')
    
    nombre = ""
    for name in tree.find('item').iter('name'):
      if name.get('type') == 'primary':
        nombre = name.get('value')
    
    suggested_players = ""
    num_votes = 0
    language_dependence = ""
    num_votes_ld = 0
    
    for poll in tree.find('item').iter('poll'):
      if poll.get('name') == 'suggested_numplayers':
        for res in poll.iter('results'):
          numplayers = res.get('numplayers')
          for r in res.iter('result'):
            if r.get('value') == 'Best':
              votes_poll = int(r.get('numvotes'))
              if num_votes < votes_poll:
                num_votes = votes_poll
                suggested_players = numplayers
      elif poll.get('name') == 'language_dependence':
        if len(poll.findall('results/result')) > 0:
          for r in poll.find('results').iter('result'):
            votes_poll = int(r.get('numvotes'))
            if num_votes_ld < votes_poll:
              num_votes_ld = votes_poll
              language_dependence = r.get('value')
  
    return (id, nombre, minplayers.get('value'), maxplayers.get('value'), suggested_players,
            minplaytime.get('value'), maxplaytime.get('value'), minage.get('value'), language_dependence)
  except AttributeError as err:
    print "Unexpected error:", err
    print "game: " + id
    print "item: " + r.text.encode('utf8')
    return (id, nombre.decode('utf-8').encode('utf-8'), "", "", "", "", "", "", "", "")


def main(argv):
  global file_in  
  global file_out
  # Validamos entrada
  try:
    opts, args = getopt.getopt(argv, "hf:o:")
  except getopt.GetoptError as err:
    print err
    print 'usage: python bgg_thing.py [-f <input_file>] [-o <output_file>]'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'usage: python bgg_thing.py [-f <input_file>] [-o <output_file>]'
      sys.exit()
    elif opt == "-f":
        file_in = arg
    elif opt == "-o":
        file_out = arg

  print "Fichero Entrada: ", file_in
  print "Fichero Salida: ", file_out

  with open(file_in) as f:
    games = f.readlines()
    
  with open(file_out, 'w') as fp:
    header = "ID,Nombre,Min Jugadores,Max Jugadores,Jugadores Recomendados,Min Duración,Max Duración,Edad Minima,Independencia Idioma" + '\n'
    fp.write(header)
    for game in games:
      tupla = get_game(game.rstrip())
      print tupla
      line = ','.join(str(s.encode('utf-8')) for s in tupla) + '\n'
      fp.write(line)
    fp.close()


if __name__ == "__main__":
  main(sys.argv[1:])
    