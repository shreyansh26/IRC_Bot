# Help taken from Linux Academy :)

#!/usr/bin/python3
import socket

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "chat.freenode.net" # Server

channel = "##bot-testing" # Channel

botnick = "shreyansh26Bot" # Your bots nick.

adminname = "shreyansh26Bot" #Your IRC nickname.
exitcode = "bye " + botnick 

ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667

ircsock.send(bytes("USER "+ adminname +" "+ adminname +" "+ adminname + " " + adminname + "\n", "UTF-8")) # user information
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) 

def joinchan(chan): # join channel(s).

  
  ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8")) 
  
  ircmsg = ""
  while ircmsg.find("End of /NAMES list.") == -1: 
    ircmsg = ircsock.recv(2048).decode("UTF-8")
    ircmsg = ircmsg.strip('\n\r')
    print(ircmsg)
#This function doesn’t need to take any arguments as the response will always be the same. Just respond with "PONG :pingis" to any PING. 
#Different servers have different requirements for responses to PING so you may need to adjust/update this depending on your server. I’ve used this particular example with Freenode and have never had any issues.
def ping(): # respond to server Pings.
  ircsock.send(bytes("PONG :pingis\n", "UTF-8"))
#All we need for this function is to accept a variable with the message we’ll be sending and who we’re sending it to. We will assume we are sending to the channel by default if no target is defined. 
#Using target=channel in the parameters section says if the function is called without a target defined, example below in the Main Function section, then assume the target is the channel.
def sendmsg(msg, target=channel): # sends messages to the target.
  #With this we are sending a ‘PRIVMSG’ to the channel. The ":” lets the server separate the target and the message.
  ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))
#Main function of the bot. This will call the other functions as necessary and process the information received from IRC and determine what to do with it.
def main():
  # start by joining the channel we defined in the Global Variables section.
  joinchan(channel)
  #Start infinite loop to continually check for and receive new info from server. This ensures our connection stays open. 
  #We don’t want to call main() again because, aside from trying to rejoin the channel continuously, you run into problems when recursively calling a function too many times in a row. 
  #An infinite while loop works better in this case.
  while 1:
    #Here we are receiving information from the IRC server. IRC will send out information encoded in UTF-8 characters so we’re telling our socket connection to receive up to 2048 bytes and decode it as UTF-8 characters. 
    #We then assign it to the ircmsg variable for processing.
    ircmsg = ircsock.recv(2048).decode("UTF-8")
    # This part will remove any line break characters from the string. If someone types in "\n” to the channel, it will still include it in the message just fine. 
    #This only strips out the special characters that can be included and cause problems with processing.
    ircmsg = ircmsg.strip('\n\r')
    #This will print the received information to your terminal. You can skip this if you don’t want to see it, but it helps with debugging and to make sure your bot is working.
    print(ircmsg)
    #Here we check if the information we received was a PRIVMSG. PRIVMSG is how standard messages in the channel (and direct messages to the bot) will come in. 
    #Most of the processing of messages will be in this section.
    if ircmsg.find("PRIVMSG") != -1:
      #First we want to get the nick of the person who sent the message. Messages come in from from IRC in the format of ":[Nick]!~[hostname]@[IP Address] PRIVMSG [channel] :[message]”
      #We need to split and parse it to analyze each part individually.
      name = ircmsg.split('!',1)[0][1:].replace('_','')
      #Above we split out the name, here we split out the message.
      message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
      #print(name)
      #print(message)
      #Now that we have the name information, we check if the name is less than 17 characters. Usernames (at least for Freenode) are limited to 16 characters. 
      #So with this check we make sure we’re not responding to an invalid user or some other message.
      if len(name) < 17:
        #And this is our first detection block! We’ll use things like this to check the message and then perform actions based on what the message is. 
        #With this one, we’re looking to see if someone says Hi to the bot anywhere in their message and replying. Since we don’t define a target, it will get sent to the channel.
        if message.find('Hi ' + botnick) != -1:
          sendmsg("Hello " + name + "!")
        #Here is an example of how you can look for a ‘code’ at the beginning of a message and parse it to do a complex task. 
        #In this case, we’re looking for a message starting with ".tell” and using that as a code to look for a message and a specific target to send to. 
        #The whole message should look like ".tell [target] [message]” to work properly.
        if message[:5].find('.tell') != -1:
          #First we split the command from the rest of the message. We do this by splitting the message on the first space and assigning the target variable to everything after it.
          target = message.split(' ', 1)[1]
          #After that, we make sure the rest of it is in the correct format. If there is not another then we don’t know where the username ends and the message begins!
          if target.find(' ') != -1:
              #If we make it here, it means we found another space to split on. We save everything after the first space (so the message can include spaces as well) to the message variable.
              message = target.split(' ', 1)[1]
              #Make sure to cut the message off from the target so it is only the target now.
              target = target.split(' ')[0]

          #if there is no defined message and target separation, we send a message to the user letting them know they did it wrong.
          else:

            #We do this by setting the target to the name of the user who sent the message (parsed from above)
            target = name
            #and then setting a new message. Note we use single quotes inside double quotes here so we don’t need to escape the inside quotes.
            message = "Could not parse. The message should be in the format of ‘.tell [target] [message]’ to work properly."
            #And finally we send the message to our target.
          sendmsg(message, target)
        
        if name.lower() == adminname.lower() and message.rstrip() == exitcode:
          #If we do get sent the exit code, then send a message (no target defined, so to the channel) saying we’ll do it, but making clear we’re sad to leave.
          sendmsg("oh...okay. :'(")
          #Send the quit command to the IRC server so it knows we’re disconnecting.
          ircsock.send(bytes("QUIT \n", "UTF-8"))
          #The return command returns to when the function was called (we haven’t gotten there yet, see below) and continues with the rest of the script. 
          #In our case, there is not any more code to run through so it just ends.
          return
    #If the message is not a PRIVMSG it still might need some response.
    else:
      #Check if the information we received was a PING request. If so, we call the ping() function we defined earlier so we respond with a PONG.
      if ircmsg.find("PING :") != -1:
        ping()

main()
