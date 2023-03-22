from database.db_connection import execute_query, create_connection

width = 30
page = ""

def hero_directory(state):
    x = "SELECT * FROM heroes"
    results = execute_query(x).fetchall()
   
    print("HERO DIRECTORY".center(width, "~") if state == 1 else "Update Mode".center(width, "~"))
    
    for thing in results:
        print(thing[1].center(width))
    
    go = input("Who to deep dive into the history of?\n".center(width) if state == 1 else "Who to update?".center(width))
    
    if go == "":
        menu()
    else:
        analyze(go) if state == 1 else Update(go)


def add_hero():
    name = input("Name of Hero?".center(width))
    about = input("Hero's Slogan/Catchphrase?".center(width))
    bio = input("How did the hero get their powers?".center(width))

    q = """
    INSERT INTO heroes (name, about_me, biography)
    VALUES ('{}', '{}', '{}')
    """.format(name, about, bio)
    execute_query(q)

    power = input("What powers do they have?".center(width))
    powerSplit = power.split(", ")
    powerQuery = """
    SELECT name  
    FROM ability_types
    """
    pwers = []
    existingPowers = execute_query(powerQuery).fetchall()
    for tuple in existingPowers:
        for power in tuple:
            pwers.append(power)

    for x in powerSplit:
        if x in pwers:
            continue
        else:
            qp = """
            INSERT INTO ability_types (name)
            VALUES ('{}')
            """.format(x)
            execute_query(qp)

        qabil = """
        INSERT INTO abilities (hero_id, ability_type_id)
        VALUES((SELECT id 
        FROM heroes
        WHERE name='{}'), (SELECT id 
        FROM ability_types
        WHERE name='{}'))
        """.format(name, x)
        execute_query(qabil)

 
    print(f"{name} joins the battle!".center(width))
    menu()


def analyze(name):
    qint = """
    SELECT id 
    FROM heroes
    WHERE name='{}'
    """.format(name)
    id = execute_query(qint).fetchone()[0]

    q0 = """
    SELECT DISTINCT about_me, biography
    FROM heroes
    WHERE name='{}'
    """.format(name)

    result0 = execute_query(q0).fetchall()
    for result in result0:
        for thing in result:
            print(thing)

    q = """
    SELECT DISTINCT ability_types.name AS ability_name
    FROM heroes
    LEFT JOIN abilities
        ON heroes.id=abilities.hero_id
    LEFT JOIN ability_types
        ON abilities.ability_type_id=ability_types.id
    WHERE heroes.name='{}'
    """.format(name)
    
    print("Abilities:", end =" ")
    results = execute_query(q).fetchall()
    for result in results:
        for thing in result:
            print(thing, end=", ")
    print('')

    qf1 = """
    SELECT heroes.name AS hero_name, relationship_types.name AS relationship_type
    FROM relationships
    JOIN heroes
        ON heroes.id=relationships.hero1_id 
    JOIN relationship_types
        ON relationships.relationship_type_id=relationship_types.id
    where hero2_id={}
    """.format(id)

    friends = []
    enemies = []

    relayq1 = execute_query(qf1).fetchall()
    for x in relayq1:
        if x[1] == "Friend" and x[0] not in friends:
            friends.append(x[0])
        elif x[1] == "Enemy" and x[0] not in enemies:
            enemies.append(x[0])
    
    qf2 = """
    SELECT heroes.name AS hero_name, relationship_types.name AS relationship_type
    FROM relationships
    JOIN heroes
        ON heroes.id=relationships.hero2_id 
    JOIN relationship_types
        ON relationships.relationship_type_id=relationship_types.id
    where hero1_id={}
    """.format(id)

    relayq2 = execute_query(qf2).fetchall()
    for x in relayq2:
        if x[1] == "Friend" and x[0] not in friends:
            friends.append(x[0])
        elif x[1] == "Enemy" and x[0] not in enemies:
            enemies.append(x[0])

    print("Friends: ", end="")
    for friend in friends:
        print(friend, end=", ")
    print("")

    print("Foes: ", end="")
    for foe in enemies:
        print(foe, end=", ")
    print("")

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
    menu()

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
            hero_directory(1)
        case '2':
            add_hero()
        case '3':
            kill_hero()
        case '4':
            hero_directory(2)

def Update(person):
    print("-".center(width,"-"))
    print("1.Name".center(width))
    print("2.About".center(width))
    print("3.Biography".center(width))
    print("4.Abilities".center(width))
    print("5.Relationships".center(width))
    x = input(f"What to change about {person}?".center(width))
    match x: 
        case '1':
            name = input(f"New name for {person}?".center(width))
            nameQuery = """
            UPDATE heroes
            SET name ='{}'
            WHERE name='{}'
            """.format(name, person)
            execute_query(nameQuery)
            print("{} has changed identities to {}".format(person, name))
            menu()
        case '2':
            print("Current 'about me' section for {}:".format(person).center(width))
            beforeAbout = """
            SELECT about_me
            FROM heroes
            WHERE name='{}'
            """.format(person)
            before = execute_query(beforeAbout).fetchall()
            print(before)

            about = input(f"New 'about me' section for {person}?")
            aboutQuery = """
            UPDATE heroes
            SET about_me ='{}'
            WHERE name='{}'
            """.format(about, person)
            execute_query(aboutQuery)
            menu()
        case '3':
            print("Current 'biography' section for {}:".format(person).center(width))
            beforeBio = """
            SELECT biography
            FROM heroes
            WHERE name='{}'
            """.format(person)
            before = execute_query(beforeAbout).fetchall()
            print(before)

            bio = input(f"New 'biography' section for {person}?")
            bioQuery = """
            UPDATE heroes
            SET biography ='{}'
            WHERE name='{}'
            """.format(bio, person)
            execute_query(bioQuery)
            menu()
        case '4':
            print("Current abilities of {}:".format(person).center(width))
            beforeAbilities = """
            SELECT ability_types.name
            FROM abilities
            JOIN ability_types 
                ON abilities.ability_type_id=ability_types.id
            WHERE hero_id=(SELECT id
            FROM heroes
            WHERE name='{}')
            """.format(person)
            before = execute_query(beforeAbilities).fetchall()
            for tuple in before:
                for str in tuple:
                    print(str)
            
        # case '5':
    
menu()