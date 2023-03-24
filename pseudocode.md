# CRUD IMPLEMENTATIONS
## CREATE  
- have input for user to enter hero name 
- have input for user to enter abilities or link to existing one
- have input for about me 
- have input for bio

```
INSERT INTO heroes (name, about_me, biography)
VALUES (input(forname), input(forabout), input(bio));

IF ability input is new:
    INSERT INTO ability_type (nameOfAbility)
ELSE:
   SOMEHOW update abilities table with new hero_id and match ability_type_id 
```
## READ 
- have in depth hero analysis(friends, enemies(maybe add new table?), powers, bio, about me)

start with list of all heroes to select from
```
SELECT name from heroes;
THEN based on input (name of hero or index)
SELECT name, about_me, biography, ability_types.name, hero2_id, relationship_type FROM heroes
JOIN relationships
    ON hero1_id
JOIN abilities
    ON hero_id
JOIN ability_type 
    ON ability_type_id
```

## UPDATE
- update relationship between heroes
- update hero abilities?

```
UPDATE relationships
SET relationship_type = input(1friend or 2enemy)
where hero1_id == input(hero1)
AND hero2_id == input(hero2)
```

## DELETE
- update on death of a hero

```
DELETE FROM heroes
WHERE name=input(hero_name)
```

## INIT function
screen to be displayed on load of program and anytime another function or query is done loading. That way, user won't have keep running the python program.

```
def init():
    PRINT (homescreen)
    DISPLAY (Options relating to CRUD)
    INPUT (what would user like to do?)
```

OPTIONS can be:
 - View current directory of heroes
    - choose a hero for a deeper dive into their info/powers/relations
 - Someone joins the good fight(add hero)
 - Tragedy Strikes(remove hero)
 - New mutation(update hero relation/or powers)
 