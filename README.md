![](https://github.com/nick16/Pokemon-BDSP-Kyogre-Shiny-Hunting-Bot/blob/main/images/kyogre.gif)

# Pokemon BDSP Ramanas Park Kyogre Shiny Hunting Bot
This script is an edited version of run_controller_cli.py script from https://github.com/mart1nro/joycontrol. In order for this script to run you must download the joycontrol repository by mart1nro, and replace mart1nro's run_controller_cli.py with this one, and add this shiny_hunter.py into the same folder.

This script was created for shiny hunting the pokemon Kyogre from Ramanas Park in BD/SP on the Nintendo Switch.
This script is easily customizable, so feel free to customize to shiny hunt any pokemon!

![](https://github.com/nick16/Pokemon-BDSP-Kyogre-Shiny-Hunting-Bot/blob/main/images/shiny_kyogre_encounter.PNG)

# Setup
## What You Need
- **Ubuntu OS** (A virtual machine is preferred)
- A **video capture device** to capture the input from the docked Nintendo Switch to your PC (I used Elgato's Game Capture Hd60 Pro)
- A **USB Bluetooth Adapter** for your pc (Internal BT adapters may work if Ubuntu is your native OS, otherwise it must be a USB Bluetooth adapter for the virtual machine to use Bluetooth) (I used Asus USB-BT500)


## Setting up the Bot
This bot works by checking a single pixel on screen at a precise (x,y) to check whether Kyogre is shiny or not. This precise (x,y) is based off of OBS being in the most top left of the screen, and Kyogre being at a precise coordinate at the right time (by calculated sleep functions).

###  1) Install Ubuntu
   I used a virtual machine of Ubuntu 20.04.4 LTS inside of VirtualBox. Thw Windowing System of the OS must be X11 for the screen capturing functions to work.
   If you use a virtual machine make sure USB 3.0 is selected in the USB options, so that the video input in OBS does not stutter.

### 2) Getting the emulated controller to connect to your switch
   Download and extract [mart1nro's repository](https://github.com/mart1nro/joycontrol) into a folder in your Ubuntu OS.

   Follow mart1nro's README to get the emulated controller to connect to your switch inside of your Ubuntu OS (Since his script apparently only works on certain Linux distros).
    
   Some hurdles I came across when trying to get the emulated controller connect to my switch:
   - mart1nro's script uses a function deprecated in the latest version of the module hid, so when installing hid I forced version 1.0.0 `pip3 install hid==1.0.0`
   - When I executed the script, it said I was missing modules I had installed, so my workaround was to install modules and run the script inside a virtual environment.
   - mart1nro's script relies on Bluetooth to connect the emulated controller to your Switch, so if you are using VirtualBox connect to your USB BT adapter by:
        1. Install VirtualBox's Guest Additions to enable USB access in the VM.
        2. Unplug the USB BT adapter from your PC.
        3. Within the virtual machine, plug in your USB BT adapter into your pc, and connect to the BT adapter (Devices > USB).
   - When you run mart1nro's script, it helps if you don't have any controller connected to the switch (doc your switch and don't have any connected controllers)
    
   Once you've gotten the controller to connect to your switch and you've played around controlling your switch through the terminal to ensure you've done things right, drag the two files from this repo [run_controller_cli.py, shiny_hunter.py] into that same folder (replacing his run_controller_cli.py)

### 3) Setup Game Capture in Ubuntu
   We need to bring the game into Ubuntu so that we can check if the pokemon is shiny.
    I accomplished this in the virtual machine by downloading OBS and adding a Video Capture Device Source. You must also select your capture device under Devices > Webcam in VirtualBox settings.
    Now make sure OBS is kept at the default window size and move it to the top left of the screen (not bypassing the doc).

### 4) Done
   Make sure you have a save right in front of Kyogre, quit the game, and are hovering over Pokemon BD/SP, then start the script!


# Tips:
- I created a stuck() function that gets executed right before we check the color of the pokemon, in the cases where the controller somehow misses a button press and ends up in the Switch settings. Because there were frequent cases where this would happen.
- There's also been frequent cases where the OBS within the virtual machine would freeze the game capture. To try to circumvent this from occurring, I included in the script to close and reopen OBS every time before checking Kyogre's color (since that's the only time where we must show the game on screen)
- There were times where when OBS would open through the script, OBS would open in a different spot. To make OBS open in the same corner, I installed gnome-tweaks through apt then executed `gsettings set org.gnome.mutter center-new-windows true`. But this didn't work 100% of the time. So your best bet is once OBS opens in any one spot consistently, use the getmouselocation script in the first tip, to choose the pixel on the pokemon you want to check if shiny.
- I double pressed every button in the script to make sure a button press doesn't miss, avoiding a potential loop.
- In case the game loading times change in future updates, my BD was running version 1.1.1
- Use a non shiny pokemon in your encounter with Kyogre. If you must use a shiny in your encounter, then add 3.1 seconds to the sleep timer on line 98 in run_controller_cli.py to compensate for your pokemons shiny animation.
- If the pokemon you're shiny hunting moves too much to check a consistent part of the pokemon, another method rather than checking the color of a single pixel is checking the average color of a group of pixels.

## How to Customize for Another Pokemon
   If you would like to use this script to shiny hunt another pokemon that requires a soft game reset, then you should have to only change 2 things.
1. In the shiny function within shiny_hunter.py, you would change the range of colors that determines if the pokemon is shiny, to a spectrum of colors of the shiny pokemon you're shiny hunting.
   What I did for Kyogre was that I googled images and videos of shiny Kyogre then used the Eyedropper Tool in Photoshop to get the RGB values from those images/videos. With those different RGB values, I found the minimum and maximum value for each R,G,B and made a range from those values.
3. On line 100 in the run_controller_cli.py, you would have to change the (x,y) on-screen coordinates to be the pixel over your pokemon you'll be checking the color of.
   How I figured out the best x,y coordinates to check if Kyogre is shiny is finding where Kyogre is still for the longest, and grabbed the x,y coordinated on that spot by using the command `xdotool getmouselocation --shell` with my cursor on the spot I wanted to grab.
   
  If you would like to use this script to shiny hunt a pokemon that involves running around or a longer dialogue, then you would have to add button presses and sleep functions to the shiny_hunt() function on line 32 in run_controller_cli.py
