![Crawler](https://github.com/ptrstn/austrian-gas-prices/actions/workflows/data-crawler.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Austria Gas Prices

An automated data crawler for austrian gas prices.

## Installation

```bash
pip install --user git+https://github.com/ptrstn/oidafuel
pip install --user git+https://github.com/ptrstn/austrian-gas-prices
```

## Usage

### Help

```bash
agp --help
```

```
usage: oidafuel [-h] [--version] [--list-regions] [--fuel-type {SUP,DIE,GAS}] [--region REGION | --address ADDRESS]

Check gas prices for a given location

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --list-regions        List Regions
  --fuel-type {SUP,DIE,GAS}
                        SUP (Super 95), DIE (Diesel) or GAS (Compressed natural gas)
  --region REGION       Region code
  --address ADDRESS     Address
```

### Example

```bash
agp --vienna
```

```
Austrian Gas Prices (agp), v0.0.1

== Vienna ==
Checking region 900 for Super 95 prices... (0 found)
Checking region 901 for Super 95 prices... (1 found)
Checking region 902 for Super 95 prices... (5 found)
Checking region 903 for Super 95 prices... (6 found)
Checking region 904 for Super 95 prices... (2 found)
Checking region 905 for Super 95 prices... (4 found)
Checking region 906 for Super 95 prices... (1 found)
Checking region 907 for Super 95 prices... (2 found)
Checking region 908 for Super 95 prices... (1 found)
Checking region 909 for Super 95 prices... (2 found)
Checking region 910 for Super 95 prices... (5 found)
Checking region 911 for Super 95 prices... (6 found)
Checking region 912 for Super 95 prices... (5 found)
Checking region 913 for Super 95 prices... (3 found)
Checking region 914 for Super 95 prices... (5 found)
Checking region 915 for Super 95 prices... (5 found)
Checking region 916 for Super 95 prices... (6 found)
Checking region 917 for Super 95 prices... (3 found)
Checking region 918 for Super 95 prices... (3 found)
Checking region 919 for Super 95 prices... (6 found)
Checking region 920 for Super 95 prices... (5 found)
Checking region 921 for Super 95 prices... (5 found)
Checking region 922 for Super 95 prices... (6 found)
Checking region 923 for Super 95 prices... (5 found)
Saving 92 gas prices in vienna_SUP.csv...
```
