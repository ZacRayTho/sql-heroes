from database.db_connection import execute_query, create_connection

def test():
    x = "SELECT * FROM heroes"
    results = execute_query(x).fetchall()
    for thing in results:
        print(thing[1])


def add_hero():
    name = input("Name of Hero? ")
    about = input("Hero's Slogan/Catchphrase? ")
    bio = input("How did the hero get their powers? ")
    q = """
        INSERT INTO heroes (name, about_me, biography)
        VALUES ('{}', '{}', '{}')
    """.format(name, about, bio)

def analyze():
    name = input("Who do you want a deep search on? ")
    q = 


def kill_hero():
    target = input("Name of unfortunate soul? ")
    q = """
        DELETE FROM heroes
        WHERE name='{}'  
    """.format(target)
    execute_query(q)
    print(f"{target} stepped on a lego, ending their heroic life, they will be missed.")

