import random
import time
import sys
import msvcrt
from dataclasses import dataclass
from rich.console import Console
from rich.live import Live

console = Console()
WIDTH, HEIGHT = console.size.width, console.size.height


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    char: str
    color: str

    def update(self, wind_x: float):
        self.vx += wind_x
        self.x += self.vx
        self.y += self.vy


class WeatherEngine:
    def __init__(self):
        self.particles = []
        self.wind = 0.0
        self.intensity = 0.3
        self.mode = "rain"  # rain | snow

    def spawn(self):
        if random.random() > self.intensity:
            return

        if self.mode == "rain":
            self.particles.append(
                Particle(
                    x=random.randint(0, WIDTH),
                    y=0,
                    vx=0,
                    vy=1.2,
                    char="|",
                    color="cyan"
                )
            )
        else:  # snow
            self.particles.append(
                Particle(
                    x=random.randint(0, WIDTH),
                    y=0,
                    vx=random.uniform(-0.2, 0.2),
                    vy=0.4,
                    char="*",
                    color="white"
                )
            )

    def update(self):
        self.spawn()

        for p in self.particles:
            p.update(self.wind)

        self.particles = [
            p for p in self.particles
            if 0 <= p.x < WIDTH and 0 <= p.y < HEIGHT
        ]



def render(engine: WeatherEngine):
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for p in engine.particles:
        x, y = int(p.x), int(p.y)
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[y][x] = f"[{p.color}]{p.char}[/]"

    return "\n".join("".join(row) for row in grid)



def handle_key(engine, key):
    if key == "q":
        sys.exit(0)
    elif key == "a":
        engine.wind -= 0.05
    elif key == "d":
        engine.wind += 0.05
    elif key == "w":
        engine.intensity = min(1.0, engine.intensity + 0.05)
    elif key == "s":
        engine.intensity = max(0.05, engine.intensity - 0.05)
    elif key == "r":
        engine.mode = "rain"
    elif key == "n":
        engine.mode = "snow"


def main():
    engine = WeatherEngine()

    try:
        with Live(render(engine), refresh_per_second=30, screen=True) as live:
            while True:
                engine.update()
                live.update(render(engine))
                time.sleep(0.03)

                # Input-Handling
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode("utf-8").lower()
                    handle_key(engine, key)

    except KeyboardInterrupt:
        console.clear()
        console.print("[green]Weather Engine beendet ☁️[/]")

if __name__ == "__main__":
    main()
