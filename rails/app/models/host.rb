class Host < ApplicationRecord
  validates :hostname, uniqueness: { message: "must be unique" }, if: -> { hostname.present? }

  def client_info
    return {mac_address: self.mac_address, client_id: self.client_id, ip_address: self.ip_address}
  end
end
