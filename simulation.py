#!/usr/bin/env python3
"""UPS truck loading simulation with conveyor-order package arrival."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import Dict, List, Optional


SHELF_RANGES = {
    "shelf_1": (1300, 5999),
    "shelf_2": (2000, 6999),
    "shelf_3": (3000, 7999),
    "shelf_4": (4000, 8600),
}


@dataclass
class Package:
    package_id: int
    address_number: int
    length: float
    size: float
    current_location: str


def valid_shelves(address_number: int) -> List[str]:
    """Return shelves whose ranges include the address number."""
    return [
        shelf
        for shelf, (start, end) in SHELF_RANGES.items()
        if start <= address_number <= end
    ]


def choose_best_shelf(address_number: int, load_counts: Dict[str, int]) -> Optional[str]:
    """Pick a valid shelf with the lightest current load."""
    candidates = valid_shelves(address_number)
    if not candidates:
        return None
    return min(candidates, key=lambda shelf: load_counts[shelf])


def generate_packages(
    num_packages: int,
    random_length: bool,
    random_size: bool,
    base_length: float,
    base_size: float,
    min_length: float,
    max_length: float,
    min_size: float,
    max_size: float,
) -> List[Package]:
    """Generate packages in conveyor arrival order (index order)."""
    locations = list(SHELF_RANGES.keys()) + ["floor"]
    packages: List[Package] = []

    for i in range(1, num_packages + 1):
        length = random.uniform(min_length, max_length) if random_length else base_length
        size = random.uniform(min_size, max_size) if random_size else base_size

        packages.append(
            Package(
                package_id=i,
                address_number=random.randint(1000, 8600),
                length=length,
                size=size,
                current_location=random.choice(locations),
            )
        )

    return packages


def simulate(
    num_packages: int,
    move_seconds: float,
    work_hours_per_week: float,
    random_length: bool,
    random_size: bool,
    base_length: float,
    base_size: float,
    min_length: float,
    max_length: float,
    min_size: float,
    max_size: float,
    seed: Optional[int] = None,
) -> None:
    if seed is not None:
        random.seed(seed)

    packages = generate_packages(
        num_packages=num_packages,
        random_length=random_length,
        random_size=random_size,
        base_length=base_length,
        base_size=base_size,
        min_length=min_length,
        max_length=max_length,
        min_size=min_size,
        max_size=max_size,
    )

    load_counts = {shelf: 0 for shelf in SHELF_RANGES}
    move_log = []
    unmappable = 0

    # Process in list order to represent conveyor arrival sequence.
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

    avg_length = sum(pkg.length for pkg in packages) / len(packages) if packages else 0.0
    avg_size = sum(pkg.size for pkg in packages) / len(packages) if packages else 0.0

    print("UPS Truck Loading Simulation")
    print("=" * 30)
    print(f"Packages generated: {num_packages}")
    print(f"Packages moved: {total_moves}")
    print(f"Packages with no valid shelf: {unmappable}")
    print(f"Length mode: {'random' if random_length else 'uniform'}")
    print(f"Size mode: {'random' if random_size else 'uniform'}")
    print(f"Average package length: {avg_length:.2f}")
    print(f"Average package size: {avg_size:.2f}")

    print("\nFinal shelf load:")
    for shelf, count in load_counts.items():
        r = SHELF_RANGES[shelf]
        print(f"  {shelf} ({r[0]}-{r[1]}): {count}")

    print()
    print(f"Time per package move: {move_seconds:.2f} sec")
    print(f"Total sort time: {total_seconds:.2f} sec ({total_hours:.2f} hours)")
    print(f"Equivalent work weeks at {work_hours_per_week:.1f} hrs/week: {weeks:.3f}")

    print("\nConveyor arrival sample (first 10):")
    for pkg in packages[:10]:
        print(
            f"  pkg#{pkg.package_id}: addr={pkg.address_number} "
            f"len={pkg.length:.2f} size={pkg.size:.2f}"
        )

    print("\nSample moves (up to 10):")
    for package_id, source, target, addr in move_log[:10]:
        print(f"  pkg#{package_id}: {addr} from {source} -> {target}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="UPS shelf-loading simulation")
    parser.add_argument("--packages", type=int, default=100, help="Number of packages from conveyor")
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
    parser.add_argument(
        "--base-length",
        type=float,
        default=12.0,
        help="Uniform length used when --random-length is not set",
    )
    parser.add_argument(
        "--base-size",
        type=float,
        default=8.0,
        help="Uniform size used when --random-size is not set",
    )
    parser.add_argument("--random-length", action="store_true", help="Randomize package lengths")
    parser.add_argument("--random-size", action="store_true", help="Randomize package sizes")
    parser.add_argument("--min-length", type=float, default=6.0, help="Minimum random length")
    parser.add_argument("--max-length", type=float, default=30.0, help="Maximum random length")
    parser.add_argument("--min-size", type=float, default=4.0, help="Minimum random size")
    parser.add_argument("--max-size", type=float, default=20.0, help="Maximum random size")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible runs")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    simulate(
        num_packages=args.packages,
        move_seconds=args.move_seconds,
        work_hours_per_week=args.work_hours_week,
        random_length=args.random_length,
        random_size=args.random_size,
        base_length=args.base_length,
        base_size=args.base_size,
        min_length=args.min_length,
        max_length=args.max_length,
        min_size=args.min_size,
        max_size=args.max_size,
        seed=args.seed,
    )
