import json

titles_json = '''[{"id":"A33_a_crimson_sea","title":"The Crimson Sea"},{"id":"A33_a_matter_of_pride","title":"Matter of Pride"},{"id":"A33_a_most_prized_item","title":"The Prized Relic"},{"id":"A33_a_union_of_crowns","title":"Union of Crowns"},{"id":"A33_across_the_pond","title":"Across the Waters"},{"id":"A33_all_roads_lead_to_verne","title":"All Roads to Verne"},{"id":"A33_alvars_reforms","title":"Alvar's Reforms"},{"id":"A33_binding_the_beast","title":"Bind the Beast"},{"id":"A33_born_of_valour","title":"Born of Valour"},{"id":"A33_break_the_queen_of_the_hill","title":"Break the Hill Queen"},{"id":"A33_corins_devout_protectors","title":"Corin's Faithful Guard"},{"id":"A33_corins_shield","title":"Corin's Shield"},{"id":"A33_expand_the_vernissage","title":"Expand the Vernissage"},{"id":"A33_expand_the_wyvern_nests","title":"Expand the Nests"},{"id":"A33_in_search_of_adventure","title":"In Search of Adventure"},{"id":"A33_in_the_name_corin","title":"In Corin's Name"},{"id":"A33_laments_regatta","title":"Lament's Regatta"},{"id":"A33_new_verne","title":"New Verne"},{"id":"A33_old_friends_old_rivals","title":"Old Friends, Old Rivals"},{"id":"A33_on_wings_of_artificery","title":"Wings of Artificery"},{"id":"A33_project_holohana","title":"Project Holohana"},{"id":"A33_religious_mercantilism","title":"Sacred Mercantilism"},{"id":"A33_spread_the_word","title":"Spread the Word"},{"id":"A33_taking_to_the_seas","title":"Take to the Seas"},{"id":"A33_taming_the_lion","title":"Taming the Lion"},{"id":"A33_the_allure_of_the_luna","title":"Allure of the Luna"},{"id":"A33_the_grand_port_of_heartspier","title":"Grand Port of Heartspier"},{"id":"A33_the_grand_vernissage","title":"The Grand Vernissage"},{"id":"A33_the_halanni_exposition","title":"The Halanni Exposition"},{"id":"A33_the_heart_of_darkness","title":"Heart of Darkness"},{"id":"A33_the_holy_corinite_empire","title":"The Holy Corinite Empire"},{"id":"A33_the_kingdom_of_verne","title":"The Kingdom of Verne"},{"id":"A33_the_lands_of_adventure","title":"Lands of Adventure"},{"id":"A33_the_might_of_the_wyvern","title":"Might of the Wyvern"},{"id":"A33_the_quest_for_eggs","title":"Quest for Eggs"},{"id":"A33_the_riches_of_the_khenak","title":"Riches of Khenak"},{"id":"A33_the_rogue_duchy","title":"The Rogue Duchy"},{"id":"A33_the_sea_nest","title":"The Sea Nest"},{"id":"A33_the_verne_halann","title":"Verne of Halann"},{"id":"A33_the_vernissage","title":"The Vernissage"},{"id":"A33_the_vernman_era","title":"The Vernman Era"},{"id":"A33_the_vernman_renaissance","title":"The Vernman Renaissance"},{"id":"A33_the_wyvern_nest_initiative","title":"Wyvern Nest Initiative"},{"id":"A33_type_2_wyverns","title":"Type II Wyverns"},{"id":"A33_united_under_crimson_wings","title":"Under Crimson Wings"},{"id":"A33_valour_on_the_seas","title":"Valour on the Seas"},{"id":"A33_with_sword_and_shield","title":"Sword and Shield"},{"id":"A33_zenith_of_the_eastern_princes","title":"Zenith of Princes"}]'''

titles = json.loads(titles_json)

loc_path = r'C:\Users\User\Documents\GitHub\My-Anbennar\localisation\verne_overhaul_l_english.yml'
with open(loc_path, 'rb') as f:
    content = f.read().decode('utf-8-sig').replace('\r', '')

# Map: stub key -> real title
# Stub: 'a33_a_crimson_sea:' (no _title suffix) -> title
stub_to_title = {}
for item in titles:
    key = item['id'].lower()  # 'a33_a_crimson_sea'
    stub_to_title[key] = item['title']

lines = content.split('\n')
new_lines = []
replacements = 0

for line in lines:
    stripped = line.strip()
    matched = False
    for key, title in stub_to_title.items():
        # Stub format: 'a33_a_crimson_sea:0 "Stub Value"' or 'a33_a_crimson_sea: 0 "Stub Value"'
        # The stub line has format: ' a33_a_crimson_sea: 0 "A Crimson Sea"'
        # We need to match lines that START with the stub key (with or without _title suffix)
        if stripped.startswith(key + ':'):
            # Replace with correct format
            new_key = key + '_title'
            new_lines.append(' ' + new_key + ':0 "' + title + '"')
            replacements += 1
            matched = True
            break
        # Also handle existing correct format that needs updating
        if stripped.startswith(key + '_title:'):
            new_key = key + '_title'
            new_lines.append(' ' + new_key + ':0 "' + title + '"')
            replacements += 1
            matched = True
            break
    
    if not matched:
        new_lines.append(line)

print(f'Replacements: {replacements}')
with open(loc_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))
print('Done!')
