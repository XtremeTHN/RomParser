{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    {
      self,
      nixpkgs,
    }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      python = (pkgs.python314.withPackages (ps: with ps; [
        colorama
        cryptography
        hatchling
      ]));
      

      buildInputs = [
        python
      ];
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        inherit buildInputs;
        packages = with pkgs; [
          ruff
          hactool
          ghex
        ];
      };

      packages.${system}.default = python.pkgs.buildPythonPackage {
        pname = "nxroms";
        version = "0.1.0";
        src = ./.;
        
        format = "pyproject";

        nativeBuildInputs = with python.pkgs; [
          hatchling
        ];

        propagatedBuildInputs = with python.pkgs; [
          cryptography
        ];

        pythonImportsCheck = [ "nxroms" ];
      };
    };
}
