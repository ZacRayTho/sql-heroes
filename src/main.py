from database.db_connection import execute_query, create_connection

width = 30

def hero_directory():
    x = "SELECT * FROM heroes"
    results = execute_query(x).fetchall()
    print("HERO DIRECTORY".center(width, "~"))
    for thing in results:
        print(thing[1].center(width))
    go = input("Who to deep dive into the history of?\n".center(width))
    if go == "":
        menu()
    else:
        analyze(go)


def add_hero():
    name = input("Name of Hero?".center(width))
    about = input("Hero's Slogan/Catchphrase?".center(width))
    bio = input("How did the hero get their powers?".center(width))
    q = """
        INSERT INTO heroes (name, about_me, biography)
        VALUES ('{}', '{}', '{}')
    """.format(name, about, bio)
    print(f"{name} joins the battle!".center(width))


def analyze(name):
    q0 = """
    SELECT DISTINCT about_me, biography
    FROM heroes
    WHERE name='{}'
    """.format(name)

    q = """
    SELECT DISTINCT ability_types.name AS ability_name
    FROM heroes
    LEFT JOIN abilities
        ON heroes.id=abilities.hero_id
    LEFT JOIN ability_types
        ON abilities.ability_type_id=ability_types.id
    WHERE heroes.name='{}'
    """.format(name)
    
    result0 = execute_query(q0).fetchall()
    for result in result0:
        for thing in result:
            print(thing)

    print("Abilities:", end =" ")
    results = execute_query(q).fetchall()
    for result in results:
        for thing in result:
            print(thing, end=", ")
    print('')
    input("Press enter to return to main menu")
    menu()


def kill_hero():
    target = input("Name of unfortunate soul?".center(width))
    q = """
        DELETE FROM heroes
        WHERE name='{}'  
    """.format(target)
    execute_query(q)
    print(f"{target} stepped on a lego, ending their heroic life, they will be missed.".center(width))

def menu():
    print("HOME PAGE".center(width, "*"))
    print("Choose an option".center(width))
    print("1.View Hero Directory".center(width))
    print("2.New Hero Form".center(width))
    print("3.Recently Deceased Form".center(width))
    print("4.Hero Update Form".center(width))
    x = input("Where would you like to go?\n".center(width))
    match x:
        case '1':
            hero_directory()
        case '2':
            add_hero()
        case '3':
            kill_hero()
        case '4':
            print("Will be implemented soon")

menu()