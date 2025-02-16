class QuestionSoaRelation < ApplicationRecord
  belongs_to :question
  belongs_to :soa
end
