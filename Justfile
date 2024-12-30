set working-directory := '/workspaces/api'
export RUST_BACKTRACE := "/workspaces/api"

alias d := dev
alias c := clean

dev:
    fastapi dev app/main.py

clean:
    find . -type d \( -name "__pycache__" -o -name ".pytest_cache" \) -exec rm -rf {} +
    find . -type f -name "*.py[cod]" -delete