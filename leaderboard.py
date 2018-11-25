import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'n089p351',
  'password': 'npelletier',
  'host': '127.0.0.1',
  'database': 'eecs_projects',
  'raise_on_warnings': True
}

def add_score(song_name, difficulty, player_name, score):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    add_new_score = ("INSERT INTO leaderboard "
                 "(song_name, difficulty, player_name, score) "
                 "VALUES (%s, %s, %s, %s)")
    score_data = (song_name, difficulty, player_name, score)
    cursor.execute(add_new_score, score_data)
    cnx.commit()
    cursor.close()
    cnx.close()

def print_scores(song_name, difficulty):
    count = 9
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    search_details(song_name, difficulty)
    search_scores("SELECT player_name, score FROM leaderboard WHERE song_name = %s AND difficulty = %s ORDER BY score")
    cursor.execute(search_people, people_data)

    results = cursor.fetchall()

    cursor.close()
    cnx.close()

    for (player_name, score) in results:
      print("{}\t {}".format(player_name, score))
      count--
      if count == 0:
          break
