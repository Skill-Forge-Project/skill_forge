import json

user_xp = 543

with open('levels.json', 'r') as levels_file:
    leveling_data = json.load(levels_file)

    for level in leveling_data:
        for level_name, level_stats in level.items():
            if level_stats['min_xp'] <= user_xp <= level_stats['max_xp']:
                print(f'User is at level {level_name}. Level: {level_stats["level"]}')
                break