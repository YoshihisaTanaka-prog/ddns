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

ActiveRecord::Schema[8.0].define(version: 2025_02_16_051503) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "pg_catalog.plpgsql"

  create_table "hosts", force: :cascade do |t|
    t.string "hostname", null: false
    t.string "mac_address", null: false
    t.string "client_id"
    t.string "ip_address", null: false
    t.datetime "time_limit", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["hostname"], name: "index_hosts_on_hostname", unique: true
    t.index ["ip_address"], name: "index_hosts_on_ip_address", unique: true
    t.index ["mac_address"], name: "index_hosts_on_mac_address", unique: true
  end

  create_table "question_soa_relations", force: :cascade do |t|
    t.bigint "question_id", null: false
    t.bigint "soa_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["question_id"], name: "index_question_soa_relations_on_question_id"
    t.index ["soa_id"], name: "index_question_soa_relations_on_soa_id"
  end

  create_table "questions", force: :cascade do |t|
    t.string "domain"
    t.integer "record_type"
    t.integer "record_class"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "soas", force: :cascade do |t|
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

  add_foreign_key "question_soa_relations", "questions"
  add_foreign_key "question_soa_relations", "soas"
  add_foreign_key "zones", "questions"
end
