from array import array
from sqlite3 import connect
import discord


async def playConnectFour(ctx, author, opponent):
    embed=discord.Embed(title="Sample Embed",
                        url="https://realdrewdata.medium.com/",
                        description="This is an embed that will show how to build an embed and the different components",
                        color=0xFF5733)

    grid = ConnectFour()

    embed.add_field(name="Connect Four Grid", value=grid.printConnectFourGrid(), inline=False)
    embed.set_footer(text=f"{author.display_name} VS {opponent.display_name}")

    await ctx.send(embed=embed)


class ConnectFour(object):
    ROW = 6
    COLUMN = 7

    def drawConnectFourGrid(self) -> list:
        a = [[":thinking:" for x in range(self.COLUMN)] for x in range(self.ROW)]
        return a

    def printConnectFourGrid(self) -> str:
        connect_four_grid = self.drawConnectFourGrid();
        connect_four_string = "";

        for row in connect_four_grid:
            for column in row:
                connect_four_string += column
            connect_four_string += "\n"

        return connect_four_string



