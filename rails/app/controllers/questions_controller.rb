class QuestionsController < ApplicationController
  def search
    @now = Time.current
    ApplicationRecord.transaction do
      @question = Question.find_by(question_params)
      unless @question.nil?
        @s_o_as = @question.soas
        @zones = @question.zones
        @invalid_count = 0
        @s_o_as.select do |s_o_a|
          s_o_a.time_limit < @now
        end.each do |s_o_a|
          @invalid_count = @invalid_count + 1
        end
        @zones.select do |zone|
          zone.time_limit < @now
        end.each do |zone|
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
          z.output_format
        end
        s_o_as = @s_o_as.map do |s|
          s.value
        end
        render json: {zones: zones, s_o_as: s_o_as }
      end
    else
      render json: nil
    end
  rescue => e
    render json: { error: e.message }, status: 500
  end

  # POST /questions
  def create_update
    ApplicationRecord.transaction do
      qp = question_params
      @question = Question.find_or_create_by(question_params)
      now = Time.current
      soa_ids = []
      s_o_as_params.each do |s|
        soa = @question.soas.find_or_initialize_by(primary: s[:primary], admin: s[:admin])
        soa.value =  s[:value]
        soa.time_limit = now + s[:ttl].seconds
        soa.save
        soa_ids << soa.id
      end
      @question.soas.each do |s|
        unless soa_ids.include?(s.id)
          qsr = QuestionSoaRelation.find_by(question_id: @question.id, soa_id: s.id)
          unless qsr.nil?
            qsr.delete
          end
        end
      end
      zone_ids = []
      zones_params.each do |z|
        zone = @question.zones.find_or_initialize_by(value1: z[:value1], value2: z[:value2])
        zone.time_limit = now + z[:ttl].seconds
        zone.save
        zone_ids << zone.id
      end
      @question.zones.each do |z|
        unless zone_ids.include?(z.id)
          z.delete
        end
      end
    end
    render json: {}, status: 200
  rescue => e
    render json: { error: e.message }, status: 500
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
            z.permit(:value1, :value2, :ttl)
          end
        end
      else
        raise ActionController::ParameterMissing.new("zones")
      end
    end
end
