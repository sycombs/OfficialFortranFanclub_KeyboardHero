import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'n089p351',
  'password': 'npelletier',
  'host': '127.0.0.1',
  'database': 'eecs_projects',
  'raise_on_warnings': True
}

difficultyRank = ['easy', 'medium', 'hard']

def leaderboard_control(song_name, mode, difficulty, score):
    song_name = song_name[:-4]
    if check_score(song_name, mode, difficulty, score):
        print('Congratulations! You got a High Score!\n')
        player_name = input('Enter Name:')
        add_score(song_name, mode, difficulty, player_name, score)
        print('Highscores for', song_name, 'on', difficultyRank[difficulty-1], ':\nRank\tPlayer\t\tScore')
        print_scores(song_name, mode, difficulty)

    else:
        print('Highscores for', song_name, 'on ', difficultyRank[difficulty-1], ':\nRank\tPlayer\t\tScore')
        print_scores(song_name, mode, difficulty)

def check_score(song_name, mode, difficulty, player_score):
    count = 1
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    search_details = (song_name, mode, difficulty)
    search_scores = ("SELECT player_name, score FROM leaderboard WHERE song_name = %s AND mode = %s AND difficulty = %s ORDER BY score DESC")
    cursor.execute(search_scores, search_details)

    results = cursor.fetchall()

    cursor.close()
    cnx.close()

    for (player_name, score) in results:
      if(player_score>score):
        return True
      count = count+1
      if count > 10:
          return False

    return True

def add_score(song_name, mode, difficulty, player_name, score):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    add_new_score = ("INSERT INTO leaderboard "
                 "(song_name, mode, difficulty, player_name, score) "
                 "VALUES (%s, %s, %s, %s, %s)")
    score_data = (song_name, mode, difficulty, player_name, score)
    cursor.execute(add_new_score, score_data)
    cnx.commit()
    cursor.close()
    cnx.close()

def print_scores(song_name, mode, difficulty):
    count = 1
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    search_detail = (song_name, mode, difficulty)
    search_score = ("SELECT player_name, score FROM leaderboard WHERE song_name = %s AND mode = %s AND difficulty = %s ORDER BY score DESC")
    cursor.execute(search_score, search_detail)

    results = cursor.fetchall()

    cursor.close()
    cnx.close()

    for (player_name, score) in results:
      print("{}\t{}\t\t{}".format(count, player_name, score))
      count = count+1
      if count > 10:
        break
