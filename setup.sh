#!/usr/bin/env bash
# Prepara un espacio de trabajo nuevo: dependencias + voz es-MX (Piper, Apache-2.0)
set -e
cd "$(dirname "$0")"
pip install --break-system-packages -q piper-tts pillow numpy
mkdir -p voices && cd voices
if [ ! -d vits-piper-es_MX-claude-high ]; then
  curl -sSL -o v.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-es_MX-claude-high.tar.bz2
  tar xjf v.tar.bz2 && rm v.tar.bz2
fi
echo "setup ok"
