# TODO - verify hashes
# TODO - typing
import argparse
import asyncio
import logging
import os
import shutil
import subprocess
from subprocess import Popen
import sys
import zipfile
import tarfile
from typing import Optional, List, Dict

import asyncpg
from pathlib import Path

import requests
from requests import Response

logger: logging.Logger = logging.getLogger('postgres-script')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(name)-24s %(message)s')

SDK_POSTGRES_PORT: int = os.environ.get('SDK_POSTGRES_PORT', 15432)
MODULE_DIR: Path = Path(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_MAP: Dict[str, str] = {
    "win32": "https://get.enterprisedb.com/postgresql/postgresql-9.6.15-2-windows-x64-binaries.zip",
    "linux": "https://get.enterprisedb.com/postgresql/postgresql-9.6.15-2-linux-x64-binaries.tar.gz",
    "darwin": "https://get.enterprisedb.com/postgresql/postgresql-9.6.15-2-osx-binaries.zip",
}
FILENAME: str = DOWNLOAD_MAP[sys.platform].split("/")[-1]
DOWNLOAD_PATH: Path = MODULE_DIR / FILENAME
EXTRACTION_PATH: Path = MODULE_DIR / "postgres-9.6.15"

POSTGRES_BIN: Path = EXTRACTION_PATH/"pgsql"/"bin"
INITDB: Path = POSTGRES_BIN/"initdb.exe" if sys.platform == "win32" else POSTGRES_BIN/"initdb"
PG_CTL: Path = POSTGRES_BIN/"pg_ctl.exe" if sys.platform == "win32" else POSTGRES_BIN/"pg_ctl"
CREATEUSER: Path = POSTGRES_BIN/"createuser.exe" if sys.platform == "win32" else POSTGRES_BIN/"createuser"
CREATEDB: Path = POSTGRES_BIN/"createdb.exe" if sys.platform == "win32" else POSTGRES_BIN/"createdb"
PG_DATA: Path = EXTRACTION_PATH/"pgsql"/"data"


def check_extract_done() -> bool:
    if EXTRACTION_PATH.exists():
        return True
    return False


def check_initdb_done() -> bool:
    if PG_DATA.exists():
        return True
    return False


async def pg_connect() -> asyncpg.Connection:
    pg_conn: asyncpg.Connection = await asyncpg.connect(
        user="postgres",
        host="127.0.0.1",
        port=SDK_POSTGRES_PORT,
        password='postgres',
        database="postgres",
    )
    return pg_conn


async def check_running() -> bool:
    pg_conn = Optional[asyncpg.Connection]
    try:
        pg_conn: asyncpg.Connection = await pg_connect()
        return True
    except ConnectionRefusedError:
        logger.debug("postgres is not running")
        return False
    finally:
        if pg_conn:
            await pg_conn.close()


def extract():
    try:
        if sys.platform == "win32":
            if not EXTRACTION_PATH.exists():
                with zipfile.ZipFile(DOWNLOAD_PATH, 'r') as z:
                    z.extractall(EXTRACTION_PATH)
        else:
            if not EXTRACTION_PATH.exists():
                with tarfile.open(DOWNLOAD_PATH, 'r') as gz:
                    gz.extractall(EXTRACTION_PATH)
    finally:
        os.remove(DOWNLOAD_PATH)


def download_and_extract():
    if not check_extract_done():
        r: Response = requests.get(DOWNLOAD_MAP[sys.platform])
        with open(DOWNLOAD_PATH, "wb") as f:
            f.write(r.content)
        extract()


def spawn(cmd: List[str]):
    process = Optional[Popen[str]]
    if sys.platform == 'win32':
        process: Popen[str] = subprocess.Popen(cmd, env=os.environ.copy())
    elif sys.platform in {'linux', 'darwin'}:
        process: Popen[str] = subprocess.Popen(f"{cmd}", shell=True, env=os.environ.copy())

    if process:
        process.wait()


def initdb():
    os.makedirs(PG_DATA, exist_ok=True)
    cmd: List[str] = [str(INITDB), "--pgdata", str(PG_DATA), "--username", "postgres"]
    spawn(cmd)


def start():
    cmd: List[str] = [str(PG_CTL), "-o", f"-p {SDK_POSTGRES_PORT}", "-D", str(PG_DATA), "-l", str(PG_DATA/"postgres-logfile.log"), "-w", "start"]
    spawn(cmd)


def stop():
    cmd: List[str] = [str(PG_CTL), "-D", str(PG_DATA), "stop"]
    spawn(cmd)


def reset():
    if asyncio.run(check_running()):
        stop()

    if PG_DATA.exists():
        logger.info("resetting postgres data directory")
        shutil.rmtree(PG_DATA)
    os.makedirs(PG_DATA, exist_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true", help="download postgres")
    parser.add_argument("--initdb", action="store_true", help="initdb postgres")
    parser.add_argument("--start", action="store_true", help="start postgres")
    parser.add_argument("--stop", action="store_true", help="stop postgres")
    parser.add_argument("--reset", action="store_true", help="reset postgres datadir")
    parsed_args = parser.parse_args()
    if parsed_args.download:
        download_and_extract()
    elif parsed_args.initdb:
        initdb()
    elif parsed_args.start:
        start()
    elif parsed_args.stop:
        stop()
    elif parsed_args.reset:
        reset()


# main()
download_and_extract()
