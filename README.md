# UPS Truck Simulator

Basic simulation for loading UPS truck shelves by address ranges with conveyor-style package arrival.

## Shelf ranges

- `shelf_1`: 1300-5999
- `shelf_2`: 2000-6999
- `shelf_3`: 3000-7999
- `shelf_4`: 4000-8600

## What the simulation does

1. Generates a conveyor sequence of packages (ordered list in arrival order).
2. Each package gets:
   - random address number (1000 to 8600)
   - starting location (`shelf_1..shelf_4` or `floor`)
   - `length` and `size` values
3. Supports uniform or randomized package dimensions:
   - uniform defaults: `--base-length`, `--base-size`
   - random toggles: `--random-length`, `--random-size`
4. Assigns each package to a valid shelf using a basic balancing rule (least-loaded valid shelf).
5. Counts each location change as one move, then converts moves to time and work weeks.

## Run examples

Uniform dimensions:

```bash
python3 simulation.py --packages 200 --move-seconds 10 --work-hours-week 40 --base-length 12 --base-size 8 --seed 7
```

Random length and random size:

```bash
python3 simulation.py --packages 200 --random-length --random-size --min-length 6 --max-length 30 --min-size 4 --max-size 20 --seed 7
```

Adjust `--move-seconds` to represent your handling-time metric per package move.
