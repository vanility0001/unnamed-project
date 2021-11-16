# unnamed-project
A Discord bot to execute Python code.

 ## Installation
Firstly, install [nextcord](https://github.com/nextcord/nextcord) by running
```shell
# Linux/macOS
python3 -m pip install -U nextcord

# Windows
py -3 -m pip install -U nextcord
```

Then, run main.py

## Setup
At the bottom of main.py, enter your token in the client.run()

## Running code
Run the !e command with your code wrapped in a Python code block:
```
!e ```python
print('Hello, world!')
``
```

The bot will run the code and return the output.

## Todo 
- Include support for more languages
- Make the evaluator more secure