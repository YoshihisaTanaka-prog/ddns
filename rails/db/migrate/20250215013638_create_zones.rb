class CreateZones < ActiveRecord::Migration[8.0]
  def change
    create_table :zones do |t|
      t.references :question, null: false, foreign_key: true
      t.string :value1
      t.string :value2
      t.datetime :time_limit, null: false

      t.timestamps
    end
  end
end
