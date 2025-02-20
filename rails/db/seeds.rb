# This file should ensure the existence of records required to run the application in every environment (production,
# development, test). The code here should be idempotent so that it can be executed at any point in every environment.
# The data can then be loaded with the bin/rails db:seed command (or created alongside the database with db:setup).
#
# Example:
#
#   ["Action", "Comedy", "Drama", "Horror"].each do |genre_name|
#     MovieGenre.find_or_create_by!(name: genre_name)
#   end
Host.create(hostname: "router", mac_address: "bc:24:11:ae:15:4f", ip_v4: "192.168.4.1")
Host.create(hostname: "vpn", mac_address: "bc:24:11:9e:f9:f0", ip_v4: "192.168.4.2")
Host.create(hostname: "mac", mac_address: "a4:fc:14:08:b9:48", ip_v4: "192.168.4.3")
Host.create(hostname: "pve", mac_address: "84:e8:cb:7e:37:3e", ip_v4: "192.168.4.4")
Host.create(hostname: "WRC-X1500GS", mac_address: "38:97:a4:53:83:ac", ip_v4: "192.168.4.5")