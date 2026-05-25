defmodule SwampWeb.ContactController do
  use SwampWeb, :controller

  def index(conn, _params) do
    render(conn, :contact)
  end

  def create(conn, _params) do
    render(conn, :confirm)
  end
end
