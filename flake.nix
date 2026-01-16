{
  description = "Deskhop firmware";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }: let
    forAllSystems = nixpkgs.lib.genAttrs [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
  in {
    packages = forAllSystems(system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in rec {
        deskhop-webconfig = pkgs.stdenv.mkDerivation {
          name = "deskhop-webconfig";

          src = ./webconfig;

          nativeBuildInputs = with pkgs; [
            (python3.withPackages(pp: [pp.jinja2]))
          ];

          installPhase = ''
            cp config.htm $out
          '';
        };

        deskhop-diskimg = pkgs.stdenv.mkDerivation {
          name = "deskhop-diskimg";

          src = ./disk;

          nativeBuildInputs = with pkgs; [
            dosfstools
            (python3.withPackages(pp: [pp.fs pp.pyfatfs]))
          ];

          buildPhase = ''
            python3 create.py disk.img ${deskhop-webconfig}
          '';

          installPhase = ''
            cp disk.img $out
          '';

          dontFixup = true;
        };

        deskhop-firmware = pkgs.stdenv.mkDerivation {
          name = "deskhop-firmware";

          src = ./.;

          buildInputs = with pkgs; [
            cmake
            gcc-arm-embedded
            newlib
            python3
          ];

          configurePhase = ''
            ln -sf ${deskhop-diskimg} disk/disk.img
            cmake -S . -B build
          '';

          buildPhase = ''
            cmake --build build
          '';

          installPhase = ''
            mkdir $out
            cp build/deskhop.uf2 $out/
          '';

          dontFixup = true;
        };

        default = deskhop-firmware;
    });
  };
}
