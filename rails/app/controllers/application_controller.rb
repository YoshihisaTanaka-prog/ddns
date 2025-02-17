class MySetting
  ATTRIBUTE_NAMES = [:serial].freeze
  attr_accessor *ATTRIBUTE_NAMES

  def initialize(hash_data)
    default_serial = Time.current.strftime('%Y%m%d01').to_i
    if hash_data[:serial].nil?
      @serial = default_serial
    elsif hash_data[:serial] < default_serial
      @serial = default_serial
    else
      @serial = hash_data[:serial]
    end
  end

  def update_data(hash_data)
    if hash_data[:serial] == true
      self.serial = self.serial + 1
    end
    File.write(Rails.root.join("server-data.json"), JSON.pretty_generate(self.to_hash))
  end

  def to_hash
    ATTRIBUTE_NAMES.inject({}) do |hash, attribute_name|
      hash.merge({ attribute_name => send(attribute_name) })
    end
  end
end

class ApplicationController < ActionController::API
  def load_settings
    hash_data = JSON.load_file!(Rails.root.join("server-data.json"), symbolize_names: true) rescue {}
    @settings = MySetting.new(hash_data)
  end
  
  def update_settings(hash_data)
    load_settings()
    @settings.update_data(hash_data)
  end
end
