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
WHERE name == input(hero_name)
```

I want something like facebook for the heros

Use index of the table instead of whole hero name
