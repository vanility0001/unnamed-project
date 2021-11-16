import nextcord
import os.path
import subprocess
import time

from nextcord.ext import commands
from datetime import datetime

client = commands.Bot(command_prefix="!")


class Evaluator:
    def __init__(self):
        print("> created new evaluator")

    @staticmethod
    async def create_temp_file(code: str) -> tuple:
        date: str = datetime.now().strftime("%d%m%Y%H%M%S")
        filename: str = f"temp-{date}.py"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)

        return "File created!", filename

    @staticmethod
    async def get_file_info(file_name: str) -> list:
        stats = os.stat(file_name)

        return [
            stats.st_size / 1000,
            datetime.fromtimestamp(stats.st_atime).strftime("%d/%m/%Y, %H:%M:%S"),
        ]

    @staticmethod
    async def run_temp_file(file_name: str) -> tuple:
        start = time.time()
        proc = subprocess.Popen(
            ["py", "-3.9", "-u", file_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        output = proc.communicate()[0].decode()
        finish = time.time() - start

        return output, proc.returncode, finish

    @staticmethod
    async def del_temp_file(file_name: str) -> None:
        if os.path.exists(file_name):
            os.remove(file_name)


evaluator = Evaluator()


@client.command(aliases=["e", "eval"])
async def evaluate(ctx: commands.Context, *, code: str) -> None:
    message = await ctx.message.reply("Creating file...")
    embed = nextcord.Embed()
    if len(code) <= 12:
        await message.edit(content="No code provided!")
        return

    if not code.startswith("```py") and not code.startswith("```python"):
        await message.edit(content="Please embed your code in a Python block!")
        return

    if code.startswith("```python"):
        code = code[9:-3]
    else:
        code = code[5:-3]

    lines = len(code.splitlines()) - 1

    data = await evaluator.create_temp_file(code)
    await message.edit(content=data[0])
    output = await evaluator.run_temp_file(data[1])
    a = await evaluator.get_file_info(data[1])
    if len(output[0]) <= 0:
        embed.add_field(
            name=f"Executed {str(lines)} lines in {output[2]}s with return code {output[1]}",
            value=f"```[No output]```",
        )
    else:
        embed.add_field(
            name=f"Executed {str(lines)} lines in {output[2]}s with return code {output[1]}",
            value=f"```{output[0]}```",
        )

    await message.edit(content=None, embed=embed)
    await evaluator.del_temp_file(data[1])

client.run("token")
