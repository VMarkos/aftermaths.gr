import json

import utils

def main():
    VALUES = [8, 8, 7, 7, 6, 6, 5, 5, 5, 4, 4, 4]
    domains = []
    for n, m in [(17, 3), (15, 3), (20, 3), (23, 4)]:
        domains.append(utils.find_partitions(n, m, VALUES))
    with open("domains.json", "w") as file:
        json.dump(domains, file, indent=2)

if __name__ == "__main__":
    main()