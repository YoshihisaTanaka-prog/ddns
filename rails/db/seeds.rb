# This file should ensure the existence of records required to run the application in every environment (production,
# development, test). The code here should be idempotent so that it can be executed at any point in every environment.
# The data can then be loaded with the bin/rails db:seed command (or created alongside the database with db:setup).
#
# Example:
#
#   ["Action", "Comedy", "Drama", "Horror"].each do |genre_name|
#     MovieGenre.find_or_create_by!(name: genre_name)
#   end
Host.create(hostname: "router", mac_address: "bc:24:11:ae:15:4f", ip_address: "192.168.4.1", time_limit: Time.current + 24.hour)
# Host.create(hostname: "router", mac_address: "bc:24:11:ae:15:4f", ip_address: "192.168.4.1")
Host.create(hostname: "mac", mac_address: "a4:fc:14:08:b9:48", ip_address: "192.168.4.3", time_limit: Time.current + 24.hour)