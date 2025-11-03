#!/usr/bin/env python3
import json

# Carregar dados
with open('database.json', 'r', encoding='utf-8') as f:
    emblems = json.load(f)

with open('sets_attack.json', 'r') as f:
    attack_sets = json.load(f)

with open('sets_sp_attack.json', 'r') as f:
    sp_attack_sets = json.load(f)

with open('sets_mixed.json', 'r') as f:
    mixed_sets = json.load(f)

emblem_dict = {e['name']: e for e in emblems}

color_map = {
    'White': 'Branco', 'Black': 'Preto', 'Red': 'Vermelho', 'Blue': 'Azul',
    'Purple': 'Roxo', 'Green': 'Verde', 'Brown': 'Marrom', 'Yellow': 'Amarelo',
    'Pink': 'Rosa', 'Gray': 'Cinza', 'Navy': 'Azul Marinho'
}

color_css = {
    'White': 'white', 'Black': 'black', 'Red': 'red', 'Blue': 'blue',
    'Purple': 'purple', 'Green': 'green', 'Brown': 'brown', 'Yellow': 'yellow',
    'Pink': 'pink', 'Gray': 'gray', 'Navy': 'navy'
}

bonus_descriptions = {
    'Branco': ['+1% HP', '+2% HP', '+4% HP'],
    'Preto': ['+1% CDR', '+2% CDR', '+4% CDR'],
    'Vermelho': ['+2% Vel. Ataque', '+4% Vel. Ataque', '+8% Vel. Ataque'],
    'Azul': ['+2% Defesa', '+4% Defesa', '+8% Defesa'],
    'Roxo': ['+2% Def. Especial', '+4% Def. Especial', '+8% Def. Especial'],
    'Verde': ['+1% Atq. Especial', '+2% Atq. Especial', '+4% Atq. Especial'],
    'Marrom': ['+1% Ataque', '+2% Ataque', '+4% Ataque'],
    'Amarelo': ['+4% Velocidade', '+6% Velocidade', '+12% Velocidade'],
    'Rosa': ['-4% Duração CC', '-8% Duração CC', '-16% Duração CC'],
    'Cinza': ['-3 Dano', '-6 Dano', '-12 Dano'],
    'Azul Marinho': ['+1% Carga Unite', '+2% Carga Unite', '+4% Carga Unite']
}

def calculate_set_info(emblem_names):
    color_counts = {}
    totals = {'hp': 0, 'attack': 0, 'sp_attack': 0, 'defense': 0, 'sp_defense': 0, 'speed': 0, 'crit': 0, 'cdr': 0}
    emblem_list = []

    for name in emblem_names:
        e = emblem_dict[name]
        emblem_list.append(e)
        color = e['color1']
        color_counts[color] = color_counts.get(color, 0) + 1

        stats = e.get('stats', [{}])[0]
        for key in totals:
            totals[key] += stats.get(key, 0)

    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
    bonuses = []

    for i, (color, count) in enumerate(sorted_colors[:2]):
        color_pt = color_map[color]
        thresholds = [2, 4, 6] if color in ['White', 'Blue', 'Purple', 'Green', 'Brown'] else [3, 5, 7]

        level = 0
        for idx, t in enumerate(thresholds):
            if count >= t:
                level = idx + 1

        bonuses.append((color, color_pt, level, count, thresholds))

    return emblem_list, totals, bonuses, color_counts

def get_stat_class(value):
    if value > 0:
        return 'positive'
    elif value < 0:
        return 'negative'
    else:
        return 'neutral'

def generate_build_html(set_title, set_desc, emblem_names):
    emblem_list, totals, bonuses, color_counts = calculate_set_info(emblem_names)

    html = f'    <div class="build-card">\n'
    html += f'        <div class="build-title">\n'
    html += f'            <h2>{set_title}</h2>\n'
    html += f'            <p>{set_desc}</p>\n'
    html += f'        </div>\n\n'
    html += f'        <div class="emblems-grid">\n'

    for e in emblem_list:
        color_css_class = color_css[e['color1']]
        img_url = f"https://d275t8dp8rxb42.cloudfront.net/emblems/pokedex/{e['name']}.png"
        html += f'            <div class="emblem">\n'
        html += f'                <img src="{img_url}" alt="{e["display_name"]}" title="{e["display_name"]}">\n'
        html += f'                <div class="emblem-color color-{color_css_class}"></div>\n'
        html += f'                <div class="emblem-name">{e["display_name"]}</div>\n'
        html += f'            </div>\n'

    html += '        </div>\n\n'
    html += '        <div class="counter">10/10</div>\n\n'
    html += '        <div class="stats-section">\n'
    html += '            <div class="stats-panel">\n'
    html += '                <h3>📊 Equipped Stats</h3>\n'

    stats_list = [
        ('HP', totals['hp'], False),
        ('Attack', totals['attack'], True),
        ('Defense', totals['defense'], False),
        ('Sp. Attack', totals['sp_attack'], True),
        ('Sp. Defense', totals['sp_defense'], False),
        ('Speed', totals['speed'], False),
        ('Crit Rate', totals['crit'], True),
        ('CDR', totals['cdr'], True)
    ]

    for label, value, is_float in stats_list:
        value_class = get_stat_class(value)
        if is_float:
            formatted_value = f"{value:+.1f}"
        else:
            formatted_value = f"{value:+.0f}"

        html += f'                <div class="stat-row">\n'
        html += f'                    <span class="stat-label">{label}</span>\n'
        html += f'                    <span class="stat-value {value_class}">{formatted_value}</span>\n'
        html += f'                </div>\n'

    html += '            </div>\n\n'
    html += '            <div class="stats-panel">\n'
    html += '                <h3>🎨 Equipped Sets</h3>\n'

    for color, color_pt, level, count, thresholds in bonuses:
        color_css_class = color_css[color]
        html += f'                <div class="color-set">\n'
        html += f'                    <div class="color-set-header">\n'
        html += f'                        <div class="color-icon color-{color_css_class}"></div>\n'
        html += f'                        <span class="color-name">{color_pt}</span>\n'
        html += f'                    </div>\n'
        html += f'                    <div class="color-levels">\n'
        html += f'                        <div class="level-badge active">{count}</div>\n'

        for idx, threshold in enumerate(thresholds):
            active = count >= threshold
            css_class = 'active' if active else 'inactive'
            html += f'                        <div class="level-badge {css_class}">{threshold}</div>\n'

        html += '                    </div>\n'

        if level > 0:
            bonus_text = bonus_descriptions[color_pt][level - 1]
            html += f'                    <div class="bonus-description">✅ Nível {level}: {bonus_text}</div>\n'
        else:
            html += f'                    <div class="bonus-description inactive">❌ Precisa de {thresholds[0]} para ativar</div>\n'

        html += '                </div>\n'

    html += '            </div>\n'
    html += '        </div>\n'
    html += '    </div>\n'

    return html

def generate_page(title, emoji, description, page_name, builds_list, active_tab):
    page = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Pokémon Unite</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>{emoji} {title}</h1>
            <p>{description}</p>
        </header>

        <nav class="nav-tabs">
            <a href="index.html"{' class="active"' if active_tab == "index" else ""}>Início</a>
            <a href="attack.html"{' class="active"' if active_tab == "attack" else ""}>Ataque Físico</a>
            <a href="sp-attack.html"{' class="active"' if active_tab == "sp-attack" else ""}>Ataque Especial</a>
            <a href="mixed.html"{' class="active"' if active_tab == "mixed" else ""}>Misto</a>
        </nav>

        <div class="build-grid">
'''

    for set_title, set_desc, emblem_names in builds_list:
        page += generate_build_html(set_title, set_desc, emblem_names)

    page += '''
        </div>
    </div>
</body>
</html>
'''

    with open(f'docs/{page_name}.html', 'w', encoding='utf-8') as f:
        f.write(page)

    print(f"✓ {page_name}.html gerado!")

# ==== Página de Ataque Físico ====
attack_builds = [
    ('💚 HP + Ataque', 'Balanceado para sustain e dano', attack_sets['set1_hp_attack']),
    ('⚔️ Ataque Máximo', 'Máximo dano físico possível', attack_sets['set2_max_attack']),
    ('💥 Crítico', 'Para Pokémon que escalam com crítico', attack_sets['set3_crit']),
    ('🛡️ Defesa Física', 'Build tanque com defesa física', attack_sets['set4_physical_defense']),
    ('🛡️ Defesa Especial', 'Build tanque contra dano mágico', attack_sets['set5_special_defense']),
    ('⚖️ Defesas Equilibradas', 'Balanceamento de ambas as defesas', attack_sets['set6_balanced_defense'])
]

generate_page('Builds de Ataque Físico', '🗡️', 'Para Pokémon que focam em dano físico', 'attack', attack_builds, 'attack')

# ==== Página de Ataque Especial ====
sp_attack_builds = [
    ('💚 HP + Ataque Especial', 'Balanceado para sustain e dano mágico', sp_attack_sets['set1_hp_sp_attack']),
    ('⚡ Ataque Especial Máximo', 'Máximo dano mágico possível', sp_attack_sets['set2_max_sp_attack']),
    ('⏱️ CDR (Cooldown)', 'Para usar habilidades com mais frequência', sp_attack_sets['set3_cdr']),
    ('🛡️ Defesa Física', 'Build tanque com defesa física', sp_attack_sets['set4_physical_defense']),
    ('🛡️ Defesa Especial', 'Build tanque contra dano mágico', sp_attack_sets['set5_special_defense']),
    ('⚖️ Defesas Equilibradas', 'Balanceamento de ambas as defesas', sp_attack_sets['set6_balanced_defense'])
]

generate_page('Builds de Ataque Especial', '✨', 'Para Pokémon que focam em dano mágico', 'sp-attack', sp_attack_builds, 'sp-attack')

# ==== Página Misto ====
mixed_builds = [
    ('💚 HP Equilibrado', 'Máximo HP mantendo ataques balanceados', mixed_sets['set1_hp_balanced']),
    ('💨 Velocidade de Movimento', 'Para rotação rápida no mapa', mixed_sets['set2_speed']),
    ('🛡️ Defesa Física', 'Build tanque com defesa física', mixed_sets['set3_physical_defense']),
    ('🛡️ Defesa Especial', 'Build tanque contra dano mágico', mixed_sets['set4_special_defense']),
    ('⚖️ Defesas Equilibradas', 'Balanceamento de ambas as defesas', mixed_sets['set5_balanced_defense'])
]

generate_page('Builds Misto (Equilibrado)', '⚖️', 'Para Pokémon que usam ambos os tipos de ataque', 'mixed', mixed_builds, 'mixed')

print("\n✅ Todas as páginas HTML foram geradas com sucesso!")
