from custom_commands.unit_checks import *
from custom_commands.unit_search import *
from custom_commands.unit_embed import *

def search_by_unit_code(unit_code: str, handbook):
    """
    Returns unit (dictionary)

    """
    # Basic information about the unit
    try:
        unit_dict = handbook[unit_code]
    except KeyError:
        return {}
    return unit_dict

def str_prereqs_to(unit_code, handbook) -> str:
    if not (valid_code_check(unit_code, handbook)):
        return False

    prereqs_list = prereqs_to(unit_code, handbook)
    output = ""
    for unit in prereqs_list:
        output += f'{unit}\n'
    return output

def units_can_complete(unit_list: list,handbook: dict) -> list:
    for unit in unit_list:
        if (not valid_code_check(unit, handbook)):
            return []

    output = []
    for unit in handbook:
        # Skip if unit is already completed.
        print()
        if unit in unit_list:
            continue
        unit_check = unit_prereq_checker(unit_list, unit, handbook)
        credit_check = unit_credit_prereq_check(unit_list, unit, handbook)
        prohibition_check = unit_prohibition_check(unit_list, unit, handbook)
        if (unit_check[0] and credit_check and prohibition_check):
            if (unit_check[1] > 0):
                output.append(unit) 

    print()
    return output
