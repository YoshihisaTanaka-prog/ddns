class CreateHosts < ActiveRecord::Migration[8.0]
  def change
    create_table :hosts do |t|
      t.string :hostname, null: false
      t.string :mac_address, null: false
      t.string :client_id
      t.string :ipv4
      t.datetime :time_limit, null: false

      t.timestamps
    end

    add_index :hosts, :hostname, unique: true
    add_index :hosts, :mac_address, unique: true
  end
end
