#!/usr/bin/bash

BASE_DIR="/home/ubuntu/poker-statistics"
DATA_PATH="$BASE_DIR/statistics_data"

deploy_poker_statistics() {
  mkdir -p $DATA_PATH

  docker rm -f poker_statistics

  docker run -d --restart always --name poker_statistics \
      -v $DATA_PATH:/application/statistics_data \
      poker-statistics-image
}

deploy_poker_statistics
