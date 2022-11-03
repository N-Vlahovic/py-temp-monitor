#!/usr/bin/env python3
from dataclasses import dataclass
import re
import subprocess
from time import sleep


@dataclass()
class Cache:
    min: float = float("inf")
    cur: float | None = None
    max: float = -float("inf")


CACHE: Cache = Cache()
P_CPU: re.Pattern = re.compile(r"(?<=tccd1:)[\s\d.°c+-]+")


def new_cache(*args) -> dict:
    return {
        key: None for key in args
    }



def get_cpu_temp(cmd: str) -> float | None:
    temp = None
    try:
        temp = re.sub(r"[^\d.+-]", "", P_CPU.findall(cmd.lower())[0].strip())
        temp = float(temp)
    except IndexError:
        pass
    finally:
        return temp


def update_cache() -> None:
    global CACHE
    tmp = get_cpu_temp(subprocess.check_output(["sensors"]).decode())
    CACHE.cur = tmp
    if tmp < CACHE.min:
        CACHE.min = tmp
    if tmp > CACHE.max:
        CACHE.max = tmp


def main() -> None:
    global CACHE
    try:
        while True:
            update_cache()
            print(CACHE)
            sleep(3)
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    main()
