#!/bin/sh

set -e

BOOTC_IMG_TAG=localhost/cloudland2025-demo:latest
CONTAINERDISK_TAG=quay.io/fmatouschek/cloudland2025-demo:latest

sudo podman build -t "${BOOTC_IMG_TAG}" -f Containerfile.bootc .

mkdir -p output
sudo podman run \
    --rm \
    -it \
    --privileged \
    --pull=newer \
    --security-opt label=type:unconfined_t \
    -v ./output:/output \
    -v /var/lib/containers/storage:/var/lib/containers/storage \
    quay.io/centos-bootc/bootc-image-builder:latest \
    --type qcow2 \
    --use-librepo=True \
    --rootfs btrfs \
    "${BOOTC_IMG_TAG}"

podman build -t "${CONTAINERDISK_TAG}" -f Containerfile.containerdisk .
