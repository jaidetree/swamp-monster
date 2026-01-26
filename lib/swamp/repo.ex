defmodule Swamp.Repo do
  use Ecto.Repo,
    otp_app: :swamp,
    adapter: Ecto.Adapters.Postgres
end
