


SELECT ability_types.name
FROM abilities
JOIN ability_types 
    ON abilities.ability_type_id=ability_types.id
WHERE hero_id=(SELECT id
FROM heroes
WHERE name='The Seer')





