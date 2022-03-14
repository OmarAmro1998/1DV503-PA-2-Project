import PySimpleGUI as sg
from queries import start
from queries import (
    show_users,
    add_user,
    show_anime,
    choise_menu_anime_type,
    favorite_characters,
    anime_with_manga,
    episodes_total,
    character_as_manganame,
    ponetial_waifus_not_blonde,
    hair_colors_of_characters,
)

# Main Menu
def mainwindow():
    sg.theme("BluePurple")
    # Create Themes
    layout = [
        [
            sg.Button("Insert Data", font=("Helvetica", 14, "bold"), expand_x=True)
        ],  # Load data to database
        [
            sg.Button("Show Profile Info", font="Helvetica", expand_x=True)
        ],  # Two tables shows all users and a waifu
        [
            sg.Button("Show Completed/Planned", font="Helvetica", expand_x=True)
        ],  # One table just shows Completed/Planned
        # [sg.Button("Show Favorite Characters")],
        [
            sg.Button("Show Planned Anime With Manga", font="Helvetica", expand_x=True)
        ],  # Two tables uses GROUP BY and ORDER BY
        [
            sg.Button(
                "Show How Many Animes And Episodes Watched",
                font="Helvetica",
                expand_x=True,
            )
        ],
        [
            sg.Button(
                "Show Manga Where Title is a Characters Name",
                font="Helvetica",
                expand_x=True,
            )
        ],  # Two Tables
        [
            sg.Button(
                "Show Potential Waifus Of My Type (not blonde)",
                font="Helvetica",
                expand_x=True,
            )
        ],  # View
        [
            sg.Button(
                "Show What Hair Color A Character Might Have",
                font="Helvetica",
                expand_x=True,
            )
        ],
        # [sg.Button("Add User", font="Helvetica", expand_x=True)],  removed
        [sg.Button("Quit", font="Helvetica", expand_x=True)],  # Quit not delete
        [sg.Button("Remove Database And Exit", font="Helvetica", expand_x=True)],
        [sg.Stretch()],
        [  # Quit and delete (why not)
            sg.Image(filename="img/catsmol.png")
        ],  # Important file
    ]
    window = sg.Window(
        "Data Selection Menu",
        layout,
        element_justification="l",
        no_titlebar=False,
        finalize=True,
        resizable=False,
        element_padding=(0, 0),
        # Dock icon in base64
        icon=b"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",
    )
    # Loop so program waits for users actions
    while True:
        # From here all the queries are executed
        event, values = window.read()
        if event == "Show Profile Info":
            show_users()
        if event == "Insert Data":
            start()
        if event == "Add User":
            add_user()
        if event == "Show All Added Anime":
            show_anime()
        if event == "Show Completed/Planned":
            choise_menu_anime_type()
        if event == "Show Planned Anime With Manga":
            anime_with_manga()
        if event == "Show How Many Animes And Episodes Watched":
            episodes_total()
        if event == "Show Manga Where Title is a Characters Name":
            character_as_manganame()
        if event == "Show Potential Waifus Of My Type (not blonde)":
            ponetial_waifus_not_blonde()
        if event == "Show What Hair Color A Character Might Have":
            hair_colors_of_characters()
        if event == "Show Favorite Characters":
            favorite_characters()
            # Drop Database
        if event == "Remove Database And Exit":
            from queries import end

            end()
            break
        if event == sg.WIN_CLOSED:
            break
        # Quit but database stays
        if event == "Quit":
            break


# Starts here
mainwindow()
