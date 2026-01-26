defmodule SwampWeb.PageController do
  use SwampWeb, :controller

  def home(conn, _params) do
    render(conn, :home)
  end
end
