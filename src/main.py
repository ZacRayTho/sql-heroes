from database.db_connection import execute_query, create_connection

def hero_directory():
    x = "SELECT * FROM heroes"
    results = execute_query(x).fetchall()
    print("HERO DIRECTORY".center(30, "~"))
    for thing in results:
        print(thing[1].center(30))


def add_hero():
    name = input("Name of Hero? ")
    about = input("Hero's Slogan/Catchphrase? ")
    bio = input("How did the hero get their powers? ")
    q = """
        INSERT INTO heroes (name, about_me, biography)
        VALUES ('{}', '{}', '{}')
    """.format(name, about, bio)
    print(f"{name} joins the battle!")

def analyze():
    name = input("Who do you want a deep search on? ")
    q = """
    SELECT DISTINCT heroes.name, about_me, biography, ability_types.name
    FROM heroes
    LEFT JOIN abilities
        ON heroes.id=abilities.hero_id
    LEFT JOIN ability_types
        ON abilities.ability_type_id=ability_types.id
    WHERE heroes.name='{}'
    """.format(name)
    results = execute_query(q).fetchall()
    for result in results:
        for x in result:
            print(x)


def kill_hero():
    target = input("Name of unfortunate soul? ")
    q = """
        DELETE FROM heroes
        WHERE name='{}'  
    """.format(target)
    execute_query(q)
    print(f"{target} stepped on a lego, ending their heroic life, they will be missed.")

def menu():
    print("HOME PAGE".center(30, "*"))
    print("Choose an option".center(30))
    print("1.View Hero Directory".center(30))
    print("2.New Hero Form".center(30))
    print("3.Recently Deceased Form".center(30))
    print("4.Hero Update Form".center(30))
    x = input("Where would you like to go? ")
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