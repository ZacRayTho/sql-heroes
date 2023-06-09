from database.db_connection import execute_query, create_connection

width = 30

### MENU OF HERO NAMES

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
        try:
            analyze(go) if state == 1 else Update(go)
        except:
            print("Hero doesn't exist")
            menu()


### ADD HERO FUNCTION

def add_hero():
    name = input("Name of Hero?".center(width))
    about = input("Hero's Slogan/Catchphrase?".center(width))
    bio = input("How did the hero get their powers?".center(width))

    q = """
    INSERT INTO heroes (name, about_me, biography)
    VALUES (%s, %s, %s)
    """
    execute_query(q, (name, about, bio, ))

    power = input("What powers do they have?(format like 'Telepathy, Invisibility, blahblah')".center(width))
    add_power(power, name)
 
    print(f"{name} joins the battle!".center(width))
    menu()


### DEEP DIVE INTO HERO'S EVERYTHING
def analyze(name):
    lazyName = like(name)
    qint = """
    SELECT id 
    FROM heroes
    WHERE lower(name) LIKE %s
    """
    id = execute_query(qint, (lazyName, )).fetchone()[0]
    
    q0 = """
    SELECT DISTINCT about_me, biography
    FROM heroes
    WHERE lower(name) LIKE %s
    """

    result0 = execute_query(q0, (lazyName, )).fetchall()
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
    WHERE lower(heroes.name) LIKE %s
    """
    
    print("Abilities:", end =" ")
    results = execute_query(q, (lazyName, )).fetchall()
    for result in results:
        for thing in result:
            print(thing, end=", ")
    print('')

    friends, enemies = frenemy(lazyName)
    
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


### NIGHT NIGHT HERO

def kill_hero():
    target = input("Name of unfortunate soul?".center(width))
    q = """
        DELETE FROM heroes
        WHERE lower(name) LIKE %s  
    """
    execute_query(q, (like(target), ))
    print(f"{target} stepped on a lego, ending their heroic life, they will be missed.".center(width))
    menu()



### MAIN MENU 

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



### UPDATE ANYHERO'S ANYTHING
def Update(person):
    lazyName = like(person)
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
            SET name =%s
            WHERE lower(name) LIKE %s
            """
            execute_query(nameQuery, (name, lazyName, ))
            print("{} has changed identities to {}".format(person, name))
            menu()
        case '2':
            print("Current 'about me' section for {}:".format(person).center(width))
            beforeAbout = """
            SELECT about_me
            FROM heroes
            WHERE lower(name) LIKE %s
            """
            before = execute_query(beforeAbout, (lazyName, )).fetchall()
            print(before[0][0])

            about = input(f"New 'about me' section for {person}?")
            aboutQuery = """
            UPDATE heroes
            SET about_me =%s
            WHERE lower(name) LIKE %s
            """
            execute_query(aboutQuery, (about, lazyName, ))
            menu()
        case '3':
            print("Current 'biography' section for {}:".format(person).center(width))
            beforeBio = """
            SELECT biography
            FROM heroes
            WHERE lower(name) LIKE %s
            """
            before = execute_query(beforeBio, (lazyName, )).fetchall()
            print(before[0][0])

            bio = input(f"New 'biography' section for {person}?")
            bioQuery = """
            UPDATE heroes
            SET biography =%s
            WHERE lower(name) LIKE %s
            """
            execute_query(bioQuery, (bio, lazyName, ))
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
            WHERE lower(name) LIKE %s)
            """
            before = execute_query(beforeAbilities, (lazyName, )).fetchall()
            for tuple in before:
                print(tuple[0])
            
            edit = input("Remove(R), or Add(A)?".center(width))
            if edit.upper() == "R":
                edit2 = input("Which Ability?".center(width))
                lazyPower = like(edit2)
                removeQuery = """
                DELETE FROM abilities
                WHERE hero_id=(SELECT id from heroes WHERE lower(name) LIKE %s)
                AND ability_type_id=(SELECT id from ability_types WHERE lower(name) LIKE %s)
                """
                execute_query(removeQuery, (lazyName, lazyPower, ))
                print(f"{person} has mysteriously lost his power of {edit2}".center(width))
                menu()
            elif edit.upper() == "A":
                edit2 = input(f"What abilities does {person} gain?(format like 'Telepathy, Invisibility, blahblah')".center(width))
                add_power(edit2, person)
                print(f"{person} has gained the power(s) of {edit2}".center(width))
                menu()

        case '5': 
            print(f"Current relationships of {person}")
            friends, enemies = frenemy(person)

            print("Friends: ", end="")
            for friend in friends:
                print(friend, end=", ")
            print("")
                
            print("Enemies: ", end="")
            for enemy in enemies:
                print(enemy, end=", ")
            print("")

            choice = input("Flip Relationship(F) OR Add another(A)?")
            if choice.upper() == "F":
                flipper = input(f"Who betrays/befriends {person}? ".center(width))
                lazyFlip = like(flipper)
                firstId = execute_query('SELECT id from heroes WHERE lower(name) LIKE %s', (lazyName, )).fetchone()
                secondId = execute_query('SELECT id FROM heroes WHERE lower(name) LIKE %s', (lazyFlip, )).fetchone()
                flipQuery = """
                UPDATE relationships
                SET relationship_type_id = (CASE WHEN relationship_type_id=1 THEN 2 ELSE 1 END)
                WHERE (hero1_id=%s OR hero2_id=%s)
                AND (hero1_id=%s OR hero2_id=%s)
                """
                execute_query(flipQuery, (firstId[0], firstId[0], secondId[0], secondId[0], ))
                print(f"{flipper} had second thoughts about {person}")
                menu()
            elif choice.upper() == "A":
                newb = input(f" Who's {person} thinking of?")
                newb2 = like(newb)
                relationship = input("Friend(F) or Enemy(E)?")
                shortrelay = "friend" if relationship.upper() == "F" else "enemy"
                newFrenemy = """
                INSERT INTO relationships (hero1_id, hero2_id, relationship_type_id)
                VALUES ((SELECT id FROM heroes WHERE lower(name) LIKE %s),
                (SELECT id FROM heroes WHERE lower(name) LIKE %s), %s)
                """
                execute_query(newFrenemy, (lazyName, newb2, 1 if relationship.upper() == "F" else 2))
                print(f"{person} has made a new {shortrelay}, named {newb}!")
                menu()
                

### FUNCTION FOR ADD ABILITY AND CHECK IF IT ALREADY EXISTS
def add_power(str, name):
    print(str, name)
    arr = str.split(", ")
    powerQuery = """
    SELECT name  
    FROM ability_types
    """
    pwers = []
    existingPowers = execute_query(powerQuery).fetchall()
    for tuple in existingPowers:
        for power in tuple:
            pwers.append(power)

    for x in arr:
        print(x)
        if x in pwers:
            pass
        else:
            qp = """
            INSERT INTO ability_types (name)
            VALUES (%s)
            """
            execute_query(qp, (x, ))

        qabil = """
        INSERT INTO abilities (hero_id, ability_type_id)
        VALUES((SELECT id 
        FROM heroes
        WHERE lower(name) LIKE %s), (SELECT id 
        FROM ability_types
        WHERE name=%s))
        """
        execute_query(qabil, (like(name), x, ))


### GET LIST OF FRIENDS AND ENEMIES FOR CURRENT HERO

def frenemy(name):
    qint = """
    SELECT id 
    FROM heroes
    WHERE lower(name) LIKE %s
    """
    id = execute_query(qint, (name, )).fetchone()[0]

    friends = []
    enemies = []
    
    q1 = """
    SELECT heroes.name AS hero_name, relationship_types.name AS relationship_type
    FROM relationships
    JOIN heroes
        ON heroes.id=relationships.hero1_id 
    JOIN relationship_types
        ON relationships.relationship_type_id=relationship_types.id
    where hero2_id=%s
    """
    q2 = """
    SELECT heroes.name AS hero_name, relationship_types.name AS relationship_type
    FROM relationships
    JOIN heroes
        ON heroes.id=relationships.hero2_id 
    JOIN relationship_types
        ON relationships.relationship_type_id=relationship_types.id
    where hero1_id=%s
    """
    
    for x in [q1, q2]:
        results = execute_query(x, (id, )).fetchall()
        for y in results:
            if y[1] == "Friend" and y[0] not in friends:
                friends.append(y[0])
            elif y[1] == "Enemy" and y[0] not in enemies:
                enemies.append(y[0])
    return [friends, enemies]


### FUNCTION USED TO ADD % FOR SQL LIKE FUNCTIONS
def like(str):
    return "%" + str + "%"

### START PROGRAM1
menu()