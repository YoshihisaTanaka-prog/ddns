class Soa < ApplicationRecord
  has_many :question_soa_relations
  has_many :questions, through: :question_soa_relations
end
