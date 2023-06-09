ARG my_appname=omnicrossrsm

FROM rust:slim-bullseye as build
ARG my_appname
ENV my_appname=$my_appname

RUN apt update && apt install -y pkg-config libssl-dev

# create a new empty shell project
RUN USER=root cargo new --bin ${my_appname}
WORKDIR /${my_appname}

# copy over your manifests
COPY ./rsm/Cargo.lock ./Cargo.lock
COPY ./rsm/Cargo.toml ./Cargo.toml

# this build step will cache your dependencies
RUN cargo build --release
RUN rm src/*.rs

# copy your source tree
COPY ./rsm/src ./src

# build for release
RUN rm ./target/release/deps/${my_appname}*
RUN cargo build --release

# our final base
FROM debian:bullseye-slim
ARG my_appname
ENV my_appname=$my_appname

# copy the build artifact from the build stage
COPY --from=build /${my_appname}/target/release/${my_appname} /usr/bin/${my_appname}

# set the startup command to run your binary
CMD ${my_appname}