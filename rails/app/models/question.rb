class Question < ApplicationRecord
  has_and_belongs_to_many :s_o_as
  has_many :zones
end
