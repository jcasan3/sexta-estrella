#!/usr/bin/env bash
# Prepara un espacio de trabajo nuevo: dependencias + voz Kokoro (Apache-2.0) + voz Piper de reserva
set -e
cd "$(dirname "$0")"
pip install --break-system-packages -q kokoro-onnx soundfile pillow numpy piper-tts
mkdir -p voices/kokoro
[ -f voices/kokoro/kokoro-v1.0.onnx ] || curl -sSL -o voices/kokoro/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f voices/kokoro/voices-v1.0.bin ] || curl -sSL -o voices/kokoro/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
echo "setup ok"
