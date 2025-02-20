class CreateHosts < ActiveRecord::Migration[8.0]
  def change
    create_table :hosts do |t|
      t.string :hostname
      t.string :mac_address, null: false
      t.string :client_id
      t.string :ip_v6
      t.string :ip_v4
      t.datetime :time_limit

      t.timestamps
    end

    add_index :hosts, [:mac_address, :client_id], unique: true
  end
end
