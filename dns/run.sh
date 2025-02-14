#!/usr/bin/bash

cd $(dirname $0)

# run(){
#   all_modules=(dnslib)
#   mapfile -t installed_modules < <(pip list | grep -Ev "^Package" | grep -Ev "^--" | grep -Ev "^pip " | awk '{print $1}')

#   needed_modules=()
#   for module in "${all_modules[@]}"; do
#     printf "%s\n" "${installed_modules[@]}" | grep -qx "$module"
#     if ! printf "%s\n" "${installed_modules[@]}" | grep -qx "$module"; then
#       needed_modules+=$module
#     fi
#   done

#   if [ ${#needed_modules[@]} -gt 0 ]; then
#     install_command="pip install"
#     for module in "${needed_modules[@]}"; do
#       install_command+=" $module"
#     done
#     bash -c "$install_command"
#   fi

#   python main.py
# }

# run

sleep infinity