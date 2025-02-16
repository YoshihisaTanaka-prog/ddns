class CreateQuestionSoaRelations < ActiveRecord::Migration[8.0]
  def change
    create_table :question_soa_relations do |t|
      t.references :question, null: false, foreign_key: true
      t.references :soa, null: false, foreign_key: true

      t.timestamps
    end
  end
end
