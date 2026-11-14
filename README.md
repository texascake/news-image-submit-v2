# news-image-01 entry v2: Friday 13 November 2026 — 26 stories

An editorial infographic summing up the world news of Friday 13 November
2026 in 26 stories: three large illustrated panels on the left (the FAA
grounding all US departures, the US downing two Iranian drones, the
Trump–Xi–Putin summit at APEC), eight more illustrated stories in a list
on the right, and fifteen one-line stories in a band along the bottom,
with the day's sources credited underneath.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The program copies the bundled `entry.png` (JPEG bytes under a `.png`
name, 1024×1024, under 1 MiB) to the output directory and verifies the
copy byte for byte. Python 3.13, standard library only, no network.

## License

MIT — see `LICENSE`.
