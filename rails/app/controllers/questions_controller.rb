class QuestionsController < ApplicationController
  def search
    ApplicationRecord.transaction do
      @question = Question.find_by(question_params)
      unless @question.nil?
        @s_o_as = @question.s_o_as
        @zones = @question.zones
        now = Time.current
        @invalid_count = 0
        @s_o_as.select do |s_o_a|
          s_o_a.time_limit < now
        end.each do |s_o_a|
          s_o_a.destroy!
        end
        @zones.select do |zone|
          zone.time_limit < now
        end.each do |zone|
          zone.destroy!
        end
      end
    end
    if @question.nil?
      render json: nil
    elsif @invalid_count == 0
      render json: {zones: @zones, s_o_as: @s_o_as }
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
      @question = Question.find__or_create_by(question_params)
      s_o_as_params.each do |s|
        @question.s_o_as.find_or_create_by(primary: s[:primary], admin: s[:admin]) do |s_o_a|
          s_o_a.value = s[:value]
          s_o_a.ttl = s[:ttl]
        end
      end
      zones_params.each do |z|
        @question.zones.find_or_create_by(value: z[:value], ttl: z[:ttl])
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
      params.require(:s_o_as).map do |s|
        s.permit(:primary, :admin, :value, :ttl)
      end
    end
    
    def zones_params
      params.require(:zones).map do |z|
        z.permit(:value, :ttl)
      end
    end
end
