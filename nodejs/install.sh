#!/bin/bash
# =========================================
# Node.js 服务自动部署脚本（固定端口 14273）
# =========================================
set -euo pipefail
export LC_ALL=C
IFS=$'\n\t'

NODE_BIN="npm"
START_CMD="start"
INSTALL_CMD="ci --only=production --loglevel=error"
LOG_FILE="/dev/stdout"

check_deps() {
  if [ ! -d "node_modules" ]; then
    echo "📥 Installing production dependencies..."
    $NODE_BIN $INSTALL_CMD || { echo "❌ Install failed!"; exit 1; }
  else
    echo "✅ Dependencies already installed."
  fi
}

prompt_port() {
  local port=${PORT:-14273}
  echo "✅ Fixed port: $port (listening on 0.0.0.0:$port)"
}

run_background_loop() {
  echo "🚀 Starting Node.js server on port 14273..."
  while true; do
    prompt_port
    $NODE_BIN $START_CMD >"$LOG_FILE" 2>&1 || true
    echo "⚠️ Node.js crashed. Restarting in 5s..."
    sleep 5
  done
}

main() {
  check_deps
  run_background_loop
}

main "$@"
