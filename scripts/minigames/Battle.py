import random
import discord
import asyncio
import time
from scripts.dbmanagement.SQLiteDBHandler import update_points


pokemon = ["Geodude using Rock Throw", "Diglett using Sand Attack", "Glaceon using Ice Shard", "Bulbasaur using Razor Leaf", "Charizard using Fire Spin"]

winning_matchups = [("Geodude using Rock Throw", "Glaceon using Ice Shard"), ("Diglett using Sand Attack", "Geodude using Rock Throw"), ("Glaceon using Ice Shard", "Diglett using Sand Attack"), ("Geodude using Rock Throw", "Charizard using Fire Spin"), ("Bulbasaur using Razor Leaf", "Geodude using Rock Throw"),
            ("Charizard using Fire Spin", "Glaceon using Ice Shard"), ("Glaceon using Ice Shard", "Bulbasaur using Razor Leaf"), ("Bulbasaur using Razor Leaf", "Diglett using Sand Attack"), ("Diglett using Sand Attack", "Charizard using Fire Spin"), ("Charizard using Fire Spin", "Bulbasaur using Razor Leaf")]


async def play_battle(ctx, client):
    # initialize health
    player_pokemon_health = 100
    bot_pokemon_health = 100

    member = ctx.message.author
    # prompt user for pokemon options
    await ctx.send(f"{member.mention}, choose your pokemon from the options below!\n 1 for Geodude using Rock Throw.\n 2 for Diglett using Sand Attack.\n 3 for Glaceon using Ice Shard.\n 4 for Bulbasaur using Razor Leaf.\n 5 for Charizard using Fire Spin.")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content

    # bot chooses a random pokemon
    rand = random.randint(0, 4)
    bot_pokemon = pokemon[rand]

    try:   
        # get users choice
        msg = await client.wait_for("message", check=check)
        player_choice = int(msg.content) - 1 
        player_pokemon = pokemon[player_choice]
        
        await ctx.send(f"Nice choice, a {player_pokemon}!\n{bot_pokemon}, I choose you!")

        # pokemon battle based on winning/losing/tied matchup
        if (player_pokemon,bot_pokemon) in winning_matchups:
            while True:
                player_pokemon_damage = random.randint(0, 70)
                bot_pokemon_health -= player_pokemon_damage
                await ctx.send(f"\n{member.mention}'s pokemon attacked for {player_pokemon_damage} damage!\nMy pokemon has {bot_pokemon_health} health remaining!")
                if bot_pokemon_health <= 0:
                    await ctx.send(f"A critical hit! {member.mention} & your {player_pokemon} are your champions! Well fought!")
                    await win(ctx)
                    break
                bot_attack_dmg = random.randint(0, 30)
                player_pokemon_health -= bot_attack_dmg
                await ctx.send(f"\nMy pokemon attacked for {bot_attack_dmg} damage!\n{member.mention}'s pokemon has {player_pokemon_health} health remaining!")
                if player_pokemon_health <= 0:
                    await ctx.send(f"{member.mention}'s pokemon cannot keep up! Me & my {bot_pokemon} win! Better luck next time!")
                    break
        elif bot_pokemon == player_pokemon:
            while True:
                player_pokemon_damage = random.randint(0, 50)
                bot_pokemon_health -= player_pokemon_damage
                await ctx.send(f"\n{member.mention}'s pokemon attacked for {player_pokemon_damage} damage!\nMy pokemon has {bot_pokemon_health} health remaining!")
                if bot_pokemon_health <= 0:
                    await ctx.send(f"My pokemon cannot go any longer! {member.mention} & your {player_pokemon} are your champions! Well fought!")
                    await win(ctx)
                    break
                bot_attack_dmg = random.randint(0, 50)
                player_pokemon_health -= bot_attack_dmg
                await ctx.send(f"\nMy pokemon attacked for {bot_attack_dmg} damage!\n{member.mention}'s pokemon has {player_pokemon_health} health remaining!")
                if player_pokemon_health <= 0:
                    await ctx.send(f"{member.mention}'s pokemon fainted! Me & my {bot_pokemon} win! Better luck next time!")
                    break
        else:
            while True:
                player_pokemon_damage = random.randint(0, 30)
                bot_pokemon_health -= player_pokemon_damage
                await ctx.send(f"\n{member.mention}'s pokemon attacked for {player_pokemon_damage} damage!\nMy pokemon has {bot_pokemon_health} health! remaining")
                if bot_pokemon_health <= 0:
                    await ctx.send(f"My pokemon cannot go on! {member.mention} & your {player_pokemon} are your champions! Well fought!")
                    await win(ctx)
                    break
                bot_attack_dmg = random.randint(0, 70)
                player_pokemon_health -= bot_attack_dmg
                await ctx.send(f"\nMy pokemon attacked for {bot_attack_dmg} damage!\n{member.mention}'s pokemon has {player_pokemon_health} health remaining!")
                if player_pokemon_health <= 0:
                    await ctx.send(f"A critical hit! Me & my {bot_pokemon} win! Better luck next time!")
                    break

    except IndexError:
            await ctx.send(f"That's not a valid choice! I'm out of here!")

    except ValueError:
            await ctx.send(f"That's not a valid choice! I'm out of here!")
            
    except asyncio.TimeoutError:
        await ctx.send("This is not that hard, try faster next time!")


async def win(ctx):
    # Award 10 points
    userID = ctx.message.author.id
    update_points(userID, int(10))