""" This is the file meant to be run
The program will create a database using the file stored in the folder data
Once created the program calls main() from gui.py which displays an interface
"""
import csv
import mysql.connector
from mysql.connector import errorcode

# You might need to change these if you have different setup, I'm using mysql workbench
print("===Establish connection with your database===")
u = input("Database username: ")
p = input("Database password: ")
h = input("Database host: ")

cnx = mysql.connector.connect(
    user=u,
    password=p,
    host=h,
    # unix_socket= '/Applications/MAMP/tmp/mysql/mysql.sock'
)


DB_NAME = "Grishin"

cursor = cnx.cursor()

# Creates database
def create_database(cursor, DB_NAME):

    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)
        )
    except mysql.connector.Error as err:
        print("Faild to create database {}".format(err))
        exit(1)


def create_table_users(cursor):
    # Since database values from files are strange I'm using varchar
    # NOT NULL because I changed NA to Unknown in the files
    create_users = (
        "CREATE TABLE `users` ("
        "  `user_id` int(50) NOT NULL,"
        "  `user_name` varchar(50) NOT NULL,"
        "  `total_anime` int(50) NOT NULL,"
        "  `total_completed` int(50) NOT NULL,"
        "  `total_on_hold` int(50) NOT NULL,"
        "  `total_plantowatch` int(50) NOT NULL,"
        "  `favorite_characters` int(50) NOT NULL,"
        "  PRIMARY KEY (`user_id`)"
        ") ENGINE=InnoDB"
    )
    try:
        print("Creating table users: ")
        cursor.execute(create_users)
        file = open("data/Users_MAL.csv")
        # Get data from the file
        csv_data = csv.reader(file)
        skipHeader = True
        for row in csv_data:
            # Skips first string from a file
            if skipHeader:
                skipHeader = False
                continue
            cursor.execute(
                "INSERT INTO users(user_id, user_name, total_anime, total_completed, total_on_hold, total_plantowatch,favorite_characters)"
                "VALUES(%s, %s, %s, %s, %s, %s,%s)",
                row,
            )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
    else:
        print("OK")


def create_table_anime(cursor):
    # Titles are weird so varchar 255
    create_species = (
        "CREATE TABLE `anime_list` ("
        "  `ID` int(40) NOT NULL,"
        "  `title` varchar(255) NOT NULL,"
        "  `type` char(50) NOT NULL,"
        "  `episodes` int(50) NOT NULL,"
        "  `episodes_watched` int(50) NOT NULL,"
        "  `status` char(50) NOT NULL,"
        "  PRIMARY KEY (`ID`)"
        ") ENGINE=InnoDB"
    )
    try:
        print("Creating table Anime: ")
        cursor.execute(create_species)
        file = open("data/Anime_MAL.csv", encoding="utf-8")
        # Get data from the file
        csv_data = csv.reader(file)
        skipHeader = True
        for row in csv_data:
            # Skips first string from a file
            if skipHeader:
                skipHeader = False
                continue
            cursor.execute(
                "INSERT INTO anime_list(ID,title,type,episodes,episodes_watched,status)"
                "VALUES(%s, %s, %s, %s, %s, %s)",
                row,
            )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")

    else:
        print("OK")
        file = open("data/Anime_MAL.csv", encoding="utf-8")
        # Get data from the file
        csv_data = csv.reader(file)
        skipHeader = True
        for row in csv_data:
            # Skips first string from a file
            if skipHeader:
                skipHeader = False
                continue
            cursor.execute(
                "INSERT INTO anime_list(ID,title,type,episodes,episodes_watched,status)"
                "VALUES(%s, %s, %s, %s, %s, %s)",
                row,
            )


# ONLY ONE WAIFU PER USER.
def create_table_characters(cursor):
    create_waifus = (
        "CREATE TABLE `characters` ("
        "  `ID` int(50) NOT NULL,"
        "  `name` varchar(255) NOT NULL,"
        "  `gender` char(50) NOT NULL,"
        "  `hair` char(50) NOT NULL,"
        "  `blood` char(20) NOT NULL,"
        "  PRIMARY KEY (`ID`)"
        ") ENGINE=InnoDB"
    )
    try:
        print("Creating table Characters: ")
        cursor.execute(create_waifus)
        file = open("data/characters.csv")
        # Get data from the file
        csv_data = csv.reader(file)
        skipHeader = True
        for row in csv_data:
            # Skips first string from a file
            if skipHeader:
                skipHeader = False
                continue
            cursor.execute(
                "INSERT INTO characters(ID,name,gender,hair,blood)"
                "VALUES(%s, %s, %s, %s, %s)",
                row,
            )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
    else:
        print("OK")


def start():
    try:
        cursor.execute("USE {}".format(DB_NAME))
        # If database exists just start
        # Create a database
    except mysql.connector.Error as err:
        print("Database {} does not exist".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor, DB_NAME)
            print("Database {} created succesfully.".format(DB_NAME))
            cnx.database = DB_NAME

            # Create tables and also show if exist.
            """
            Now here you might think why are there are
            so many calls of the same function?
            That's because the mysql.connector is so stupid
            that it won't insert the data after creating the first table
            So the solution is to call the function again and it works...
            """
            create_table_users(cursor)
            create_table_anime(cursor)
            create_table_anime(cursor)
            create_table_characters(cursor)
            create_table_characters(cursor)
            create_table_users(cursor)
            create_table_users(cursor)
            create_table_anime(cursor)
            create_table_anime(cursor)
            create_table_manga(cursor)
            create_table_manga(cursor)
            print()
            # Once created shows menu
        # If not connected there will be an error.
        else:
            print(err)


def create_table_manga(cursor):
    create_species = (
        "CREATE TABLE `manga_list` ("
        "  `title` varchar(255) NOT NULL,"
        "  `type` char(50) NOT NULL,"
        "  `dates` varchar(100) NOT NULL,"
        "  PRIMARY KEY (`title`,`type`,`dates`)"
        ") ENGINE=InnoDB"
    )
    try:
        print("Creating table Manga: ")
        cursor.execute(create_species)
        file = open("data/mangalist.csv", encoding="utf-8")
        # Get data from the file
        csv_data = csv.reader(file)
        skipHeader = True
        for row in csv_data:
            # Skips first string from a file
            if skipHeader:
                skipHeader = False
                continue
            cursor.execute(
                "INSERT INTO manga_list(title, type, dates)" "VALUES(%s, %s, %s)", row,
            )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)


# These function are used in the start.py file because the 'cursor' is initialized here
def end():
    cursor.execute("DROP DATABASE {}".format(DB_NAME))


def show_users():
    from windows import select_users

    select_users(cursor)


def add_user():
    from windows import add_user

    add_user(cursor)


def show_anime():
    from windows import selectanime

    selectanime(cursor)


def choise_menu_anime_type():
    from windows import choise_menu_anime_type

    choise_menu_anime_type(cursor)


def favorite_characters():
    from windows import show_favorite_characters

    show_favorite_characters(cursor)


def anime_with_manga():
    from windows import manga_with_anime_adaptation

    manga_with_anime_adaptation(cursor)


def episodes_total():
    from windows import episodes_watched_total

    episodes_watched_total(cursor)


def character_as_manganame():
    from windows import character_name_as_title

    character_name_as_title(cursor)


def ponetial_waifus_not_blonde():
    from windows import ponetial_waifus_not_blonde

    ponetial_waifus_not_blonde(cursor)


def hair_colors_of_characters():
    from windows import character_hair_color

    character_hair_color(cursor)
