#!/bin/bash
# Make the render gates runnable in a Claude Code on the web container.
#
# The core checks are stdlib-only and need nothing. Everything that RENDERS —
# validate_layout.py, visual_baseline.py, verify_rebuild.py, check_antipatterns.py,
# export_pdf.py — needs three things a fresh container does not have:
#
#   1. A CJK font. Without one, 繁中 slides fall back to a face with different
#      metrics, so fingerprints are not comparable with a macOS capture.
#   2. A Chromium that starts as root. The bundled binary refuses without
#      --no-sandbox, and scripts/validate_layout.py finds a browser by looking
#      for `chrome` on PATH, so a wrapper is the least invasive fix. It affects
#      only this throwaway container.
#   3. pypdf, for scripts/export_pdf.py.
#
# Idempotent: every step is skipped when already satisfied. Failures warn rather
# than abort, so a session still starts when the network is unavailable.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

FONT_DIR="$HOME/.local/share/fonts"
BIN_DIR="$HOME/.local/bin"
mkdir -p "$FONT_DIR" "$BIN_DIR"

# 1 - Noto Sans TC, the first face in --font-cjk
if fc-list :lang=zh-tw family 2>/dev/null | grep -qi "noto sans tc"; then
  echo "session-start: Noto Sans TC already present"
else
  echo "session-start: installing Noto Sans TC"
  for weight in 400 700; do
    url=$(curl -fsS -H "User-Agent: Mozilla/5.0" \
      "https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@${weight}" \
      | grep -oE 'https://fonts\.gstatic\.com/[^)]*\.ttf' | head -1) || url=""
    if [ -n "$url" ]; then
      curl -fsS -o "$FONT_DIR/NotoSansTC-${weight}.ttf" "$url" \
        || echo "session-start: WARNING download failed for weight ${weight}"
    else
      echo "session-start: WARNING could not resolve Noto Sans TC ${weight}; CJK metrics will differ"
    fi
  done
  fc-cache -f >/dev/null 2>&1 || true
fi

# 2 - a `chrome` on PATH that starts as root
if command -v chrome >/dev/null 2>&1; then
  echo "session-start: chrome already on PATH"
else
  real=""
  for candidate in /opt/pw-browsers/chromium-*/chrome-linux/chrome \
                   /usr/bin/chromium /usr/bin/chromium-browser /usr/bin/google-chrome; do
    if [ -x "$candidate" ]; then
      real="$candidate"
      break
    fi
  done
  if [ -n "$real" ]; then
    echo "session-start: wrapping $real as chrome --no-sandbox"
    printf '#!/bin/sh\nexec %s --no-sandbox "$@"\n' "$real" > "$BIN_DIR/chrome"
    chmod +x "$BIN_DIR/chrome"
  else
    echo "session-start: WARNING no Chromium found; render gates will report 'cannot run'"
  fi
fi

# 3 - optional PDF exporter dependency.
# Verify the IMPORT, not just the install: pypdf pulls in `cryptography`, and a container that
# mixes a system cryptography with a pip pypdf can install cleanly and still fail at import.
if ! python3 -c "import pypdf" 2>/dev/null; then
  pip install --quiet --disable-pip-version-check -r requirements-export.txt 2>/dev/null || true
  if ! python3 -c "import pypdf" 2>/dev/null; then
    echo "session-start: WARNING pypdf does not import; scripts/export_pdf.py will not run." \
         "Everything else is unaffected."
  fi
fi

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$CLAUDE_ENV_FILE"
fi

echo "session-start: render gates ready"
