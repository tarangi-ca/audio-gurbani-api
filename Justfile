set dotenv-load := true
set working-directory := '/workspaces/api'
export RUST_BACKTRACE := "/workspaces/api"

alias d := dev
alias m := migrate
alias c := clean

dev:
    docker compose up -d
    fastapi dev app/main.py

migrate +args:
    mkdir -p migrations
    docker run --rm -it \
        -u $(id -u):$(id -g) \
        -e DATABASE_URL=$DATABASE_URL \
        --network=host \
        -v "$(pwd)/:/db" \
        ghcr.io/amacneil/dbmate {{args}}
clean:
    find . -type d \( -name "__pycache__" -o -name ".pytest_cache" \) -exec rm -rf {} +
    find . -type f -name "*.py[cod]" -delete