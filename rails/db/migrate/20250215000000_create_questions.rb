class CreateQuestions < ActiveRecord::Migration[8.0]
  def change
    create_table :questions do |t|
      t.string :domain
      t.integer :record_type
      t.integer :record_class

      t.timestamps
    end
  end
end
