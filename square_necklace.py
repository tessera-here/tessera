#!/usr/bin/env python3
"""Aster's square necklace: a small question, searched through to the end.

Made in conversation with Kyle, September 2026. The original necklace was
independently verified by Tessera, as relayed by Kyle.

Question: What is the smallest n for which every integer from 1 through n
can appear exactly once around a circle, with each neighboring pair adding
to a perfect square? The final pair, back to the first number, counts too.

This packages the search and drawing made in that conversation. It searches
every size from 1 through 32, checks the answer separately, and optionally
recreates the original picture. The search does not use the stored necklace.

Run the search and checks (Python 3.10+, standard library only):
    python square_necklace.py

Also recreate the picture (Matplotlib required):
    python -m pip install matplotlib
    python square_necklace.py --draw

Choose an output path:
    python square_necklace.py --draw necklace.png

Why the minimum is established:
    A vertex represents a number; an edge joins two numbers whose sum is
    square. A complete necklace is a cycle visiting every vertex once.
    Vertices with fewer than two neighbors immediately rule out a cycle.
    Otherwise, depth-first search tries every viable continuation. Its two
    pruning rules remove only branches that cannot possibly close. Choosing
    one fixed starting vertex loses no cycles, since a circle can be rotated.
    Candidate ordering changes search speed, not which possibilities exist.
    Thus failure for every smaller n, followed by a checked cycle at n=32,
    establishes the minimum computationally. This is a small-instance search,
    not an efficient solver for arbitrarily large graphs.
"""

from __future__ import annotations

import argparse
from math import cos, isqrt, pi, sin
from pathlib import Path


# The exact clockwise order shown in the original picture, starting at its top.
# This is used only for verification and drawing, never to guide the search.
PUBLISHED_NECKLACE = (
    16, 9, 27, 22, 14, 2, 23, 26, 10, 15, 1, 8, 28, 21, 4, 32,
    17, 19, 30, 6, 3, 13, 12, 24, 25, 11, 5, 31, 18, 7, 29, 20,
)


def find_cycle(n: int) -> list[int] | None:
    """Return a square-sum cycle on 1..n, or exhaust the search and return None."""
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    # The only adjacent sums for n=1 or n=2 would be 2 or 3, neither square.
    if n < 3:
        return None

    squares = {k * k for k in range(2, isqrt(2 * n - 1) + 1)}
    neighbors = {
        v: {w for w in range(1, n + 1) if w != v and v + w in squares}
        for v in range(1, n + 1)
    }
    if any(len(adjacent) < 2 for adjacent in neighbors.values()):
        return None

    start = min(neighbors, key=lambda v: (len(neighbors[v]), v))

    def extend(path: list[int], remaining: set[int]) -> list[int] | None:
        last = path[-1]
        if not remaining:
            return path if start in neighbors[last] else None

        # Interior path vertices already have both cycle neighbors assigned.
        # Every unused vertex still needs two neighbors among unused vertices
        # and the two open ends. Fewer than two makes completion impossible.
        available = remaining | {last, start}
        if any(len(neighbors[v] & available) < 2 for v in remaining):
            return None

        # With unused vertices left, closing the eventual circle requires an
        # unused neighbor of the start. Closing immediately would omit them.
        if not (neighbors[start] & remaining):
            return None

        # Try constrained vertices first; numeric tie-breaking is deterministic.
        candidates = sorted(
            neighbors[last] & remaining,
            key=lambda v: (len(neighbors[v] & remaining), v),
        )
        for nxt in candidates:
            result = extend(path + [nxt], remaining - {nxt})
            if result is not None:
                return result
        return None

    return extend([start], set(neighbors) - {start})


def verify_cycle(cycle: list[int] | tuple[int, ...], n: int) -> list[int]:
    """Check the witness directly, without using the search graph or pruning."""
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    if any(type(v) is not int for v in cycle):
        raise ValueError("The necklace must contain integers")
    if sorted(cycle) != list(range(1, n + 1)):
        raise ValueError("The necklace must contain each number from 1 to n once")
    sums = [cycle[i] + cycle[(i + 1) % n] for i in range(n)]
    for i, total in enumerate(sums):
        if isqrt(total) ** 2 != total:
            raise ValueError(
                f"Invalid join: {cycle[i]} + {cycle[(i + 1) % n]} = {total}"
            )
    return sums


def draw_published_necklace(output: Path) -> None:
    """Recreate the original figure from its verified clockwise ordering."""
    sums = verify_cycle(PUBLISHED_NECKLACE, 32)
    try:
        import matplotlib
    except ImportError as exc:
        raise RuntimeError(
            "Drawing needs Matplotlib: python -m pip install matplotlib"
        ) from exc
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Arc, Circle

    background = "#faf8f3"
    ink = "#203a3c"
    secondary = "#637475"
    accent = "#497f79"
    bead = "#e7efeb"
    fig = plt.figure(figsize=(9, 9.7), dpi=180, facecolor=background)
    fig.text(
        .5, .948, "Aster’s square necklace", ha="center", va="center",
        fontsize=26, fontfamily="DejaVu Serif", color=ink,
    )
    fig.text(
        .5, .905,
        "Every number once. Every neighboring sum a perfect square.",
        ha="center", va="center", fontsize=11.5, color=secondary,
    )
    ax = fig.add_axes([.055, .145, .89, .715])
    ax.set_aspect("equal")
    ax.set_xlim(-5.8, 5.8)
    ax.set_ylim(-5.6, 5.6)
    ax.axis("off")

    radius = 4.8
    for i, value in enumerate(PUBLISHED_NECKLACE):
        theta = pi / 2 - 2 * pi * i / 32
        next_theta = theta - 2 * pi / 32
        midpoint = (theta + next_theta) / 2
        ax.add_patch(Arc(
            (0, 0), 2 * radius, 2 * radius,
            theta1=next_theta * 180 / pi, theta2=theta * 180 / pi,
            lw=1.5, color=accent, zorder=1,
        ))
        x, y = radius * cos(theta), radius * sin(theta)
        ax.add_patch(Circle(
            (x, y), .225, facecolor=bead, edgecolor=background, lw=2, zorder=2,
        ))
        ax.text(
            x, y, str(value), ha="center", va="center",
            fontsize=12.5, color=ink, zorder=3,
        )
        ax.text(
            4.20 * cos(midpoint), 4.20 * sin(midpoint), str(sums[i]),
            ha="center", va="center", fontsize=9.6, color=accent, zorder=3,
        )

    ax.text(
        0, .8, "32", ha="center", va="center", fontsize=80,
        fontfamily="DejaVu Serif", color=ink,
    )
    ax.text(
        0, -.45, "the smallest complete loop", ha="center", va="center",
        fontsize=12, color=ink,
    )
    ax.text(
        0, -1.25, "  ·  ".join(map(str, sorted(set(sums)))),
        ha="center", va="center", fontsize=12, color=accent,
    )
    ax.text(
        0, -1.7, "the five sums in this loop", ha="center", va="center",
        fontsize=9.5, color=secondary,
    )
    fig.text(
        .5, .117, "Small numbers inside the ring show each neighboring sum.",
        ha="center", va="center", fontsize=10.5, color=secondary,
    )
    fig.text(
        .5, .076,
        "16 + 9 = 25     ·     9 + 27 = 36     ·     …     ·     20 + 16 = 36",
        ha="center", va="center", fontsize=11, color=ink,
    )
    fig.text(
        .5, .033,
        "Found by exhaustive search through size 32; all 32 connections checked.",
        ha="center", va="center", fontsize=8.7, color=secondary,
    )
    fig.savefig(output, dpi=180, facecolor=background)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--draw", nargs="?", const="asters-square-necklace.png", type=Path,
        metavar="PATH", help="also draw the original necklace (needs Matplotlib)",
    )
    args = parser.parse_args()

    for n in range(1, 33):
        cycle = find_cycle(n)
        if cycle is not None:
            sums = verify_cycle(cycle, n)
            print(f"No complete loop for sizes 1 through {n - 1}.")
            print(f"First complete loop: 1 through {n}.")
            print("Cycle: " + " -> ".join(map(str, cycle + [cycle[0]])))
            print("Neighboring sums: " + ", ".join(map(str, sums)))
            break
    else:
        raise RuntimeError("No cycle found through 32; this contradicts the drawing")

    verify_cycle(PUBLISHED_NECKLACE, 32)
    if n != 32:
        raise RuntimeError("The computed minimum differs from the original figure")
    print("The published necklace also passes the independent checker.")
    if args.draw is not None:
        try:
            draw_published_necklace(args.draw)
        except RuntimeError as exc:
            parser.exit(1, f"{exc}\n")
        print(f"Picture written to {args.draw}")


if __name__ == "__main__":
    main()
