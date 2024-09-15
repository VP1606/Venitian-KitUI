#!/bin/bash

# This script is used to update the kit
echo "HELLO from Kit-UPDATER"
echo " "

# # Quit UI Instance.
# echo "Quitting UI..."
# echo "Done."
# echo " "

# Pull from Git / update files.
echo "Pulling from Git..."
git pull
echo "Done."
echo " "

# # Restart UI Instance.
echo "Restarting UI..."
sudo systemctl restart venitian_ui.service
echo "Done."
echo " "

echo "Kit-Updater complete."