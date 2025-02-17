Rails.application.routes.draw do
  # resources :questions
  # resources :hosts
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Reveal health status on /up that returns 200 if the app boots with no exceptions, otherwise 500.
  # Can be used by load balancers and uptime monitors to verify that the app is live.
  # get "up" => "rails/health#show", as: :rails_health_check

  post "dhcp/search-from-client-data", to: "hosts#search_dhcp"
  post "dhcp/search-from-ip", to: "hosts#search_dhcp_ip"
  post "dhcp/set", to: "hosts#create_update"
  post "dhcp/erase", to: "hosts#destroy"

  post "dns/search-host", to: "hosts#search_dns_host"
  post "dns/search-ip", to: "hosts#search_dns_ip"
  post "dns/search-cache", to: "questions#search"
  post "dns/set", to: "questions#create_update"

  post "get-settings/soa", to: "settings#get_soa"
  # Defines the root path route ("/")
  # root "posts#index"
end
