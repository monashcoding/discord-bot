import hikari
from custom_commands.unit_search import *
def embed_maker(unit_code, handbook):
    unit_dict = search_by_unit_code(unit_code, handbook)
    # Creation of embed

    unit_name = unit_dict['unit_name']
    unit_code = unit_dict['unit_code']
    unit_desc = unit_dict['description'].replace("<p>", "").replace("</p>", "")
    unit_cp = unit_dict['credit_points']
    unit_school = unit_dict['school']
    # Requisites
    unit_reqs_dict = unit_dict['requisites']
    unit_prohibs = unit_reqs_dict['prohibitions']
    unit_coreqs = unit_reqs_dict['corequisites']

    # Prerequisites (nested dict)
    unit_prereqs = unit_reqs_dict['prerequisites']

    # Offerings
    unit_offerings_dict = unit_dict['offerings']

    embed = hikari.Embed(title=unit_name, description=unit_desc)

    # Adding fields: unit code, credit points, faculty, offerings
    embed.add_field("Unit code:", unit_code)
    embed.add_field("Credit points awarded upon completion:", unit_cp)
    embed.add_field("Faculty:", unit_school)

    # Offerings string formatting
    unit_offering_str = ""
    if (not unit_offerings_dict):
        unit_offering_str = "No offerings available"
    for offering in unit_offerings_dict:
        unit_offering_str += f"Campus: {offering['campus']}\nTeaching Period: {offering['period']}\nMode: {offering['mode']}\n\n"
    embed.add_field("Offerings:", unit_offering_str)
    embed.add_field("Number of credits required prior:",
                    unit_reqs_dict['cp_required'])

    # make button: requisites
    unit_prohibs_str = ""
    for unit in unit_prohibs:
        unit_prohibs_str += f"{unit}, "

    unit_coreqs_str = ""
    for unit in unit_coreqs:
        unit_coreqs_str += f"{unit}, "

    prereq_unit = ""
    for prereq_unit_dict in unit_prereqs:
        prereq_unit = f"{prereq_unit_dict['NumReq']} of "
        for unit in prereq_unit_dict['units']:
            prereq_unit += f"{unit}, "
        prereq_unit += " or "

    arr = prereq_unit.split(",")
    arr.pop()
    prereq_unit = "".join(arr)
    return embed
