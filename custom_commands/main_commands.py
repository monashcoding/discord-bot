from custom_commands.unit_checks import *
from custom_commands.unit_embed import *


def str_prereqs_to(unit_code, handbook) -> str:
    prereqs_list = prereqs_to(unit_code, handbook)
    output = ""
    for unit in prereqs_list:
        output += f'{unit}\n'
    return output

def units_can_complete(unit_list: list,handbook: dict) -> list:
    output = []
    credit_attained = sum([int(unit['credit_points']) for unit in unit_list])
    for unit in handbook:
        # Skip if unit is already completed.
        if unit in unit_list:
            continue
        unit_check = unit_prereq_checker(unit_list, unit, handbook)
        prohibition_check = unit_prohibition_check(unit_list, unit, handbook)
        credit_check = credit_attained >= unit['requisites']['cp_required']
        if (unit_check[0] and credit_check and prohibition_check):
            if (unit_check[1] > 0):
                output.append(unit) 
    return output
