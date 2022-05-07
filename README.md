# Python Directory Buster

## Description

This is a web spider tool written in python.\
Please run this script using python3 and above.

## Comman Line Arguments

    positional arguments:
    website               Target website URL (E.g: mysite.com, https://www.mysite.com, etc)

    options:
    -h, --help            show this help message and exit
    -l WORDLIST, --wordlist WORDLIST
                            Path to wordlist file
    -rd RECURSION_DEPTH, --recursion-depth RECURSION_DEPTH
                            Depth limit for recursive enumeration
    -t TIMEOUT, --timeout TIMEOUT
                            Time limit for web requests
    -v [VERBOSE], --verbose [VERBOSE]
                            Increase verbosity level
    -d [DEBUG], --debug [DEBUG]
                            Print debugging notes

## Examples

**Display help message:**

```
python3 dirBuster.py -h
```

**Scan `mysite.com`:**

```
python3 dirbuster.py mysite.com
```

**Set recursion depth to 3:**

```
python3 dirbuster.py mysite.com -rd 3
```

**Set custom wordlist:**

```
python3 dirbuster.py mysite.com -l WORDLIST_PATH
```
