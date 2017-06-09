IRC Bot
=======

A simple IRC Bot made in python3.  
Since the bot uses a private channel (namely **##bot-testing**), the adminname has been set the same as the bot nickname, for verifying exit status. You can change the adminname with your own IRC nickname, if the bot is deployed on a public channel.

Package Used
------------
* socket (Read [here](https://docs.python.org/3/howto/sockets.html "Socket") for details)  
  `pip3 install socket`

Running the bot
---------------
* `cd` to the root of the project.
* In the terminal run:  
  `python3 irc_bot.py`
* Head to [irc.freenode.net](https://webchat.freenode.net/ "IRC Chat") and enter the credentials as per the code.
* Start chatting and enjoy!!

Usage/Sample Commands
---------------------
1. `Hi shreyansh26Bot` i.e `Hi [bot_nickname]`
2. `.tell ##bot-testing Hey! Whats up?` i.e `.tell [channel_name] [message_text]`
3. `bye shreyansh26Bot` i.e `bye [bot_nickname]`
