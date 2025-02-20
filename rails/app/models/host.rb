class Host < ApplicationRecord
  validates :hostname, uniqueness: { message: "must be unique" }, if: -> { hostname.present? }
  validates :ip_v4, uniqueness: { message: "must be unique" }, if: -> { ip_v4.present? }
  validates :ip_v6, uniqueness: { message: "must be unique" }, if: -> { ip_v6.present? }

  def client_info
    return {mac_address: self.mac_address, client_id: self.client_id, ip_v4: self.ip_v4}
  end
end
