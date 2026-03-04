#!/usr/bin/env python3
"""Basic UPS truck loading simulation with simple timing metrics."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import Dict, List, Optional


SHELF_RANGES = {
    "shelf_1": (1300, 5999),
    "shelf_2": (1000, 2999),
    "shelf_3": (3000, 7999),
    "shelf_4": (4000, 8600),
}


@dataclass
class Package:
    package_id: int
    address_number: int
    current_location: str


def valid_shelves(address_number: int) -> List[str]:
    """Return shelves whose ranges include the address number."""
    return [
        shelf
        for shelf, (start, end) in SHELF_RANGES.items()
        if start <= address_number <= end
    ]


def choose_best_shelf(address_number: int, load_counts: Dict[str, int]) -> Optional[str]:
    """Pick a valid shelf with the lightest current load.

    This is a simple stand-in for an optimizer: if multiple shelves are valid,
    choose the one with the fewest packages assigned so far.
    """
    candidates = valid_shelves(address_number)
    if not candidates:
        return None
    return min(candidates, key=lambda shelf: load_counts[shelf])


def simulate(
    num_packages: int,
    move_seconds: float,
    work_hours_per_week: float,
    seed: Optional[int] = None,
) -> None:
    if seed is not None:
        random.seed(seed)

    locations = list(SHELF_RANGES.keys()) + ["floor"]
    packages: List[Package] = []

    for i in range(1, num_packages + 1):
        packages.append(
            Package(
                package_id=i,
                address_number=random.randint(1000, 8600),
                current_location=random.choice(locations),
            )
        )

    load_counts = {shelf: 0 for shelf in SHELF_RANGES}
    move_log = []
    unmappable = 0

    for pkg in packages:
        target = choose_best_shelf(pkg.address_number, load_counts)
        if target is None:
            unmappable += 1
            continue

        load_counts[target] += 1
        if pkg.current_location != target:
            move_log.append((pkg.package_id, pkg.current_location, target, pkg.address_number))
            pkg.current_location = target

    total_moves = len(move_log)
    total_seconds = total_moves * move_seconds
    total_hours = total_seconds / 3600
    weeks = total_hours / work_hours_per_week if work_hours_per_week > 0 else float("inf")

    print("UPS Truck Loading Simulation")
    print("=" * 30)
    print(f"Packages generated: {num_packages}")
    print(f"Packages moved: {total_moves}")
    print(f"Packages with no valid shelf: {unmappable}")
    print()
    print("Final shelf load:")
    for shelf, count in load_counts.items():
        r = SHELF_RANGES[shelf]
        print(f"  {shelf} ({r[0]}-{r[1]}): {count}")

    print()
    print(f"Time per package move: {move_seconds:.2f} sec")
    print(f"Total sort time: {total_seconds:.2f} sec ({total_hours:.2f} hours)")
    print(f"Equivalent work weeks at {work_hours_per_week:.1f} hrs/week: {weeks:.3f}")

    print("\nSample moves (up to 10):")
    for package_id, source, target, addr in move_log[:10]:
        print(f"  pkg#{package_id}: {addr} from {source} -> {target}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Basic UPS shelf-loading simulation")
    parser.add_argument("--packages", type=int, default=100, help="Number of random packages")
    parser.add_argument(
        "--move-seconds",
        type=float,
        default=12.0,
        help="Time metric for one package move",
    )
    parser.add_argument(
        "--work-hours-week",
        type=float,
        default=40.0,
        help="Hours worked per week used for time conversion",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible runs")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    simulate(
        num_packages=args.packages,
        move_seconds=args.move_seconds,
        work_hours_per_week=args.work_hours_week,
        seed=args.seed,
    )
