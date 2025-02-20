class Zone < ApplicationRecord
  belongs_to :question

  def output_format
    ttl = (self.time_limit - Time.current).floor
    "#{self.value1} #{ttl} #{self.value2}"
  end
end
