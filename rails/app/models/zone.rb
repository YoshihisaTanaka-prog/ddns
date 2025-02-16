class Zone < ApplicationRecord
  belongs_to :question

  def output_format(domain)
    "#{domain} #{(self.time_limit - Time.now).to_i} #{self.value}"
  end
end
