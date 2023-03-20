# MacTextOnDesktopWallpaper
A simple script to display text on the image of the wallpaper, on macos. MacOs port of https://askubuntu.com/a/556769 from ubuntu

Follow theses steps to have it run on startup:


    Create a text file containing your commands (bash script):

    #!/bin/bash

    #start auto wallpaper update  script
    python3 <path/to/folder>/walltext.py

    Save this file in ~/Library/autoWallLaunch.cmd
    Make it executable: chmod +x ~/Library/autoWallLaunch.cmd
    Add this file in System Preferences > Accounts > Login items


