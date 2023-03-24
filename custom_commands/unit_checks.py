

def unit_prohibition_check(unit_list: str, unit_code: str, handbook: dict) -> bool:
    # if any unit in the unit list is prohibited compared to unit code, return False.
    unit_prohibs_list = handbook[unit_code]['requisites']['prohibitions']
    for unit in unit_list:
        if unit in unit_prohibs_list:
            return False
    return True


def prereqs_to(unit_code: str, handbook: dict, filter = None) -> list:
    """    
    Input a unit code.
    Looks into each unit in the handbook.
    if the unit code is in the unit prereq list,
    append the unit.

    Args:
        unit_code (str): _description_
        handbook (dict): _description_

    Returns:
        str: _description_

    """
    output = []
    for unit in handbook:
        filter_val = filter_check(unit, filter)
        if not filter_val:
            continue
        for unit_prereq_dict in handbook[unit]['requisites']['prerequisites']:
            if (unit_code in unit_prereq_dict['units']):
                output.append(unit)
    return output


def unit_prereq_checker(unit_list: list, unit_code: str, handbook: dict) -> tuple:
    """     
    First we must loop all the "or" unit conditionals.
     Ensure unit_code is valid.
     Ensure all valid units are selected in list.
     Ensure that unit itself is not already completed.

    Args:
        unit_list (_type_): _description_
        unit_code (_type_): _description_
        handbook (_type_): _description_

    Returns:
        bool: _description_
    """
    # looping through unit_code prerequisites to see if prereqs are met.
    # at least one unit in the unit list is actually in the prereq.
    unit_prereq_dict = handbook[unit_code]['requisites']['prerequisites']
    counter = 0
    for units_and in unit_prereq_dict:
        counter = 0
        numreq = units_and['NumReq']
        units_or = units_and['units']
        for unit in unit_list:
            if unit in units_or:
                counter += 1
        if (counter < numreq):
            return (False, counter)
    return True, counter


def unit_credit_prereq_check(unit_list, unit_code, handbook) -> bool:
    credit_total = 0
    for unit in unit_list:
        credit_total += int(handbook[unit]['credit_points'])
    unit_credit_prereq = int(handbook[unit_code]['requisites']['cp_required'])

    if (credit_total < unit_credit_prereq):
        return False
    return True


def filter_check(unit_code, filter):
    if filter is None:
        return True
    for i in range(0, len(filter)):
        if unit_code[i] != filter[i]:
            return False
    return True