class Host < ApplicationRecord
  validates :client_id, uniqueness: { message: "must be unique" }, if: -> { client_id.present? }
  attr_accessor :ttl
  before_create :set_time_limit

  private
    def set_time_limit
      self.time_limit = Time.current + ttl.seconds if ttl.present?
    end
end
