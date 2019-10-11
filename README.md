# Persimmon
A Python3 bot for Discord using discord.py.  
Created by [UnsignedByte](https://github.com/UnsignedByte) and licensed under [The MIT License](https://en.wikipedia.org/wiki/MIT_License).  
Add this bot to your server [here](https://discordapp.com/oauth2/authorize?client_id=631186998702506015&scope=bot&permissions=2146958847)!

## Commands
Prefix: `.`

Necessary arguments: `{var}`  
Optional arguments: `(var)`  
Remember to delete `{}` and `()`.


### Utilities

| **Name** | **Usage** | **Description** | **Aliases** |
|:-:|:-:|:-:|:-:|
|help|`.help (page)`|Displays help information. If no valid page number is given, the first page will be displayed.|`help`|
|info|`.info`|Displays general information about the bot.|`info`, `hi`|
|close|`.close`|Shut down the bot and save all data.|`close`, `shutdown`|
|save|`.save`|Save all data.|`save`|
|settings|`.settings {args}`|Look at Settings Subcommands.|`settings`|
|purge|`.purge {n}`|Clears the last `n` messages.|`clear`, `purge`|
|define|`.define {word}`|Retrieves the definition of a word from Merriam-Webster.|`define`, `dictionary`|
|wolframalpha|`.wolframalpha {query}`|Queries wolframalpha and returns an image containing the result|`wolframalpha`, `wolfram`, `wa`|

#### Settings Subcommands

| **Name** | **Usage** | **Description** | **Aliases** |
|:-:|:-:|:-:|:-:|
|settings|`.settings {subcommand} (args)`|Settings for the bot. Requires the `manage server` permission. | `settings`|
|disable|`.settings disable {cmd} {channel(s)}`|Disables a command in the specified channels.|`disable`|
|enable|`.settings enable {cmd} {channel(s)}`|Enables a command in the specified channels.|`enable`|

### Fun
| **Name** | **Usage** | **Description** | **Aliases** |
|:-:|:-:|:-:|:-:|
|invite|`.invite`|Creates an invite link for the server!|`invite`|
|thesaurus|`.thesaurus`|Thesaurus-ifies a sentence.|`thesaurus`|
|rps|`.rps {item}`|Plays rock paper scissors!|`rps`|
|trivia|`.trivia (difficulty) (category)`|Answer trivia questions for money!|`trivia`|

### Gambling/Economy
| **Name** | **Usage** | **Description** | **Aliases** |
|:-:|:-:|:-:|:-:|
|daily|`.daily`|Gives you your daily money!|`daily`|
|money|`.money (mention)`|Displays your money or someone else's money.|`money`|
|bank|`.bank`|Displays your bank account information.|`bank`|
|deposit|`.deposit {amount}`|Deposits Mooney into your bank account.|`deposit`, `dep`|
|withdraw|`.withdraw {amount}`|Withdraws Mooney from your bank account.|`withdraw`, `with`|

#### Ping Logging
| **Name** | **Usage** | **Description** | **Aliases** |
|:-:|:-:|:-:|:-:|
|who ping|`who ping`|Check pings|None|
|clear ping|`clear ping`|Clear saved pings|None|
