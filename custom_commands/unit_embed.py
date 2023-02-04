from hikari import Embed

def embed_maker(unit_code: str, handbook: dict) -> Embed:
    """
    Makes an embed for a unit, with information about it.
    
    
    """
    unit_dict = handbook.get(unit_code, {})
    # Creation of embed

    unit_name = unit_dict['unit_name']
    unit_code = unit_dict['unit_code']
    unit_desc = unit_dict['description'].replace("<p>", "").replace("</p>", "")
    unit_cp = unit_dict['credit_points']
    unit_school = unit_dict['school']
    # Requisites
    unit_reqs_dict = unit_dict['requisites']


    # Offerings
    unit_offerings_dict = unit_dict['offerings']

    embed = Embed(title=unit_name, description=unit_desc)

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

    return embed
