from custom_commands.unit_checks import *
from custom_commands.unit_embed import *


def str_prereqs_to(unit_code, handbook) -> str:
    """
    Turns prerequisites to newline separated lines.
    """
    return "\n".join(prereqs_to(unit_code, handbook))

def units_can_take(unit_list: list,handbook: dict) -> list:
    """
    Determines the units you can take, for a list of units you have done.
    """
    output = []
    credit_attained = sum([int(handbook[unit]['credit_points']) for unit in unit_list])
    for unit in handbook:
        # Skip if unit is already completed.
        if unit in unit_list:
            continue
        unit_check = unit_prereq_checker(unit_list, unit, handbook)
        prohibition_check = unit_prohibition_check(unit_list, unit, handbook)
        credit_check = credit_attained >= handbook[unit]['requisites']['cp_required']
        if (unit_check[0] and credit_check and prohibition_check):
            if (unit_check[1] > 0):
                output.append(unit) 
    return output
