class CreateSoas < ActiveRecord::Migration[8.0]
  def change
    create_table :soas do |t|
      t.string :primary
      t.string :admin
      t.string :value
      t.datetime :time_limit, null: false

      t.timestamps
    end
  end
end
