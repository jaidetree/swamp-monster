defmodule SwampWeb.ContactHTML do
  @moduledoc """
  This module contains pages rendered by ContactController.

  See the `page_html` directory for all templates available.
  """
  use SwampWeb, :html

  embed_templates "page_html/*"
end
