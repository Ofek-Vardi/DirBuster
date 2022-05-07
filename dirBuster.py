#!/usr/bin/python3

import mechanize
import sys
import argparse
from termcolor import colored as clr


def enum(site: str, lst: list, level: int = 0) -> None:
    """
    Prints valid subdirectories of the given URL.
    :param site: Website URL
    :type site: str
    :param lst: Subdirectory list
    :type lst: list
    :param level: Current recursion level
    :type level: int
    :return: None
    """
    global SUMMARY
    # Recursion depth enforcement
    if level < DEPTH:
        br = mechanize.Browser()  # Initialize browser
        for suffix in lst:
            try:
                path = f"{site}/{suffix}"
                if VERBOSE:
                    print(f"{clr('[*] Sending request for:', 'yellow')} {path}")
                r = br.open(path, timeout=TIMEOUT)  # Request attempt
                if r.code == 200:  # Valid link
                    res = clr(f"[+] {path}", "green")
                    print(res)
                    # Append results to summary
                    if VERBOSE or DEBUG:
                        SUMMARY.append(res)
                    # Call the 'scan()' function recursively
                    # Remove the current 'word' from 'word_list' to avoid infinite loop
                    enum(path, [item for item in lst if item != suffix], level=level + 1)
            except Exception as err:  # Invalid link
                if DEBUG:
                    print(clr(f"[!] {err}", "red"))
    elif VERBOSE:
        print(clr("[*] Recursion depth limit reached, moving on...", "yellow"))


def validate_url(protocols: list[str]) -> str:
    """
    Validates whether a URL is reachable via https / http / other protocol provided by the user.
    :param protocols: List of protocols to validate
    :type protocols: list[str]
    :return: New URL prefixed by the first validated protocol from 'protocols', if one exists
    :rtype: str
    """
    if VERBOSE:
        print(f"{clr('[*] Validating required protocol...', 'yellow')}")
    br = mechanize.Browser()  # Request attempt
    for protocol in protocols:
        try:
            path = f"{protocol}://{WEBSITE}"
            if br.open(path, timeout=TIMEOUT).code == 200:  # Valid protocol found
                return path
        except Exception as err:  # Invalid protocol
            if DEBUG:
                print(clr(f"[!] {err}", "red"))
    # No valid protocol found
    print(f"{clr('[!] URL UNREACHABLE:', 'red')} {WEBSITE}")
    sys.exit()


def main() -> None:
    """
    This script spiders through a URL recursively and prints available subdirectories.
    :return: None
    """
    global WEBSITE
    if "//" in WEBSITE:
        protocols = WEBSITE.split("://")[0]
    else:
        protocols = ["https", "http"]
    valid_path = validate_url(protocols)
    if VERBOSE:
        print(f"{clr('[*] URL Validated:', 'yellow')} {valid_path}")
    # Although DIRS is a global variable, I have to pass it as an argument into 'enum()',
    # since it is a recursive function, which replaces its 2nd argument on each subsequent call
    enum(valid_path, DIRS)

    # Results summary
    if VERBOSE or DEBUG:
        print(clr("\n[*] Summary:", "yellow"))
        if SUMMARY:
            print("\n".join(SUMMARY))
        else:
            print(clr("[!] No subdirectories found!", "red"))


if __name__ == "__main__":
    # Initialize the parser
    parser = argparse.ArgumentParser(
        description="Description: Python Web Spider"
    )
    # Add the parameters positional/optional
    parser.add_argument("website", help="Target website URL (E.g: mysite.com, https://www.mysite.com, etc)", type=str)
    parser.add_argument('-l', '--wordlist', help="Path to wordlist file", type=str, default="")
    parser.add_argument('-rd', '--recursion-depth', help="Depth limit for recursive enumeration", type=int, default=2)
    parser.add_argument('-t', '--timeout', help="Time limit for web requests", type=int, default=1)
    parser.add_argument('-v', '--verbose', help="Increase verbosity level", type=int, default=0, nargs='?',
                        const=1)
    parser.add_argument('-d', '--debug', help="Print debugging notes", type=int, default=0, nargs='?',
                        const=1)
    # Parse the arguments
    args = parser.parse_args()

    # Global variables
    WEBSITE = args.website
    DEPTH = args.recursion_depth
    TIMEOUT = args.timeout
    VERBOSE = args.verbose
    DEBUG = args.debug
    SUMMARY = []
    wordlist_path = args.wordlist
    if wordlist_path:  # Wordlist argument was provided
        try:
            # Get subdirectory list
            with open(wordlist_path, "r") as f:
                DIRS = f.readlines()
            # Strip newlines
            for i, word in enumerate(DIRS):
                DIRS[i] = word.strip()
        except (FileNotFoundError, IOError) as error:  # Unable to read from the given wordlist file
            print(f"clr(f'[!] ERROR: {error}', 'red') {wordlist_path}")
            sys.exit()
    else:
        # Default value for DIRS, in case wordlist argument wasn't provided
        DIRS = ["hypertext", "login.php", "user", "1", "2", "index.html", "robots.txt", "careers", "platform",
                "bundles"]
    try:
        main()
    except KeyboardInterrupt:
        pass
