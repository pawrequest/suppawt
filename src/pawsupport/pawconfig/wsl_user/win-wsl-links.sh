#!/bin/bash

create_symlink() {
    local target=$1
    local link_name=$2

    if [ -L "$link_name" ] || [ -e "$link_name" ]; then
        echo "Skipping $link_name: already exists."
    else
        if ln -s "$target" "$link_name"; then
            echo "Created symlink for $target at $link_name."
        else
            echo "Failed to create symlink for $target at $link_name."
        fi
    fi
}

# create_symlink "/mnt/c/Users/RYZEN/.gitconfig" ".gitconfig"
create_symlink "/mnt/c/Users/RYZEN/.config" "$HOME/.config"
create_symlink "/mnt/c/Users/RYZEN/prdev" "$HOME/prdev"
