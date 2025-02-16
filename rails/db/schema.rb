# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[8.0].define(version: 2025_02_15_030512) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "pg_catalog.plpgsql"

  create_table "hosts", force: :cascade do |t|
    t.string "hostname", null: false
    t.string "mac_address", null: false
    t.string "client_id"
    t.string "ipv4"
    t.datetime "time_limit", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["hostname"], name: "index_hosts_on_hostname", unique: true
    t.index ["mac_address"], name: "index_hosts_on_mac_address", unique: true
  end

  create_table "questions", force: :cascade do |t|
    t.string "domain"
    t.integer "record_type"
    t.integer "record_class"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "questions_s_o_as", id: false, force: :cascade do |t|
    t.bigint "question_id", null: false
    t.bigint "s_o_a_id", null: false
    t.index ["question_id", "s_o_a_id"], name: "index_questions_s_o_as_on_question_id_and_s_o_a_id"
    t.index ["s_o_a_id", "question_id"], name: "index_questions_s_o_as_on_s_o_a_id_and_question_id"
  end

  create_table "s_o_as", force: :cascade do |t|
    t.string "primary"
    t.string "admin"
    t.string "value"
    t.datetime "time_limit", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "zones", force: :cascade do |t|
    t.bigint "question_id", null: false
    t.string "value"
    t.datetime "time_limit", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["question_id"], name: "index_zones_on_question_id"
  end

  add_foreign_key "zones", "questions"
end
