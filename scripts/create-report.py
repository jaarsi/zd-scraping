import argparse
import json
import os
from datetime import datetime
from io import StringIO

import pandas as pd

from app.scrape import get_all_results


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", default=os.cpu_count(), type=int)
    parser.add_argument("--results_per_page", default=12, type=int)
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        filename = f"reports/{datetime.now().isoformat()}"
        print(f"Creating report on '{filename}'")
        concurrency, results_per_page = (
            min(args.concurrency, 32),
            args.results_per_page,
        )
        print(f"{concurrency=}")
        print(f"{results_per_page=}")

        def handler(page: int):
            print(f"\r\033[0;32mRetrieving data from page {page:04d}", end="")

        results, errors = get_all_results(concurrency, results_per_page, handler)
        print(
            f"\n\033[0;35mCompleted with {len(results)} results and {len(errors)} errors"
        )
        results = sorted(results, key=lambda item: item["_page"])
        pd.read_json(StringIO(json.dumps(results))).to_csv(f"{filename}.csv")

        if errors:
            with open(f"{filename}-errors.json", "w") as file:
                json.dump(errors, file, indent=4)
    except KeyboardInterrupt:
        print("\n\033[0;31mInterrupted")
    except Exception as error:
        print(str(error))
    finally:
        print("\033[0mEnd")


if __name__ == "__main__":
    main()
