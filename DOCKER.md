# Docker Development Stack

## Quick Start

```bash
# Build image
docker compose build dev

# Development shell
docker compose run --rm dev

# Run tests headless
docker compose run --rm test-headless

# Run with local display (Linux)
docker compose run --rm -e DISPLAY=$DISPLAY dev
```

## Services

| Service | Description | Usage |
|---------|-------------|-------|
| `dev` | Development environment with Rust | `docker compose run dev` |
| `shell` | Interactive shell | `docker compose run shell` |
| `test-headless` | Run pytest with Xvfb | `docker compose run test-headless` |
| `xvfb` | X11 virtual display | Auto-started for headless tests |

## Building

```bash
# Development build (debug symbols)
docker compose build dev

# Release build (optimized)
docker compose build --build-arg Maturin_FEATURE_FLAGS=--release dev
```

## Running Tests

```bash
# All tests headless
docker compose run --rm test-headless

# Specific test file
docker compose run --rm test-headless pytest tests/test_mesh.py -v

# Single test
docker compose run --rm test-headless pytest tests/test_mesh.py::test_function_name -v
```

## Development Workflow

```bash
# 1. Enter container
docker compose run --rm dev

# 2. Build Rust extension
maturin develop

# 3. Run tests
pytest tests/ -v

# 4. Edit code (changes sync automatically)
# ...
```

## GPU/OpenGL

For hardware acceleration:

```bash
# With NVIDIA GPU
docker compose run --rm --gpus all dev

# Add to docker-compose.yml:
#   deploy:
#     resources:
#       reservations:
#         devices:
#           - driver: nvidia
```

## Troubleshooting

```bash
# Software rendering
export LIBGL_ALWAYS_SOFTWARE=1

# Check container GPU
docker run --rm --gpus all nvidia/cuda:12-runtime nvidia-smi

# View logs
docker compose logs -f
```

## Files

- `Dockerfile` - Python 3.12 + Rust build environment
- `docker-compose.yml` - Service definitions