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

