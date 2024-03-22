# See: https://github.com/NixOS/nixpkgs/blob/a1dd0c78411c35b96eff808aca25983b26763cea/pkgs/development/libraries/gstreamer/rs/default.nix
{
  lib,
  stdenv,
  fetchFromGitLab,
  fetchpatch,
  rustPlatform,
  meson,
  ninja,
  python3,
  pkg-config,
  rustc,
  cargo,
  cargo-c,
  nasm,
  gst_all_1,
  openssl,
  nix-update-script,
}: let
  # TODO: figure out what must be done about this upstream - related lu-zero/cargo-c#323 lu-zero/cargo-c#138
  cargo-c' = (cargo-c.__spliced.buildHost or cargo-c).overrideAttrs (oldAttrs: {
    patches =
      (oldAttrs.patches or [])
      ++ [
        (fetchpatch {
          name = "cargo-c-test-rlib-fix.patch";
          url = "https://github.com/lu-zero/cargo-c/commit/8421f2da07cd066d2ae8afbb027760f76dc9ee6c.diff";
          hash = "sha256-eZSR4DKSbS5HPpb9Kw8mM2ZWg7Y92gZQcaXUEu1WNj0=";
          revert = true;
        })
      ];
  });
in
  stdenv.mkDerivation rec {
    pname = "gstreamer-plugins-rs";
    version = "0.12.3";

    outputs = ["out" "dev"];

    src = fetchFromGitLab {
      domain = "gitlab.freedesktop.org";
      owner = "gstreamer";
      repo = "gst-plugins-rs";
      rev = version;
      hash = "sha256-bP9BmfkRc1QCiv3UD/79qiihtp/Mmh1WE14yu9pYmCs=";
    };

    cargoDeps = rustPlatform.importCargoLock {
      lockFile = ./Cargo.lock;
      outputHashes = {
        "cairo-rs-0.19.3" = "sha256-wwT1tEtQ6jJfhGG4/8C/su7mTvu0LzzCIJr7EuuviFM=";
        "ffv1-0.0.0" = "sha256-af2VD00tMf/hkfvrtGrHTjVJqbl+VVpLaR0Ry+2niJE=";
        "flavors-0.2.0" = "sha256-zBa0X75lXnASDBam9Kk6w7K7xuH9fP6rmjWZBUB5hxk=";
        "gdk4-0.8.1" = "sha256-VPmegFZ/bC8x1vkl3YU208jQ8FCEKLwe6ZDatz4mIvM=";
        "gstreamer-0.22.3" = "sha256-Sj98DoW2aj1C9OC1m2ce1ByBUuIOjYDzQG8QHAyEPzA=";
      };
    };

    strictDeps = true;

    nativeBuildInputs = [
      rustPlatform.cargoSetupHook
      meson
      ninja
      python3
      python3.pkgs.tomli
      pkg-config
      rustc
      cargo
      cargo-c'
      nasm
    ];

    buildInputs = [
      gst_all_1.gstreamer
      gst_all_1.gst-plugins-base
      gst_all_1.gst-plugins-bad
      openssl
    ];

    checkInputs = [
      gst_all_1.gst-plugins-good
      gst_all_1.gst-plugins-bad
    ];

    mesonFlags = [
      (lib.mesonEnable "rtp" true)
      (lib.mesonEnable "webrtc" true)
    ];

    # turn off all auto plugins since we use a list of plugins we generate
    mesonAutoFeatures = "disabled";

    doCheck = true;

    preConfigure =
      ''
        export CARGO_BUILD_JOBS=$NIX_BUILD_CORES

        patchShebangs dependencies.py
      ''
      + lib.optionalString (!gst_all_1.gst-plugins-base.glEnabled) ''
        sed -i "/\['gstreamer-gl-1\.0', 'gst-plugins-base', 'gst_gl_dep', 'gstgl'\]/d" meson.build
      '';

    # run tests ourselves to avoid meson timing out by default
    checkPhase = ''
      runHook preCheck

      meson test --no-rebuild --verbose --timeout-multiplier 12

      runHook postCheck
    '';

    installCheckPhase = ''
      runHook preInstallCheck
      readelf -a $out/lib/gstreamer-1.0/libgstrswebp.so | grep -F 'Shared library: [libwebpdemux.so'
      runHook postInstallCheck
    '';

    passthru.updateScript = nix-update-script {
      # use numbered releases rather than gstreamer-* releases
      extraArgs = ["--version-regex" "([0-9.]+)"];
    };
  }
