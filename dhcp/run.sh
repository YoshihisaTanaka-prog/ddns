#!/usr/bin/bash

cd $(dirname $0)

run(){
  all_modules=(scapy)
  mapfile -t installed_modules < <(pip list | grep -Ev "^Package" | grep -Ev "^--" | grep -Ev "^pip " | awk '{print $1}')

  needed_modules=()
  for module in "${all_modules[@]}"; do
    needed_modules+=$module
  done

  install_command="pip install"
  for module in "${needed_modules[@]}"; do
    install_command+=" $module"
  done

  bash -c "$install_command"

  python main.py
}

run

sleep infinity