from custom_commands.unit_checks import *
from custom_commands.unit_embed import *
import re


def str_prereqs_to(unit_code, handbook, filter_arg) -> str:
    """
    Converts prerequisites to newline-separated lines.

    Args:
        unit_code (str): The unit code to retrieve prerequisites for.
        handbook (dict): The handbook data dictionary containing unit information.
        filter_arg: Filter argument to apply to the prerequisites.

    Returns:
        str: Newline-separated string containing the prerequisites for the unit.
    """
    return "\n".join(prereqs_to(unit_code, handbook, filter_arg))


def substring_matching(string_1: str, string_2: str):
    """
    Performs substring matching to find the position of string_1 in string_2.

    Args:
        string_1 (str): The substring to search for.
        string_2 (str): The string to search in.

    Returns:
        int: The starting position of string_1 in string_2, or -1 if not found.
    """
    n, m = len(string_1), len(string_2)
    i, j = 0, 0
    for i in range(m - n + 1):
        j = 0
        while j < n and string_2[i + j] == string_1[j]:
            j += 1
            if j == n:
                return i
    return -1


def limit_field_pointers(input, char_limit) -> list:
    """
    Limits the field pointers within the given character limit.

    Args:
        input (str): The input string.
        char_limit (int): The maximum character limit for each field.

    Returns:
        list: List of tuples representing the start and end pointers for each field.
    """
    i, j = 0, char_limit
    lst_pointers = []
    while i < len(input) - char_limit:
        while input[j] != f"\n":
            j -= 1
        lst_pointers.append((i, j))
        i = j + 1
        j = i + char_limit
    lst_pointers.append((i, len(input) - 1))
    return lst_pointers


def units_can_take(unit_list: list, handbook: dict, filter=None) -> list:
    """
    Determines the units that can be taken based on the list of units already completed.

    Args:
        unit_list (list): List of unit codes that have been completed.
        handbook (dict): The handbook data dictionary containing unit information.
        filter: Filter argument to apply while determining units (default: False).

    Returns:
        list: List of unit codes that can be taken.
    """
    output = []
    credit_attained = sum([int(handbook[unit]["credit_points"]) for unit in unit_list])
    for unit in handbook:
        # Skip if unit is already completed.
        if unit in unit_list:
            continue
        unit_check = unit_prereq_checker(unit_list, unit, handbook)
        prohibition_check = unit_prohibition_check(unit_list, unit, handbook)
        credit_check = credit_attained >= handbook[unit]["requisites"]["cp_required"]
        filter_val = filter_check(unit, filter)
        if unit_check[0] and credit_check and prohibition_check and filter_val:
            if unit_check[1] > 0:
                output.append(unit)
    return output


def search_by_name(unit_request, handbook: dict):
    """
    Searches for units by name using substring matching.

    Args:
        unit_request (str): The unit name to search for.
        handbook (dict): The handbook data dictionary containing unit information.

    Returns:
        list: List of potential units matching the search criteria, sorted by relevance.
    """
    modified_req = re.sub("[^A-Za-z0-9]+", "", unit_request).lower()
    lst_potential_units = []
    for unit in handbook:
        name = handbook[unit]["unit_name"]
        modified_name = re.sub("[^A-Za-z0-9]+", "", name)
        modified_name = modified_name.lower()
        pos = substring_matching(modified_req, modified_name)
        if pos == -1:
            continue
        pos_rank = pos
        length_rank = len(modified_name) - len(modified_req)
        lst_potential_units.append((unit, pos_rank, length_rank))

    lst_potential_units.sort(key=lambda x: x[2])
    lst_potential_units.sort(key=lambda x: x[1])
    return lst_potential_units


def get_unit_offerings(unit_code: str, handbook: dict) -> list[str]:
    """
    Gets the offerings for the unit.

    Args:
        unit_code (str): The unit code to retrieve offerings for.
        handbook (dict): The handbook data dictionary containing unit information.

    Returns:
        list: List of offerings for the unit.
    """
    offerings = [(offering['period'], offering['campus']) for offering in handbook[unit_code]["offerings"]]
    return offerings


def units_can_take_this_semester(unit_list: list, handbook: dict, period: str = None, filter_arg: str = None) -> list:
    """
    Determines the units that can be taken this semester based on the list of units already completed.

    Args:
        unit_list (list): List of unit codes that have been completed.
        handbook (dict): The handbook data dictionary containing unit information.
        period (str): The period to check for (default: None).
        filter (str): Filter argument to apply while determining units (default: False).
    Returns:
        list: List of unit codes that can be taken this semester.
    """

    units = units_can_take(unit_list, handbook, filter_arg)
    if period is None:
        return units
    
    output = []
    for unit in units:
        offerings = get_unit_offerings(unit, handbook)
        for period_c, campus in offerings:
            if period == period_c:
                output.append(unit)
                break
    return output
