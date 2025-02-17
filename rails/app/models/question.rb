class Question < ApplicationRecord
  has_many :question_soa_relations
  has_many :soas, through: :question_soa_relations
  has_many :zones
end
