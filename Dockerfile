FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /home/dnly/stage/madcad

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libgl1-mesa-dev \
    libegl1-mesa-dev \
    libx11-dev \
    libxcursor-dev \
    libxrandr-dev \
    libxi-dev \
    libxxf86vm-dev \
    libglfw3-dev \
    pkg-config \
    libssl-dev \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY pyproject.toml Cargo.toml ./
RUN pip install --root-user-action=ignore maturin pytest

RUN maturin fetch --python python3

CMD ["bash"]