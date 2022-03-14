"""
This file is responsible for creating
individual windows for each query
"""

import PySimpleGUI as sg

# Look at the users table
def select_users(myCursor):
    val1 = []
    myCursor.execute(
        "select user_id,user_name,total_anime,total_completed,total_on_hold,total_plantowatch,characters.name from users JOIN characters ON users.favorite_characters=characters.ID;"
    )
    for i in myCursor:
        val1.append(list(i))
    headers = [
        "User ID",
        "Username",
        "Total Anime",
        "Completed",
        "On Hold",
        "Planned To Watch",
        "Waifu",
    ]
    sg.theme("DarkBlue3")
    layout1 = [
        [
            sg.Table(
                headings=headers,
                values=val1,
                display_row_numbers=False,
                enable_events=True,
                justification="c",
                key="-table-",
                font=("Arial", 14),
            )
        ],
    ]

    mainLayout = [[sg.Column(layout1)]]
    window = sg.Window("Users", mainLayout, resizable=True)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break


# Look at anime_list table
def selectanime(myCursor):
    val1 = []
    myCursor.execute("select * from anime_list")
    for i in myCursor:
        val1.append(list(i))
    headers = [
        "Series ID",
        "Title",
        "Type",
        "Episodes",
        "Watched Episodes",
        "Status",
    ]
    sg.theme("DarkBlue3")
    layout1 = [
        [
            sg.Table(
                headings=headers,
                values=val1,
                display_row_numbers=False,
                enable_events=True,
                justification="c",
                key="-table-",
                font=("Arial", 14),
            )
        ],
    ]

    mainLayout = [[sg.Column(layout1)]]
    window = sg.Window("Anime", mainLayout, resizable=False)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break


# Used to testing just ignore / might remove later / no button for this
def add_user(cursor):

    layout = [
        [
            sg.Text("User ID", size=(22, 1)),
        ],
        [sg.InputText((), key="-ID-")],
        [
            sg.Text("Username", size=(22, 1)),
        ],
        [sg.InputText((), key="-USERNAME-")],
        [
            sg.Text("Total Anime", size=(22, 1)),
        ],
        [sg.InputText((), key="-ANIME-")],
        [
            sg.Text("Total Completed", size=(22, 1)),
        ],
        [sg.InputText((), key="-COMPLETED-")],
        [
            sg.Text("Total On Hold", size=(22, 1)),
        ],
        [sg.Input((), key="-HOLD-")],
        [
            sg.Text("Total Plan To Watch", size=(22, 1)),
        ],
        [sg.Input((), key="-PLANNED-")],
        [
            sg.Text("Waifu ID", size=(22, 1)),
        ],
        [sg.Input((), key="-WAIFU-")],
        [sg.Submit()],
    ]

    window = sg.Window("Add User", layout)
    event, values = window.read()

    userid = values["-ID-"]
    username = values["-USERNAME-"]
    total_anime = values["-ANIME-"]
    completed = values["-COMPLETED-"]
    on_hold = values["-HOLD-"]
    planned = values["-PLANNED-"]
    waifu = values["-WAIFU-"]
    cursor.execute(
        "INSERT INTO users(user_id, user_name, total_anime, total_completed, total_on_hold, total_plantowatch,favorite_characters)"
        "VALUES({},'{}',{},{},{},{},{})".format(
            userid, username, total_anime, completed, on_hold, planned, waifu
        ),
    )

    window.close()


# Look at planned animes
def select_all_planned(myCursor):
    val1 = []
    myCursor.execute(
        "SELECT title,type ,status FROM Grishin.anime_list WHERE status='Plan to Watch' ORDER BY title ASC;"
    )
    for i in myCursor:
        val1.append(list(i))
    headers = ["Title", "Type", "Status"]
    sg.theme("DarkBlue3")
    layout1 = [
        [
            sg.Table(
                headings=headers,
                values=val1,
                display_row_numbers=False,
                enable_events=True,
                justification="c",
                key="-table-",
                font=("Arial", 14),
            )
        ],
    ]

    mainLayout = [[sg.Column(layout1)]]
    window = sg.Window("Planned", mainLayout, resizable=True)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break


# Shows all completed animes
def select_all_completed(myCursor):
    val1 = []
    myCursor.execute(
        "SELECT title,type ,status FROM Grishin.anime_list WHERE status='Completed';"
    )
    for i in myCursor:
        val1.append(list(i))
    headers = ["Title", "Type", "Status"]
    sg.theme("DarkBlue3")
    layout1 = [
        [
            sg.Table(
                headings=headers,
                values=val1,
                display_row_numbers=False,
                enable_events=True,
                justification="c",
                key="-table-",
                font=("Arial", 14),
            )
        ],
    ]

    mainLayout = [[sg.Column(layout1)]]
    window = sg.Window("Completed", mainLayout, resizable=True)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break


# Includes in itself two functions above
def choise_menu_anime_type(myCursor):
    layout = [
        [sg.Text("My Window")],
        [
            sg.Combo(
                ["Completed", "Plan To Watch"],
                size=(10, 5),
                key="-C-",
                enable_events=True,
            )
        ],
        [sg.Text(size=(12, 1), key="-OUT-")],
        [sg.Button("Go"), sg.Button("Exit")],
    ]

    window = sg.Window("Choise", layout, finalize=True)
    window["-C-"].bind("<KeyRelease>", "KEY DOWN")

    while True:  # Event Loop
        event, values = window.read()
        print(values)
        if event == "Go" and values == {"-C-": "Plan To Watch"}:
            print("success")
            select_all_planned(myCursor)
        if event == "Go" and values == {"-C-": "Completed"}:
            select_all_completed(myCursor)

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "-C-KEY DOWN":
            window["-C-"].Widget.event_generate("<Down>")
    window.close()


# One character each user has
def show_favorite_characters(myCursor):
    val1 = []
    myCursor.execute(
        "SELECT users.user_name, name FROM characters INNER JOIN users ON users.favorite_characters=characters.ID WHERE users.user_id='14375084';"
    )
    for i in myCursor:
        val1.append(list(i))
    headers = ["ID", "name"]
    sg.theme("DarkBlue3")
    layout1 = [
        [
            sg.Table(
                headings=headers,
                values=val1,
                display_row_numbers=False,
                enable_events=True,
                justification="c",
                key="-table-",
                font=("Arial", 14),
            )
        ],
    ]

    mainLayout = [[sg.Column(layout1)]]
    window = sg.Window("Character", mainLayout, resizable=True)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break


# Might implement later
def series_largerthan24():
    pass


# Show manga that has an anime adaptation
def manga_with_anime_adaptation(myCursor):
    val1 = []
    myCursor.execute(
        "SELECT manga_list.title,manga_list.type FROM Grishin.manga_list JOIN anime_list ON anime_list.title=manga_list.title WHERE anime_list.status ='Plan To Watch' GROUP BY manga_list.title, manga_list.type ORDER BY manga_list.title;"
    )
    for i in myCursor:
        val1.append(list(i))
    headers = ["Title", "Manga volumes"]
    sg.theme("DarkBlue3")
    layout1 = [
        [
            sg.Table(
                headings=headers,
                values=val1,
                display_row_numbers=False,
                enable_events=True,
                justification="c",
                key="-table-",
                font=("Arial", 14),
            )
        ],
    ]

    mainLayout = [[sg.Column(layout1)]]
    window = sg.Window("Character", mainLayout, resizable=True)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break


# Counts animes and episodes watched
def episodes_watched_total(myCursor):
    val1 = []
    myCursor.execute(
        "SELECT COUNT(title),SUM(episodes_watched) FROM grishin.anime_list;"
    )
    for i in myCursor:
        val1.append(list(i))
    headers = ["Animes Watched", "Episodes Watched Total"]
    sg.theme("DarkBlue3")
    layout1 = [
        [
            sg.Table(
                headings=headers,
                values=val1,
                display_row_numbers=False,
                enable_events=True,
                justification="c",
                key="-table-",
                font=("Arial", 14),
            )
        ],
    ]

    mainLayout = [[sg.Column(layout1)]]
    window = sg.Window("Character", mainLayout, resizable=True)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break


# Show manga with title as characters name
def character_name_as_title(myCursor):
    val1 = []
    myCursor.execute(
        "SELECT manga_list.title, manga_list.type ,manga_list.dates,characters.name,characters.gender,characters.hair FROM Grishin.characters,Grishin.manga_list WHERE characters.name = manga_list.title;"
    )
    for i in myCursor:
        val1.append(list(i))
    headers = ["Title", "Type", "Dates", "Name", "Gender", "Hair Color"]
    sg.theme("DarkBlue3")
    layout1 = [
        [
            sg.Table(
                headings=headers,
                values=val1,
                display_row_numbers=False,
                enable_events=True,
                justification="c",
                key="-table-",
                font=("Arial", 14),
            )
        ],
    ]

    mainLayout = [[sg.Column(layout1)]]
    window = sg.Window("Character As Title", mainLayout, resizable=True)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break


# Now thats a nice view
def ponetial_waifus_not_blonde(myCursor):
    val1 = []
    myCursor.execute("SELECT name, hair FROM Potential_Waifus WHERE NOT hair='Blonde';")
    for i in myCursor:
        val1.append(list(i))
    headers = ["Name", "Hair Color"]
    sg.theme("DarkBlue3")
    layout1 = [
        [
            sg.Table(
                headings=headers,
                values=val1,
                display_row_numbers=False,
                enable_events=True,
                justification="c",
                key="-table-",
                font=("Arial", 14),
            )
        ],
    ]

    mainLayout = [[sg.Column(layout1)]]
    window = sg.Window("Waifus", mainLayout, resizable=True)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break


# Shows all hair colour a character might have
def character_hair_color(myCursor):
    val1 = []
    myCursor.execute("SELECT hair FROM Grishin.characters GROUP BY hair;")
    for i in myCursor:
        val1.append(list(i))
    headers = ["Hair Color"]
    sg.theme("DarkBlue3")
    layout1 = [
        [
            sg.Table(
                headings=headers,
                values=val1,
                display_row_numbers=False,
                enable_events=True,
                justification="c",
                key="-table-",
                font=("Arial", 14),
            )
        ],
    ]

    mainLayout = [[sg.Column(layout1)]]
    window = sg.Window("Hair Colors Of Characters", mainLayout, resizable=True)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
