# UPS Truck Simulator

Basic first-pass simulation for loading UPS truck shelves by address ranges.

## Shelf ranges

- `shelf_1`: 1300-5999
- `shelf_2`: 1000-2999
- `shelf_3`: 3000-7999
- `shelf_4`: 4000-8600

## What the simulation does

1. Generates random packages with an address number from 1000 to 8600.
2. Gives each package a random starting location (`shelf_1..shelf_4` or `floor`).
3. Assigns each package to a valid shelf using a basic balancing rule (least-loaded valid shelf).
4. Counts each location change as one move.
5. Converts total moves into a time metric using `--move-seconds` and estimated work weeks.

Package size is treated as uniform in this version.

## Run

```bash
python3 simulation.py --packages 200 --move-seconds 10 --work-hours-week 40 --seed 7
```

Adjust `--move-seconds` to represent your handling-time metric per package move.
