let
  # Use a specific nixpkgs revision for potentially better stability
  # Find a recent stable commit hash on https://status.nixos.org/
  # Example: nixpkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/YOUR_CHOSEN_COMMIT_HASH.tar.gz") {};
  # Or use your current channel:
  pkgs = import <nixpkgs> {};

  # Use the specific Python package set
  pythonPackages = pkgs.python311Packages;

  obspyBuildDeps = [
    pkgs.libxml2.dev
    pkgs.libxslt.dev
    # Add other .dev packages if build errors mention missing headers
  ];

in
pkgs.mkShell {
  name = "obspy-dev-env"; # Optional: Add a name

  buildInputs = [
    # Core Python environment components from the 3.11 set
    pythonPackages.python
    pythonPackages.pip      # Good practice to include pip from the same set
    pythonPackages.setuptools # Use the setuptools matching the python

    # The uv tool itself
    pkgs.uv

    # Build Toolchain & Helpers
    pkgs.clang
    pkgs.pkg-config

    # Obspy's specific library dependencies
  ] ++ obspyBuildDeps;

  # Ensure uv uses the env python if PATH manipulation is tricky
  # (This might be redundant with the .envrc logic, but belts and suspenders)
  shellHook = ''
    export UV_PYTHON_EXECUTABLE="${pythonPackages.python.interpreter}"
    echo "--- Nix shell hook: Set UV_PYTHON_EXECUTABLE to ${pythonPackages.python.interpreter} ---"
  '';
}