![](https://github.com/nick16/Pokemon-BDSP-Kyogre-Shiny-Hunting-Bot/blob/main/images/kyogre.gif)

# Pokemon BD/SP Ramanas Park Kyogre Shiny Hunting Bot
This script is an edited version of run_controller_cli.py script from https://github.com/mart1nro/joycontrol. In order for this script to run you must download the joycontrol repository by mart1nro, and replace mart1nro's run_controller_cli.py with this one, and add this shiny_hunter.py into the same folder.

This script was created for shiny hunting the pokemon Kyogre from Ramanas Park in BD/SP.
This script is easily customizable, so feel free to customize to shiny hunt any pokemon!

![](https://github.com/nick16/Pokemon-BDSP-Kyogre-Shiny-Hunting-Bot/blob/main/images/shiny_kyogre_encounter.PNG)

# Setup
## Prerequisites
- Ubuntu OS (A virtual machine is prefered)
- A video capture device to capture the input from the docked Nintendo Switch to your PC (I used Elgato's Game Capture Hd60 Pro)
- A USB Bluetooth Adapter for your pc (Internal BT adapters may work if Ubuntu is your native OS, otherwise it must be a USB Bluetooth adapter for the virtual machine to use bluetooth)


## Setting up the Bot
This bot works by checking a single pixel on screen at a precise (x,y) to check whether Kyogre is shiny or not. This precise (x,y) is based off of OBS being in the most top left of the screen, and Kyogre being at a precise coordinate at the right time (by calculated sleep functions).

###  1) Install Ubuntu
   I used a virtual machine of Ubuntu 20.04.4 LTS inside of VirtualBox.
   If you use a virtual machine make sure USB 3.0 is selected in the USB options, so that the video input in OBS does not stutter.

### 2) Getting the emulated controller to connect to your switch
   Download and extract mart1nro's repository into a folder in your Ubuntu OS.

   Follow mart1nro's README to get the emulated controller to connect to your switch inside of your Ubuntu OS (Since his script aparently only works on certain Linux distros).
    
   Some hurdles I came across when trying to get the emulated controller connect to my switch:
   - mart1nro's script uses a function depracted in the latest version of the module hid, so when installing hid I forced version 1.0.0.
            ex: pip3 install hid==1.0.0
   - When I executed the script, it said I was missing modules I had installed, so my workaround was to install modules and run the script inside a virtual environment.
   - mart1nro's script relies on Bluetooth to connect the emulated controller to your Switch, so if you are using VirtualBox connect to your USB BT adapter by:
        1. Install VirtualBox's Guest Additions to enable USB access in the VM.
        2. Unplug the USB BT adapter from your PC.
        3. Within the virtual machine, plug in your USB BT adapter into your pc, and connect to the BT adapter (Devices > USB).
    
   Once you've gotten the controller to connect to your switch and you've played around controlling your swtch through the terminal to ensure you've done things right, drag the two files from this repo [run_controller_cli.py, shiny_hunter.py] into that same folder (replacing his run_controller_cli.py)

### 3) Setup Game Capture in Ubuntu
   We need to bring the game into Ubuntu so that we can check if the pokemon is shiny.
    I accomplished this in the virtual machine by downloading OBS, and adding a Video Capture Device Source. You must also select your capture device under Devices > Webcam in VirtualBox settings.
    Now make sure OBS is kept at the default window size and move it to the most top left of the screen (not bypassing the doc).

### 4) Done
   Make sure you have a save right infront of Kyogre, quit the game, and are hovering over Pokemon BD/SP, then start the script!


# Tips:
- How I figured out the best x,y coordinates to check if Kyogre is shiny is finding where Kyogre is still for the longest, and grabbed the x,y coordinated on that spot by using the command `xdotool getmouselocation --shell` with my cursor on the spot I wanted to grab.
- I created a stuck() function that gets executed right before we check the color of the pokemon, in the cases where the controller somehow misses a button press and ends up in the Switch settings. Because there were frequent cases where this would happen.
- There's also been frequent cases where the OBS within the virtual machine would freeze the game capture. To try to circumvent this occuring I included in the script to close and reopen OBS everytime before checking Kyogre's color (since thats the only time where we must show the game on screen)
- There were times where when I started OBS through the script, OBS would open in a different spot. To make OBS open in the same corner, I installed gnome-tweaks through apt then executed `gsettings set org.gnome.mutter center-new-windows true`
- I double pressed every button in the script to make sure a button press doesn't miss, avoiding a potential loop.
- In case the loading times change in future updates, my BD was running version 1.1.1
