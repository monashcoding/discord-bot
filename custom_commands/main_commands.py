from custom_commands.unit_checks import *
from custom_commands.unit_embed import *
import re
def str_prereqs_to(unit_code, handbook, filter_arg) -> str:
    """
    Turns prerequisites to newline separated lines.
    """
    return "\n".join(prereqs_to(unit_code, handbook, filter_arg))


def substring_matching(string_1, string_2):
    n, m = len(string_1), len(string_2)
    i, j = 0, 0
    for i in range(m - n + 1):
        j = 0
        while (j < n and string_2[i + j] == string_1[j]):
            j += 1
            if (j == n):
                return i
    return -1


def units_can_take(unit_list: list, handbook: dict, filter = False) -> list:
    """
    Determines the units you can take, for a list of units you have done.
    """
    output = []
    credit_attained = sum([int(handbook[unit]['credit_points'])
                          for unit in unit_list])
    for unit in handbook:
        # Skip if unit is already completed.
        if unit in unit_list:
            continue
        unit_check = unit_prereq_checker(unit_list, unit, handbook)
        prohibition_check = unit_prohibition_check(unit_list, unit, handbook)
        credit_check = credit_attained >= handbook[unit]['requisites']['cp_required']
        filter_val = filter_check(unit, filter)
        if (unit_check[0] and credit_check and prohibition_check and filter_val):
            if (unit_check[1] > 0):
                output.append(unit)
    return output


def search_by_name(unit_request, handbook: dict):
    modified_req = re.sub('[^A-Za-z0-9]+', '', unit_request).lower()
    lst_potential_units = []
    for unit in handbook:
        name = handbook[unit]['unit_name']
        modified_name = re.sub('[^A-Za-z0-9]+', '', name)
        modified_name = modified_name.lower()
        pos = substring_matching(modified_req, modified_name)
        if (pos == -1):
            continue
        pos_rank = pos
        length_rank = len(modified_name) - len(modified_req)
        lst_potential_units.append((unit, pos_rank, length_rank))

    lst_potential_units.sort(key=lambda x: x[2])
    lst_potential_units.sort(key=lambda x: x[1])
    return lst_potential_units


