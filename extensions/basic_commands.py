import lightbulb
import json
import hikari
from custom_commands.main_commands import *
plugin = lightbulb.Plugin('basic_commands')

with open('JSON\handbook_data_complete.json', 'r') as f:
    handbook = json.load(f)


def load(bot):
    bot.add_plugin(plugin)


@plugin.listener(hikari.InteractionCreateEvent)
async def on_component_interaction(event: hikari.InteractionCreateEvent) -> None:
    # Filter out all unwanted interactions
    if not isinstance(event.interaction, hikari.ComponentInteraction):
        return
    print(event.interaction.custom_id)
    label, unit_code = event.interaction.custom_id.split(",")
    unit_dict = handbook[unit_code]
    title_str = f'{unit_code} {label}'
    output_str = ""
    if label == "Prerequisites":
        unit_prereqs = unit_dict['requisites']['prerequisites']

        for prereq_unit_dict in unit_prereqs:
            prereq_unit = f"{prereq_unit_dict['NumReq']} of "
            for unit in prereq_unit_dict['units']:
                prereq_unit += f"{unit}, "
            prereq_unit += "\n"
            output_str += prereq_unit

    elif label == "Corerequisites":
        unit_coreqs = unit_dict['requisites']['corequisites']

        for coreqs_unit_dict in unit_coreqs:
            coreqs_unit = f"{coreqs_unit_dict['NumReq']} of "
            for unit in coreqs_unit_dict['units']:
                coreqs_unit += f"{unit}, "
            coreqs_unit += "\n"
            output_str += coreqs_unit

    elif label == "Prohibitions":
        unit_prohibs = unit_dict['requisites']['prohibitions']
        output_str = "\n".join(unit_prohibs)

    embed = hikari.Embed(title=title_str,
                         description=output_str)
    if label == "back":
        embed = embed_maker(unit_code, handbook)
    try:
        await event.interaction.create_initial_response(

            hikari.ResponseType.MESSAGE_UPDATE,
            embed=embed,
        )
    except hikari.NotFoundError:
        await event.interaction.edit_initial_response(
            embed=embed,
        )


@plugin.command
@lightbulb.option("code", "Insert a valid unit code")
@lightbulb.command('search', 'Search the handbook by unit code.')
@lightbulb.implements(lightbulb.SlashCommand)
async def search_unit_code(ctx: lightbulb.Context):
    unit_dict = search_by_unit_code(ctx.options.code, handbook)
    if (not unit_dict):
        await ctx.respond(content="Invalid unit code")
    unit_code = ctx.options.code
    # Creation of embed
    embed = embed_maker(ctx.options.code, handbook)
    # make button: requisites
    row = ctx.bot.rest.build_message_action_row()
    labels = ["Prerequisites", "Corerequisites", "Prohibitions", "back"]
    for label in labels:
        row.add_button(hikari.ButtonStyle.PRIMARY, f'{label},{unit_code}').set_label(
            label).add_to_container()
    await ctx.respond(embed, component=row)



@plugin.command
@lightbulb.option("code", "Insert a valid unit code")
@lightbulb.command('search_prereqs_to', 'Searches for units that the current unit is a prereq to.')
@lightbulb.implements(lightbulb.SlashCommand)
async def search_prereqs_to(ctx: lightbulb.Context):
    unit_code = ctx.options.code
    prereqs_to_str = str_prereqs_to(unit_code, handbook)
    if (not prereqs_to_str):
        prereqs_to_str = "No current units."
    embed = hikari.Embed(title=f"{unit_code}: Prerequisites to")
    embed.add_field("Units:", prereqs_to_str)
    await ctx.respond(embed)

@plugin.command
@lightbulb.option("unit_list", "Insert a list of valid units you have completed")
@lightbulb.command('units_can_complete', 'Returns a list of units you can complete, given an input list of completed units')
@lightbulb.implements(lightbulb.SlashCommand)
async def list_codes(ctx: lightbulb.Context):
    output = ""
    unit_list = ctx.options.unit_list.replace(" ", "").split(",")
    units_lst = units_can_complete(unit_list, handbook)
    for unit in units_lst:
        output += f"{unit}\n"

    embed = hikari.Embed(title="List of units")
    embed.add_field("Units:", output)
    await ctx.respond(embed)
