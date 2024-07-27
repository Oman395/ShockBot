# Shock Collar Controller
This is a project created by [@yuridoggy](https://x.com/yuridoggy) and [@OmanTheHuman1](https://x.com/OmanTheHuman1) on twitter, made to control a specific brand of 433 MHz shock collar wirelessly.

This project uses the arduino [collar library](https://github.com/CrashOverride85/collar/tree/master) made by [CrashOverride85](https://github.com/CrashOverride85), for it's "type 1" collars.

The collar meant for use with this project is the [CaiXianLin](https://aliexpress.com/item/1005005133046985.html) collar, sold on Aliexpress.
- This is the same collar used by Pishock and Openshock, so it is compatible with these projects.

This project takes heavy inspiration from [PiShock](https://pishock.com/#/) and [OpenShock](https://openshock.org/#features), although uses none of their resources, and does not require an ESP32, instead requiring a computer with an internet connection and an arduino.

## What is it?
There are two components to the shock controller, being the transmitter, and a digital interface. There are two selections of digital interface, and only one can be used at a time.

[Transmitter Instructions](#transmitter)
- [Building the Transmitter](#building-the-transmitter)
- [Flashing the Transmitter](#flashing-the-transmitter)

[Interface Instructions](#interface)
- [Discord Bot](#discord-bot)
  - [Download List](#download-list)
  - [Running the Bot](#running-the-bot)
  - [Bot Commands](#bot-commands)
  - [Pairing](#pairing)

# Transmitter
## Building the Transmitter
### Parts List
- Arduino of any kind, this project was tested on an [Arduino Nano](https://store.arduino.cc/products/arduino-nano), which can be found for cheap on [Aliexpress](https://www.aliexpress.us/item/3256804883476369.html).
- 433 MHz Transmitter, found on [Aliexpress](https://www.aliexpress.us/item/3256806137174797.html?channel=twinner ), or [Amazon](https://a.co/d/cJgeM4a)
- (Optional) [Female to Female Cable connectors](https://www.aliexpress.us/item/3256804460701476.html), if you don't have a soldering iron.

## Assembly
- This will be using the Arduino Nano as an example, as that is what this project is built on. This should be easily changed for any other arduinos as long as the pins line up.

First, make sure everything is unplugged until you are sure everything is right. Do NOT work on this while the arduino is plugged in.

#### Step one

Connect power to the transmitter. This will be from black to black, and red to red in this picture (the color of the wire doesn't matter, just there for clarity).

Each pin is labeled on the Arduino and Transmitter, Connect GND to GND, and 5V to VCC

This can be done with your cable connectors, or with wires and solder.

![image](https://github.com/user-attachments/assets/1ba75857-157b-47a0-8d32-01aeb5273696)
![image](https://github.com/user-attachments/assets/4276c202-018c-44e9-8594-393329b440b7)

#### Step two

Connect the transmitter's output to the Arduino. In this picture it is from yellow to yellow. 

Connect the pin labeled D2 on the Arduino to the unlabeled remaining pin on the transmitter.
![image](https://github.com/user-attachments/assets/0efb3dda-313d-49ec-b7fd-927e707daf93)
![image](https://github.com/user-attachments/assets/13b34efb-7fa4-475a-8db4-17cfe408e047)

And you're done! From here, just plug in the Arduino into the computer.

## Flashing the Transmitter
Now that you've built the transmitter, you need to put some code on it for it to send signals to your shock collar. 

### Advanced
- Download the [Arduino IDE](https://www.arduino.cc/en/software)
- Open `shock_transmitter.ino` in the `shock_transmitter` folder, and run it. Upload it to the correct COM port, which can be done in the top left. This can be found by unplugging and replugging in your Arduino, to see which port it is using. You will have to select the correct model of Arduino that you are using in the top left as well.


# Interface
From here, you have a selection of two interfaces. One is a self-hosted discord bot, allowing your shock collar to be controlled through a discord bot of your own making. The other is a self-hosted website, which will require a VPN (like [ZeroTier](https://www.zerotier.com/)), or some other way of having somebody enter your network.

## Discord Bot
To set up the discord bot, first you'll need to download a few things.

You will need to have done everything under [Transmitter](#transmitter) before doing this.

### Download List
- [Python](https://www.python.org/downloads/) needs to be installed to run the bot. Go to their website, and install the latest version if you don't already have Python installed.
- [Package Installer for Python](https://pip.pypa.io/en/stable/installation/), or pip, is required to install some dependencies. In your command terminal (Which can be opened with Windows + R, then typing cmd), paste in `python -m ensurepip --upgrade` and let it run.

## Running the Bot
- Download this repository and unzip it. Go into the `ShockBot` folder, then the `discord_bot` folder, and open the file labeled `.env`
  - Open up the [Discord Developer Portal](https://discord.com/developers/applications), and sign into your account. From there, click "New Application. Give it any name you want, and click Create
  - From there, go to the `Installation` tab, and enable User Install if it is not enabled already.
  - Then, go to the Bot tab, and click `Reset Token`. Copy the new token it displays.
  - Go back to the `.env` file in the `ShockBot` folder, and paste it between the quotation marks.
- Next, open `config.json` in the same folder.
  - Open discord, and get your User ID. 
    - This can be done by going to your settings, then advanced, and turning on Developer Mode. 
    - From there, leave the menu, right click your name, and click `Copy User ID`.
  - Paste your User ID in place of the `0` next to `"user"` in `config.json`
- Go back to the `Developer Portal` and open up your bot. Go to the `Bot` tab again, and scroll down until you see `Privileged Gateway Intents`. Turn on Presence Intent, Server Members Intent, and Message Content Intent.
- Head to the `OAuth2` tab now, and click on `Bot` under `Scopes`, then under `Bot Permissions`, just click `Administrator`.
  - If you want to limit the bot, you can enable only `View Channels`, and `Send Messages` [UNTESTED]
- Go to the `Installation` tab, and copy the Install Link, and paste it into your browser. From there, you can choose to add it to a server or your account. This is recommended for server use, and needs to be added to a server before it can be used for an account.
  - For server usage, add it to a server.
  - Otherwise, add it to your own account. You will have to manually whitelist users under `data/whitelist.json` in the `discord_bot` folder, by copying the User ID of those you want to add, and pasting them in there with commas in between. You can still whitelist yourself with the `/whitelist` command demonstrated later.
- Now, run the `ports.py` file under `discord_bot/setup`. Now, plug in your Transmitter (or unplug it). Whichever port is now newly there (or not there), replace the port next to `"port"` in `config.json` with that port. If you unplugged your transmitter, plug it back in.
  
- Run the `install_reqs.cmd` file in `discord_bot/setup`.
- From here, you will just need to run the `main.py` file in the `ShockBot` folder, and the bot will be running!

### Run on Startup (WINDOWS ONLY)
If you want the bot to run when you turn on or restart your computer, run the `startup.bat` file in `discord_bot/setup`. 

If this doesn't work, press `Windows + R` and type in `shell:startup`. This will take you to the startup folder. Create a shortcut to the `main.pyw` file in `discord_bot`, and move that into the startup folder.

## Bot Commands
Every command the bot has is fairly self explanatory, and the parameters are listed when using the slash command. To use the bot, type `/`, then the name of the command.

#### Reload
- Reloads the bot, usually fixes any small errors.

#### Whitelist `[USER]`
- Whitelists a user, allowing them to shock, vibrate, or beep the shock collar.

#### Unwhitelist `[USER]`
- Unwhitelists a user, stopping them from shocking, vibrating, or beeping the shock collar.
  
#### Shock `[POWER]` `[DURATION]`
- Shocks the wearer at a strength of `[POWER]` for `[DURATION]`, in tenth's of a second, where a duration of 10 is 1 second.

#### Vibe `[DURATION]`
- Vibrates the collar at a strength of `[POWER]` for `[DURATION]`, in tenth's of a second, where a duration of 10 is 1 second.

#### Beep `[POWER]` `[DURATION]`
- Beeps the collar at a strength of `[POWER]` for `[DURATION]`, in tenth's of a second, where a duration of 10 is 1 second.

#### Pair
- Used to pair the collar during [pairing](#pairing)

#### Stop
- Stops any command being done to the collar, used to cancel commands or for emergencies.

## Pairing
- To pair the discord bot (when it is running) to the collar, hold down the power button on the collar until the light starts blinking. Then run the [Pair](#pair) command, which should beep the collar.
