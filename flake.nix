{
  description = "Swamp Monster Leather";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            elixir
            erlang
            lexical

            nodejs_24

            # PostgreSQL
            postgresql_18
            pgcli
            postgresql_18.lib
            openssl
          ];

          # Shell hook for additional environment setup
          shellHook = ''
            echo "Elixir development environment loaded!"
            echo "Elixir version: $(elixir --version)"
            echo "Postgres version: $(postgres --version)"
          '';
        };
      }
    );
}
