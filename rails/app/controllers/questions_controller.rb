class QuestionsController < ApplicationController
  def search
    ApplicationRecord.transaction do
      @question = Question.find_by(question_params)
      unless @question.nil?
        @s_o_as = @question.soas
        @zones = @question.zones
        now = Time.current
        @invalid_count = 0
        @s_o_as.select do |s_o_a|
          s_o_a.time_limit < now
        end.each do |s_o_a|
          s_o_a.destroy!
          @invalid_count = @invalid_count + 1
        end
        @zones.select do |zone|
          zone.time_limit < now
        end.each do |zone|
          zone.destroy!
          @invalid_count = @invalid_count + 1
        end
      end
    end
    if @question.nil?
      render json: nil
    elsif @invalid_count == 0
      if @zones.empty? && @s_o_as.empty?
        render json: nil
      else
        zones = @zones.map do |z|
          z.output_format(@question.domain)
        end
        s_o_as = @s_o_as.map do |s|
          s.value
        end
        render json: {zones: zones, s_o_as: s_o_as }
      end
    else
      render json: nil
    end
  rescue ApplicationRecord::RecordInvalid => e
    render json: { error: e.message }, status: 500
  end

  # POST /questions
  def create_update
    ApplicationRecord.transaction do
      qp = question_params
      @question = Question.find_or_create_by(question_params)
      now = Time.current
      s_o_as_params.each do |s|
        @question.soas.find_or_create_by(primary: s[:primary], admin: s[:admin]) do |soa|
          soa.value = s[:value]
          soa.time_limit = now + s[:ttl].seconds
        end
      end
      zones_params.each do |z|
        @question.zones.find_or_create_by(value: z[:value]) do |zone|
          zone.time_limit = now + z[:ttl].seconds
        end
      end
    end
    render json: {}, status: 200
  rescue ActiveRecord::RecordInvalid => e
    render json: { error: e.message }, status: 422
  end

  private
    # Only allow a list of trusted parameters through.
    def question_params
      params.expect(question: [ :domain, :record_type, :record_class ])
    end

    def s_o_as_params
      if params[:s_o_as].nil?
        raise ActionController::ParameterMissing.new("s_o_as")
      elsif params[:s_o_as].instance_of?(Array)
        if params[:s_o_as].empty?
          []
        else
          params[:s_o_as].map.with_index do |s, index|
            s.permit(:primary, :admin, :value, :ttl)
          end
        end
      else
        raise ActionController::ParameterMissing.new("s_o_as")
      end
    end
    
    def zones_params
      if params[:zones].nil?
        raise ActionController::ParameterMissing.new("zones")
      elsif params[:zones].instance_of?(Array)
        if params[:zones].empty?
          []
        else
          params[:zones].map.with_index do |z, index|
            z.permit(:value, :ttl)
          end
        end
      else
        raise ActionController::ParameterMissing.new("zones")
      end
    end
end
