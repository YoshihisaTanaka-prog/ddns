class HostsController < ApplicationController
  def search_dns_host
    if params[:ip_domain].nil?
      raise ActionController::ParameterMissing.new("ip_domain")
    else
      ips = params[:ip_domain].split(".")
      ip_address = [ips[3], ips[2], ips[1], ips[0]].join(".")
      host = Host.find_by(ip_address: ip_address)
      if host.nil?
        render json: nil
      elsif host.time_limit < Time.current
        render json: nil
      else
        render json: host.hostname.to_json
      end
    end
  end

  def search_dns_ip
    if params[:hostname].nil?
      raise ActionController::ParameterMissing.new("hostname")
    else
      host = Host.find_by(hostname: params[:hostname])
      if host.nil?
        render json: nil
      elsif host.time_limit < Time.current
        render json: nil
      else
        render json: host.ip_address.to_json
      end
    end
  end

  def search_dhcp_ip
    if params.dig(:host, :ip_address).nil?
      raise ActionController::ParameterMissing.new("host[:ip_address]")
    else
      host = Host.find_by(ip_address: params.dig(:host, :ip_address))
      logger.info host
      if host.nil?
        render json: false
      elsif host.time_limit < Time.current
        render json: false
      else
        render json: true
      end
    end
  end

  def search_dhcp
    @host = Host.find_by(searching_host_params)
    if @host.nil?
      render json: nil
    elsif @host.time_limit < Time.current
      render json: nil
    else
      render json: @host.ip_address.to_json
    end
  end

  def create_update
    hp = updating_host_params
    @is_creating = false
    @host = Host.find_or_create_by(searching_host_params) do |host|
      host.hostname = hp[:hostname]
      host.ip_address = hp[:ip_address]
      host.time_limit = hp[:time_limit]
      @is_creating = true
    end
    if @is_creating
      self.update_settings({serial: true})
      render json: {}
    elsif @host.update(hp)
      self.update_settings({serial: true})
      render json: {}
    else
      render json: @host.errors, status: :unprocessable_entity
    end
  end
  
  def destroy
    @host = Host.find_by(searching_host_params)
    if @host.nil?
      render json: {}, status: 200
    elsif @host.destroy
      self.update_settings({serial: true})
      render json: {}, status: 200
    else
      render json: @host.errors, status: :unprocessable_entity
    end
  end

  private
    def searching_host_params
      params.expect(host: [:mac_address, :client_id])
    end

    def updating_host_params
      p = params.expect(host: [:hostname, :ip_address, :ttl])
      if p[:ttl].nil?
        soa_data = JSON.parse(ENV.fetch("LOCAL_SOA"), symbolize_names: true)
        return {hostname: p[:hostname], ip_address: p[:ip_address], time_limit: Time.current + soa_data[:minimum].seconds}
      else
        return {hostname: p[:hostname], ip_address: p[:ip_address], time_limit: Time.current + p[:ttl].seconds}
      end
    end
end
