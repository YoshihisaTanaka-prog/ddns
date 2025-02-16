class SettingsController < ApplicationController
  def get_soa
    load_settings()
    soa_data = JSON.parse(ENV.fetch("LOCAL_SOA"))
    soa_data[:serial] = @settings.serial
    render json: soa_data
  end
end
