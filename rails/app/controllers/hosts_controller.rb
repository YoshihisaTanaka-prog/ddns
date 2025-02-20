class HostsController < ApplicationController
  def search_dns_host
    if params[:ip_domain].nil?
      raise ActionController::ParameterMissing.new("ip_domain")
    else
      ips = params[:ip_domain].split(".")
      ip_address = [ips[3], ips[2], ips[1], ips[0]].join(".")
      host = Host.find_by(ip_v4: ip_address)
      if host.nil?
        render json: nil
      elsif host.time_limit.nil? # fixed ip
        render json: host.hostname.to_json
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
        render json: {ip_v4: nil, ip_v6: nil}
      elsif host.time_limit.nil? # fixed ip
        render json: {ip_v4: host.ip_v4, ip_v6: host.ip_v6}.to_json
      elsif host.time_limit < Time.current
        render json: {ip_v4: nil, ip_v6: nil}
      else
        render json: {ip_v4: host.ip_v4, ip_v6: host.ip_v6}.to_json
      end
    end
  end

  def search_dhcp_ip
    if params.dig(:host, :ip_address).nil?
      raise ActionController::ParameterMissing.new("host[:ip_address]")
    else
      host = Host.find_by(ip_v4: params.dig(:host, :ip_address))
      logger.info host
      if host.nil?
        render json: nil
      elsif host.time_limit.nil? # fixed ip
        render json: host.client_info
      elsif host.time_limit < Time.current
        render json: nil
      else
        render json: host.client_info
      end
    end
  end

  def search_dhcp
    host = Host.find_by(searching_host_params)
    if host.nil?
      render json: {ip_v4: nil, ip_v6: nil}
    elsif host.time_limit.nil? # fixed ip
      render json: {ip_v4: host.ip_v4, ip_v6: host.ip_v6}.to_json
    elsif host.time_limit < Time.current
      render json: {ip_v4: nil, ip_v6: nil}
    else
      render json: {ip_v4: host.ip_v4, ip_v6: host.ip_v6}.to_json
    end
  end

  def create_update_v4
    create_update("IPv4")
  end

  def create_update_v6
    create_update("IPv6")
  end

  def fix
    host = Host.find_or_initialize_by(searching_host_params)
  end
  
  def destroy
    host = Host.find_by(searching_host_params)
    if host.nil?
      render json: {}, status: 200
    elsif host.time_limit.nil?
      render json: {}, status: 200
    else
      host.time_limit = Time.current
      if host.save
        self.update_settings({serial: true})
        render json: {}, status: 200
      else
        render json: host.errors, status: :unprocessable_entity
      end
    end
  end

  private
    def create_update(mode)
      shp = searching_host_params
      uhp = updating_host_params
      host = Host.find_by(shp)
      if host.nil?
        host = Host.new(shp)
        if uhp[:ttl].nil?
          soa_data = JSON.parse(ENV.fetch("LOCAL_SOA"), symbolize_names: true)
          host.time_limit = Time.current + soa_data[:minimum].seconds
        else
          host.time_limit = Time.current + uhp[:ttl].seconds
        end
      else
        unless host.time_limit.nil?
          if uhp[:ttl].nil?
            ttl = host.time_limit - host.updated_at
            host.time_limit = Time.current + ttl
          else
            host.time_limit = Time.current + uhp[:ttl].seconds
          end
        end
      end
      host.hostname = uhp[:hostname]
      if mode == "IPv4"
        host.ip_v4 = uhp[:ip_address]
      else
        host.ip_v6 = uhp[:ip_address]
      end
      p host
      if host.save
        self.update_settings({serial: true})
        render json: {}
      else
        render json: host.errors, status: :unprocessable_entity
      end
    end

    def searching_host_params
      params.expect(host: [:mac_address, :client_id])
    end

    def updating_host_params
      params.expect(host: [:hostname, :ip_address, :ttl])
    end

    def fix_host_params
      p = params.expect(host: [:ip_address, :is_fixing])
      return {ip_address: p[:ip_address]}
    end
end
