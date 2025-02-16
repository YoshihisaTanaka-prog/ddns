class HostsController < ApplicationController
  before_action :set_host, only: %i[ create_update destroy ]

  def search_host
    ips = params[:ipv4].split(".")
    ipv4 = [ips[3], ips[2], ips[1], ips[0]].join(".")
    host = Host.find_by(ipv4: ipv4)
    if host.nil?
      render json: {answer: nil}
    elsif host.time_limit < Time.current
      render json: {answer: nil}
    else
      render json: {answer: host.hostname}
    end
  end

  def search_ipv4
    host = Host.find_by(hostname: params[:hostname])
    if host.nil?
      render json: {answer: nil}
    elsif host.time_limit < Time.current
      render json: {answer: nil}
    else
      render json: {answer: host.ipv4}
    end
  end

  def search_dhcp
    if params[:host].nil?
      if params[:ipv4].nil?
        render json: nil
      else
        render json: Host.where("ipv4 LIKE ?", "#{params[:ipv4]}%").map do |host|
          host.ipv4.split(".").map(&:to_i)
        end
      end
    else
      @host = Host.find_by(searching_host_params)
      render json: Host.find_by(searching_host_params)
    end
  end

  def search_dhcp_list
    render json: Host.where("ipv4 LIKE ?", "#{params[:ipv4]}%").map do |host|
      host.ipv4.split(".").map(&:to_i)
    end
  end

  def create_update
    @host = Host.find_or_create_by(searching_host_params)
    if @host.update(updating_host_params)
      self.update_settings({serial: true})
      render json: @host
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
      params.expect(host: [:hostname, :ipv4, :ttl])
    end
end
