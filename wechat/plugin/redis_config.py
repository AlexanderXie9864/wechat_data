#!/usr/bin/env python3
# coding=utf-8
# __author__: Alexander
import redis
# pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
redis_sr = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True, password=)  # 数据采集数据库

redis_map = redis.Redis(host='localhost', port=6379, db=2, decode_responses=True, password=)  # 经纬度数据
