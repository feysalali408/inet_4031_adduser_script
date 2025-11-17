#!/usr/bin/python3

# INET4031 - Automated User Creation Script (Interactive Version)
# Author: Feysal Ali
# Updated for Step 7 (Dry Run Mode)

import os
import sys
import re

def main():

    # Ask user for dry-run or real-run
    choice = input("Run in DRY RUN mode? (Y/N): ").strip().lower()
    dry_run = (choice == "y")

    if dry_run:
        print("\n>>> DRY RUN ENABLED — No system changes will be made.\n")
    else:
        print("\n>>> REAL RUN ENABLED — Users and groups WILL be created.\n")

    # Process input line-by-line
    for line in sys.stdin:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip comment lines
        if re.match(r"^#", line):
            if dry_run:
                print(f"SKIP (comment): {line}")
            continue

        # Split fields
        fields = line.split(":")
        if len(fields) < 5:
            if dry_run:
                print(f"ERROR: Not enough fields → {line}")
            continue

        username, password, last_name, first_name, groups = fields
        gecos = f"{first_name} {last_name},,,"
        group_list = groups.split(",")

        # ---- CREATE USER ----
        print(f"==> Creating account for {username}...")
        cmd = f"/usr/sbin/adduser --disabled-password --gecos '{gecos}' {username}"

        if dry_run:
            print("DRY RUN - would run:", cmd)
        else:
            os.system(cmd)

        # ---- SET PASSWORD ----
        print(f"==> Setting the password for {username}...")
        cmd = f"/bin/echo -ne '{password}\n{password}' | /usr/bin/sudo /usr/bin/passwd {username}"

        if dry_run:
            print("DRY RUN - would run:", cmd)
        else:
            os.system(cmd)

        # ---- ADD TO GROUPS ----
        for group in group_list:
            if group.strip() == "-" or group.strip() == "":
                if dry_run:
                    print(f"SKIP (no groups) for {username}")
                continue

            print(f"==> Assigning {username} to the {group} group...")
            cmd = f"/usr/sbin/adduser {username} {group}"

            if dry_run:
                print("DRY RUN - would run:", cmd)
            else:
                os.system(cmd)

if __name__ == "__main__":
    main()
