class CreateJoinTableQuestionSoa < ActiveRecord::Migration[8.0]
  def change
    create_join_table :questions, :s_o_as do |t|
      t.index [:question_id, :s_o_a_id]
      t.index [:s_o_a_id, :question_id]
    end
  end
end
