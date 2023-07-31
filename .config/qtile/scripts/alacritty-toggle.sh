#!/bin/bash

# Define the directory containing the Alacritty config files
CONFIG_DIRECTORY="$HOME/.config/alacritty"

# Define the names of your two Alacritty config files
ALACRITTY_CONFIG_1="alacritty.yml"
ALACRITTY_CONFIG_2="grey-alacritty.yml"

# Find all the config files in the directory (recursively)
config_files=($(find "$CONFIG_DIRECTORY" -type f -name "$ALACRITTY_CONFIG_1" -o -name "$ALACRITTY_CONFIG_2"))

# Function to switch the Alacritty config file
switch_config() {
  for config_file in "${config_files[@]}"; do
    if [ "$config_file" = "$1" ]; then
      mv "$1" "${1}.backup"
      cp "$2" "$1"
      echo "Switched $1 to $2"
    fi
  done
}

# Check if the current config is config 1 or config 2, then switch to the other one
for config_file in "${config_files[@]}"; do
  if [ -f "$config_file" ]; then
    if grep -q "$ALACRITTY_CONFIG_1" "$config_file"; then
      switch_config "$config_file" "$CONFIG_DIRECTORY/$ALACRITTY_CONFIG_2"
    elif grep -q "$ALACRITTY_CONFIG_2" "$config_file"; then
      switch_config "$config_file" "$CONFIG_DIRECTORY/$ALACRITTY_CONFIG_1"
    fi
  fi
done




