class CreateSOAs < ActiveRecord::Migration[8.0]
  def change
    create_table :s_o_as do |t|
      t.string :primary
      t.string :admin
      t.string :value
      t.datetime :time_limit, null: false

      t.timestamps
    end
  end
end
