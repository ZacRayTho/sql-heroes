from database.db_connection import execute_query


def frenemy(name):
    qint = """
    SELECT id 
    FROM heroes
    WHERE name=%s
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
        ON heroes.id=relationships.hero1_id 
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


friends,enemies = frenemy('The Seer')
print(friends)
print(enemies)
# execute_query(q)