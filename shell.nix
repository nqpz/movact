# Use this file with nix-shell or similar tools; see https://nixos.org/
with import <nixpkgs> {};

mkShell {
  buildInputs = [ (python2.withPackages (ps: [ ps.pygtk ])) ];
}
