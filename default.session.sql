SELECT DISTINCT heroes.name, about_me, biography, ability_types.name
FROM heroes
LEFT JOIN abilities
    ON heroes.id=abilities.hero_id
LEFT JOIN ability_types
    ON abilities.ability_type_id=ability_types.id
WHERE heroes.name='The Seer'

