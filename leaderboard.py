"""@package docstring
   leaderboard.py is in charge of handling the mySQL database for the leaderboards. Specifically, it gets passed the song name, mode, difficulty and score
   and checks for songs that have the same name, mode, and difficulty to determine if you have a high score.  It is in charge of adding new scores, checking scores,
   and printing out the top scores.
"""
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
    """
    @pre song_name is a file name with .wav
    @param song_name: The name of the song file
    @param mode: The game mode that is played, either 1 for regular or 2 for osu
    @param difficulty: the difficulty of the game, being 1,2, or 3 for easy, medium, or hard
    @param score: The score of the game
    @post Will take in the variables and compare them to mySQL database.  Will add it as new high score if it is top 10, and then will print out the top 10.
    """
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
    """
    @pre none
    @param song_name: The name of the song file
    @param mode: The game mode that is played, either 1 for regular or 2 for osu
    @param difficulty: the difficulty of the game, being 1,2, or 3 for easy, medium, or hard
    @param player_score: The score of the game
    @post Checks if the given player score is within the top 10 for that song, mode, and difficulty in the mySQL table
    @return true if the score is in the top 10, false if it is not
    """
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
    """
    @pre none
    @param song_name: The name of the song file
    @param mode: The game mode that is played, either 1 for regular or 2 for osu
    @param difficulty: the difficulty of the game, being 1,2, or 3 for easy, medium, or hard
    @param player_name: The name of the individual who got the score
    @param player_score: The score of the game
    @post Adds an entry to the mySQL table with all of these parameters
    """
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
    """
    @pre none
    @param song_name: The name of the song file
    @param mode: The game mode that is played, either 1 for regular or 2 for osu
    @param difficulty: the difficulty of the game, being 1,2, or 3 for easy, medium, or hard
    @post Prints out the top 10 entries in the table Leaderboard that have the same song_name, mode, and difficulty
    """
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
