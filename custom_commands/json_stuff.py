import json

"""
/help commands.
"""
search = "Retrieves unit information on the unit based off the unit code, e.g /search 'MTH2225' returns unit information on unit with code 'MTH2225' "
search_prereqs_to = "Retrieves a list of units that the input unit is a prereq towards. e.g /search_prereqs_to 'FIT1045' returns a list of units that requires FIT1045 as a prerequisite."
units_can_take = "Inputs a list of units separated by commas, and returns a list of units that you can now take. However, it does not list every single unit possible,\nonly those with at least one unit in the list of units provided in the input. e.g /units_can_take 'FIT1045, MTH1030' returns all units that have at least FIT1045 or MTH1030 as a requirement, or both."
search_name = "A fuzzy search that returns a list of top results, e.g /search_name 'english' will return a list of units with keyword 'english' in the name" 
help_dict = dict()

lst_1 = ['search', 'search_prereqs_to', 'units_can_take', 'search_name']
lst_2 = [search, search_prereqs_to, units_can_take, search_name]
for index, key in enumerate(lst_1):
    help_dict[key] = lst_2[index]

with open('help.json', 'w') as fn:
    json.dump(help_dict, fn)
print()