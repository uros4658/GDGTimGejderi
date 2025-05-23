{
  description = "Description for the project";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [];
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" "x86_64-darwin" ];
      perSystem = { config, self', inputs', pkgs, system, ... }: {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            dbeaver-bin
              (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
                                          pandas
                                          numpy
                                          scikit-learn
                                          fastapi
                                          sqlalchemy
                                          psycopg2
                                          alembic
                                          pydantic
                                          python-dotenv
                                          bcrypt
                                          uvicorn
                                          pip
              ]))
            postgresql_17
            gcc
          ];
        };
      };
      flake = {
      };
    };
}
