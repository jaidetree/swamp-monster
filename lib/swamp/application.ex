defmodule Swamp.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      SwampWeb.Telemetry,
      Swamp.Repo,
      {DNSCluster, query: Application.get_env(:swamp, :dns_cluster_query) || :ignore},
      {Phoenix.PubSub, name: Swamp.PubSub},
      # Start a worker by calling: Swamp.Worker.start_link(arg)
      # {Swamp.Worker, arg},
      # Start to serve requests, typically the last entry
      SwampWeb.Endpoint
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Swamp.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  @impl true
  def config_change(changed, _new, removed) do
    SwampWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
