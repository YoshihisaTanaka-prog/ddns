class Host < ApplicationRecord
  validates :client_id, uniqueness: { message: "must be unique" }, if: -> { client_id.present? }
end
