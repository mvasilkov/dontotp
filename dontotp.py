#!/usr/bin/env python3
import argparse
from datetime import datetime
import hashlib
from pathlib import Path
from time import sleep
import tomllib
from typing import TypedDict

import colorama
from colorama import Fore, Style
import pyotp


class Account(TypedDict):
    type: str
    secret: str
    issuer: str
    label: str
    digits: int
    algorithm: str
    period: int


class Otp(TypedDict):
    otp: str
    remaining: float


def get_accounts() -> list[Account]:
    secrets_file = Path(__file__).parent.resolve() / 'secrets.toml'
    secrets_text = secrets_file.read_text(encoding='utf-8')
    return tomllib.loads(secrets_text).get('accounts', [])


def get_otp(a: Account) -> Otp:
    otp = pyotp.TOTP(
        a['secret'],
        issuer=a['issuer'],
        name=a['label'],
        digits=a['digits'],
        digest=getattr(hashlib, a['algorithm'].lower()),
        interval=a['period'],
    )
    t = datetime.now()
    return {
        'otp': otp.at(t),
        'remaining': otp.interval - t.timestamp() % otp.interval,
    }


def print_all():
    accounts = get_accounts()
    for a in accounts:
        if a['type'] != 'TOTP':
            continue
        otp = get_otp(a)

        print()
        print(f"{Fore.CYAN}{a['issuer']} {Fore.RESET}{a['label']}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{otp['otp']}{Style.RESET_ALL}")

        remaining = round(otp['remaining'])
        filled = '█' * remaining
        rest = '░' * (a['period'] - remaining)

        print(f'{Fore.YELLOW}|{filled}{rest}|{Style.RESET_ALL}')
        print()


def run(watch=False):
    if not watch:
        print_all()
        return

    try:
        while True:
            print(colorama.ansi.clear_screen())
            print('\x1b[0;0H')
            print_all()
            sleep(1)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--watch', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    colorama.init()
    run(watch=args.watch)
    colorama.deinit()
