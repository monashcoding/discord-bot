def unit_prohibition_check(unit_list: str, unit_code: str, handbook: dict) -> bool:
    """
    Checks if any unit in the given unit list is prohibited for the specified unit code.

    Args:
        unit_list (str): A comma-separated list of unit codes.
        unit_code (str): The unit code to check against.
        handbook (dict): The handbook data dictionary containing unit information.

    Returns:
        bool: True if no unit in the unit list is prohibited for the specified unit code, False otherwise.
    """
    unit_prohibs_list = handbook[unit_code]["requisites"]["prohibitions"]
    for unit in unit_list:
        if unit in unit_prohibs_list:
            return False
    return True


def prereqs_to(unit_code: str, handbook: dict, filter=None) -> list:
    """
    Retrieves a list of units that have the specified unit code as a prerequisite.

    Args:
        unit_code (str): The unit code to search for as a prerequisite.
        handbook (dict): The handbook data dictionary containing unit information.
        filter (Optional): An optional filter value. Defaults to None.

    Returns:
        list: A list of unit codes that have the specified unit code as a prerequisite.
    """
    output = []
    for unit in handbook:
        filter_val = filter_check(unit, filter)
        if not filter_val:
            continue
        for unit_prereq_dict in handbook[unit]["requisites"]["prerequisites"]:
            if unit_code in unit_prereq_dict["units"]:
                output.append(unit)
    return output


def unit_prereq_checker(unit_list: list, unit_code: str, handbook: dict) -> tuple:
    """
    Checks if the units in the unit list meet the prerequisites for the specified unit code.

    Args:
        unit_list (list): A list of unit codes to check for meeting prerequisites.
        unit_code (str): The unit code to check prerequisites against.
        handbook (dict): The handbook data dictionary containing unit information.

    Returns:
        tuple: A tuple containing a boolean value indicating whether the prerequisites are met
               and the counter value representing the number of units in the unit list that match the prerequisites.
    """
    unit_prereq_dict = handbook[unit_code]["requisites"]["prerequisites"]
    counter = 0
    for units_and in unit_prereq_dict:
        counter = 0
        numreq = units_and["NumReq"]
        units_or = units_and["units"]
        for unit in unit_list:
            if unit in units_or:
                counter += 1
        if counter < numreq:
            return (False, counter)
    return True, counter


def unit_credit_prereq_check(
    unit_list: list[str], unit_code: str, handbook: dict
) -> bool:
    """
    Checks if the total credits of the units in the unit list meet the credit prerequisites
    for the specified unit code.

    Args:
        unit_list (list): A list of unit codes to calculate the total credits.
        unit_code (str): The unit code to check credit prerequisites against.
        handbook (dict): The handbook data dictionary containing unit information.

    Returns:
        bool: True if the total credits meet the credit prerequisites, False otherwise.
    """
    credit_total = 0
    for unit in unit_list:
        credit_total += int(handbook[unit]["credit_points"])
    unit_credit_prereq = int(handbook[unit_code]["requisites"]["cp_required"])

    if credit_total < unit_credit_prereq:
        return False
    return True


def filter_check(unit_code, filter):
    """
    Checks if the unit code matches the filter pattern.

    Args:
        unit_code (str): The unit code to check against the filter.
        filter (str): The filter pattern to match the unit code against.

    Returns:
        bool: True if the unit code matches the filter pattern, False otherwise.
    """
    if filter is None:
        return True
    for i in range(0, len(filter)):
        if unit_code[i] != filter[i]:
            return False
    return True
