#!/usr/bin/env bash
set -e

echo -e "\033[1;36m⚡ Installing GLO (Git Loop Operator)... \033[0m"

# Install python dependencies
if command -v pip3 &>/dev/null; then
    pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt
else
    pip install -r requirements.txt
fi

# Copy binary globally
sudo cp glo.py /usr/local/bin/glo
sudo chmod +x /usr/local/bin/glo
sudo ln -sf /usr/local/bin/glo /usr/local/bin/automategit

echo -e "\033[1;32m✔ Installation Complete!\033[0m"
echo -e "You can now run \033[1;33mglo\033[0m or \033[1;33mglo --stats\033[0m from any directory."
