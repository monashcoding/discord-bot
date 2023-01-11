import json

with open('JSON\handbook_data_complete.json', 'r') as f:
    handbook: dict = json.load(f)

def func(unit_code):
    unit_dict = handbook[unit_code]
    unit_prereqs = unit_dict['requisites']['prerequisites']
    output_str = ""
    for unit in unit_prereqs:
        temp_lst = [f"\n{unit['NumReq']} of"]
        temp_lst.append("\n".join([unit_or for unit_or in unit['units']]))
        output_str += "\n".join(temp_lst)
    return output_str



print(func('FIT2014'))
print()