import lightbulb
import json
import hikari
from lightbulb.utils.pag import EmbedPaginator
from custom_commands.main_commands import *
plugin = lightbulb.Plugin('unit_commands')


"Global variables"
with open('JSON\handbook_data_complete.json', 'r') as fp_1:
    handbook: dict = json.load(fp_1)

with open('JSON\help_cmd.json', 'r') as fp_2:
    help_dict: dict = json.load(fp_2)

with open('JSON\sca_cost.json', 'r') as fp_3:
    sca_cost: dict = json.load(fp_3)

def load(bot):
    bot.add_plugin(plugin)


@plugin.command
@lightbulb.option('command', 'Insert command name')
@lightbulb.command('help', 'Assistance with commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx: lightbulb.Context):
    desc = help_dict.get(ctx.options.command, False)
    if not desc: desc = "No command found."
    embed = hikari.Embed(title='Commmand help')
    embed.add_field(ctx.options.command,desc)
    await ctx.respond(embed)

@plugin.listener(hikari.InteractionCreateEvent)
async def on_component_interaction(event: hikari.InteractionCreateEvent) -> None:
    # Filter out all unwanted interactions
    if not isinstance(event.interaction, hikari.ComponentInteraction):
        return
    interaction_info =  event.interaction.custom_id.split(",")
    if (interaction_info[0] == "search"):
        label = interaction_info[1]
        unit_code = interaction_info[2]

        unit_dict = handbook[unit_code]
        title_str = f'{unit_code} {label}'
        output_str = ""
        if label == "Prerequisites":
            unit_prereqs = unit_dict['requisites']['prerequisites']

            for unit in unit_prereqs:
                temp_lst = [f"\n{unit['NumReq']} of"]
                temp_lst.append("\n".join([unit_or for unit_or in unit['units']]))
                output_str += "\n".join(temp_lst)

        elif label == "Corerequisites":
            unit_coreqs = unit_dict['requisites']['corequisites']

            for unit in unit_coreqs:
                temp_lst = [f"\n{unit['NumReq']} of"]
                temp_lst.append("\n".join([unit_or for unit_or in unit['units']]))
                output_str += "\n".join(temp_lst)

        elif label == "Prohibitions":
            unit_prohibs = unit_dict['requisites']['prohibitions']
            output_str = "\n".join(unit_prohibs)

        embed = hikari.Embed(title=title_str,
                            description=output_str)
        if label == "Back":
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
    unit_code = ctx.options.code.upper()
    unit_dict = handbook.get(unit_code, False)
    if (not unit_dict):
        await ctx.respond(content="Invalid unit code")
    # Creation of embed
    embed = embed_maker(unit_code, handbook)
    # make button: requisites
    row = ctx.bot.rest.build_message_action_row()
    labels = ["Prerequisites", "Corerequisites", "Prohibitions", "Back"]
    for label in labels:
        row.add_interactive_button(
        hikari.ButtonStyle.PRIMARY,
        f'search,{label},{unit_code}', label= label)
        
    await ctx.respond(embed, component=row)


@plugin.command
@lightbulb.option("code", "Insert a valid unit code")
@lightbulb.option("filter_arg", "Optional argument for filtering.", required=False)
@lightbulb.command('search_prereqs_to', 'Searches for units that the current unit is a prereq to.')
@lightbulb.implements(lightbulb.SlashCommand)
async def search_prereqs_to(ctx: lightbulb.Context):
    unit_code = ctx.options.code.upper()
    filter_arg = ctx.options.filter_arg
    unit_dict = handbook.get(unit_code, False)
    if (not unit_dict):
        await ctx.respond(content="Invalid unit code")
    prereqs_to_str = str_prereqs_to(unit_code, handbook, filter_arg)
    if (not prereqs_to_str):
        prereqs_to_str = "No current units."
    embed = hikari.Embed(title=f"{unit_code}: Prerequisites to")
    embed.add_field("Units:", prereqs_to_str)
    await ctx.respond(embed)


@plugin.command
@lightbulb.option("unit_list", "Insert a list of valid units you have completed")
@lightbulb.option("filter_arg", "An extra filter for units.", required= False)
@lightbulb.command('units_can_take', 'Returns a list of units you can complete, given an input list of completed units')
@lightbulb.implements(lightbulb.SlashCommand)
async def list_codes(ctx: lightbulb.Context):
    invalid_units = []
    invalid_counter = False
    units = ctx.options.unit_list.upper().replace(" ", "").split(",")
    filter_arg = ctx.options.filter_arg
    units = list(set(units))

    for unit in units:
        if unit not in handbook:
            invalid_units.append(unit)
            invalid_counter = True
    if (invalid_counter):
        await ctx.respond("The following input units are invalid:\n"+"\n".join(invalid_units))

    takeable_units = units_can_take(units, handbook, filter_arg)
    embed = hikari.Embed(title="List of units")
    output = "\n".join(takeable_units)
    if (len(takeable_units) == 0):
         output = "No takeable units."
    embed.add_field("Units:", output)
    await ctx.respond(embed)


@plugin.command
@lightbulb.option("unit_name", "Insert a valid unit code")
@lightbulb.option("top_x_results", "Specifies the top x results, default is 100", required= False, default= 100)
@lightbulb.command('search_name', 'Searches for units with similar name to request.')
@lightbulb.implements(lightbulb.SlashCommand)
async def fuzzy_search(ctx: lightbulb.Context):
    unit_request = ctx.options.unit_name
    top_x = int(ctx.options.top_x_results)
    if (len(unit_request) <= 4):
        await ctx.respond(content= "A more specific request is required!")
        return
    lst_potential_units = search_by_name(unit_request, handbook)
    if not (lst_potential_units): await ctx.respond(content="No units found containing input request.")
    lst_potential_units = lst_potential_units[0:min(top_x, len(lst_potential_units))]
    output = [unit[0] + f" {handbook[unit[0]]['unit_name']}" for unit in lst_potential_units]
    pag = EmbedPaginator(max_lines=25)
    for unit in output:
        pag.add_line(unit)
    for page in pag.build_pages():
        await ctx.respond(page)


    

@plugin.listener(hikari.MemberCreateEvent)
async def greet(event: hikari.MemberCreateEvent) -> None:
    message = "hallowhatdoyoustudy"
    channel_id = 804513491763200006
    my_channel = 1061247563963039834
    user = event.member
    await plugin.bot.rest.create_message(my_channel, content=f"{user} has joined M@M")
    
@plugin.listener(hikari.MemberDeleteEvent)
async def left(event: hikari.MemberDeleteEvent) -> None:
    user = event.old_member
    my_channel = 1061247563963039834
    await plugin.bot.rest.create_message(my_channel, content=f"{user} has left M@M")


@plugin.command
@lightbulb.option("unit_list", "Insert a list of valid units.")
@lightbulb.option("domestic", "Input Y if domestic with CSP, N for not", required= True)
@lightbulb.command('unit_costs', 'Computes the expected cost for the list of units.')
@lightbulb.implements(lightbulb.SlashCommand)
async def list_codes(ctx: lightbulb.Context):

    units = ctx.options.unit_list.upper().replace(" ", "").split(",")
    units = list(set(units))
    
    expected_cost = sum([sca_cost[str(handbook[unit]['sca_band'])] * int(handbook[unit]['credit_points']) for unit in units])

    embed = hikari.Embed(title="List of units")
    output = "\n".join(units)
    if (len(units) == 0):
         expected_cost = 0
    embed.add_field("For the following units:", output)
    embed.add_field("Expected_cost: (AUD) ", expected_cost)
    await ctx.respond(embed)
