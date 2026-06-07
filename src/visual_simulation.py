import pygame
import math
import time
from typing import Any
from screen import Screen


class VisualSimulation:
    """
    Visualizes drone paths on a map using pygame.

    Controls:
        SPACE       : pause / resume
        R           : restart
        LEFT/RIGHT  : step back / forward one turn (auto-pauses)
        ESC         : quit
    """

    ANIM_SPEED = 1.5
    HOVER_RADIUS = 28
    CONN_HOVER_DIST = 10

    def __init__(self, drone_solutions: list[dict[int, list]],
                 drone_map: Any) -> None:
        self.solutions = drone_solutions
        self.drone_map = drone_map
        self.screen = Screen()

        all_coords = self._get_all_coords()
        self.min_x = min(c[0] for c in all_coords)
        self.max_x = max(c[0] for c in all_coords)
        self.min_y = min(c[1] for c in all_coords)
        self.max_y = max(c[1] for c in all_coords)

        self.max_turn = max(
            max(sol.keys()) for sol in self.solutions if sol
        )

        self.current_turn: float = 0.0
        self.paused = False
        self.last_time = time.time()

        self.hovered_hub: Any | None = None
        self.hovered_connection: Any | None = None
        self.mouse_pos: tuple[int, int] = (0, 0)

    def _get_all_coords(self) -> list[tuple]:
        return [hub.coordinates for hub in self._all_hubs().values()]

    def _all_hubs(self) -> dict:
        hubs = {}
        if self.drone_map.hub:
            hubs.update(self.drone_map.hub)
        hubs[self.drone_map.start_hub.name] = self.drone_map.start_hub
        hubs[self.drone_map.end_hub.name] = self.drone_map.end_hub
        return hubs

    def _to_screen(self, coord: tuple[int, int]) -> tuple[int, int]:
        pad = Screen.PADDING

        dx = self.max_x - self.min_x or 1
        dy = self.max_y - self.min_y or 1

        usable_w = self.screen.width - pad * 2
        usable_h = self.screen.height - pad * 2 - 60

        scale = min(usable_w / dx, usable_h / dy)

        sx = pad + int((coord[0] - self.min_x) * scale)
        sy = pad + 30 + int((coord[1] - self.min_y) * scale)
        return sx, sy

    def _dist(self, p1: tuple, p2: tuple) -> float:
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def _dist_point_to_segment(self, p, a, b) -> float:
        """Distance from point p to segment [a, b]."""
        ax, ay = a
        bx, by = b
        px, py = p
        dx, dy = bx - ax, by - ay
        if dx == 0 and dy == 0:
            return self._dist(p, a)
        t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy)
                       / (dx * dx + dy * dy)))
        return self._dist(p, (ax + t * dx, ay + t * dy))

    def _drones_at_hub(self, hub_name: str, turn: int) -> list[int]:
        """Return list of drone indices present at hub_name at given turn."""
        result = []
        for i, sol in enumerate(self.solutions):
            if turn in sol and sol[turn][0] == hub_name:
                result.append(i)
        return result

    def _drones_on_connection(self, connection: Any, turn: int) -> list[int]:
        """Return drone indices currently on this connection at given turn."""
        result = []
        for i, sol in enumerate(self.solutions):
            turns = sorted(sol.keys())
            for j in range(len(turns) - 1):
                t0, t1 = turns[j], turns[j + 1]
                if t0 <= turn < t1:
                    h0 = sol[t0][0]
                    h1 = sol[t1][0]
                    if ({h0, h1} == {connection.zone_1, connection.zone_2}):
                        result.append(i)
        return result

    def _update_hover(self) -> None:
        mx, my = self.mouse_pos
        hubs = self._all_hubs()

        self.hovered_hub = None
        for hub in hubs.values():
            pos = self._to_screen(hub.coordinates)
            if self._dist((mx, my), pos) <= self.HOVER_RADIUS:
                self.hovered_hub = hub
                self.hovered_connection = None
                return

        self.hovered_connection = None
        if self.drone_map.connection:
            for connection in self.drone_map.connection:
                if connection.zone_1 in hubs and connection.zone_2 in hubs:
                    p1 = self._to_screen(hubs[connection.zone_1].coordinates)
                    p2 = self._to_screen(hubs[connection.zone_2].coordinates)
                    if (self._dist_point_to_segment((mx, my), p1, p2)
                       <= self.CONN_HOVER_DIST):
                        self.hovered_connection = connection
                        return

    def _draw_connections(self) -> None:
        if not self.drone_map.connection:
            return
        hubs = self._all_hubs()

        for connection in self.drone_map.connection:
            if connection.zone_1 not in hubs or connection.zone_2 not in hubs:
                continue
            p1 = self._to_screen(hubs[connection.zone_1].coordinates)
            p2 = self._to_screen(hubs[connection.zone_2].coordinates)

            is_hovered = (self.hovered_connection is connection)
            color = (180, 180, 80) if is_hovered else Screen.CONNECTION_COLOR
            width = 5 if is_hovered else 3
            pygame.draw.line(self.screen.screen, color, p1, p2, width)

    def _draw_paths(self) -> None:
        for i, sol in enumerate(self.solutions):
            color = Screen.PATH_COLORS[i % len(Screen.PATH_COLORS)]
            faint = tuple(max(0, c - 150) for c in color)
            turns = sorted(sol.keys())
            points = [self._to_screen(sol[t][1]) for t in turns]
            if len(points) >= 2:
                pygame.draw.lines(self.screen.screen, faint, False, points, 2)

    def _draw_hubs(self) -> None:
        hubs = self._all_hubs()

        for name, hub in hubs.items():
            pos = self._to_screen(hub.coordinates)
            color = Screen.HUB_COLORS.get(hub.color,
                                          Screen.HUB_COLORS["default"])
            is_hovered = (self.hovered_hub is hub)
            radius = Screen.HUB_RADIUS + (6 if is_hovered else 0)

            # Circle
            border_color = (255, 255, 100) if is_hovered else (255, 255, 255)
            pygame.draw.circle(self.screen.screen, color, pos, radius)
            pygame.draw.circle(self.screen.screen, border_color,
                               pos, radius, 2)

    def _interpolate_drone_pos(self, sol: dict,
                               turn: float) -> tuple[int, int] | None:
        turns = sorted(sol.keys())
        if not turns:
            return None
        if turn <= turns[0]:
            return self._to_screen(sol[turns[0]][1])
        if turn >= turns[-1]:
            return self._to_screen(sol[turns[-1]][1])
        for i in range(len(turns) - 1):
            t0, t1 = turns[i], turns[i + 1]
            if t0 <= turn <= t1:
                alpha = (turn - t0) / (t1 - t0)
                p0 = self._to_screen(sol[t0][1])
                p1 = self._to_screen(sol[t1][1])
                return (int(p0[0] + (p1[0] - p0[0]) * alpha),
                        int(p0[1] + (p1[1] - p0[1]) * alpha))
        return None

    def _draw_drones(self) -> None:
        for i, sol in enumerate(self.solutions):
            color = Screen.PATH_COLORS[i % len(Screen.PATH_COLORS)]
            pos = self._interpolate_drone_pos(sol, self.current_turn)
            if pos is None:
                continue

            glow = pygame.Surface((Screen.DRONE_RADIUS * 6,
                                   Screen.DRONE_RADIUS * 6), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*color, 60),
                               (Screen.DRONE_RADIUS * 3,
                                Screen.DRONE_RADIUS * 3),
                               Screen.DRONE_RADIUS * 3)
            self.screen.screen.blit(glow, (pos[0] - Screen.DRONE_RADIUS * 3,
                                           pos[1] - Screen.DRONE_RADIUS * 3))

            pygame.draw.circle(self.screen.screen, color,
                               pos, Screen.DRONE_RADIUS)
            pygame.draw.circle(self.screen.screen, (255, 255, 255),
                               pos, Screen.DRONE_RADIUS, 2)

            label = self.screen.font.render(f"D{i}", True, (15, 15, 25))
            self.screen.screen.blit(label, (pos[0] - label.get_width() // 2,
                                            pos[1] - label.get_height() // 2))

    def _draw_tooltip(self) -> None:
        """Draw info tooltip for hovered hub or connection."""
        lines = []

        if self.hovered_hub is not None:
            hub = self.hovered_hub
            lines = [
                f"HUB: {hub.name}",
                f"Coords : {hub.coordinates}",
                f"Max drones : {hub.max_drones}",
            ]

        elif self.hovered_connection is not None:
            connection = self.hovered_connection
            lines = [
                "CONNECTION",
                f"{connection.zone_1}  <->  {connection.zone_2}",
                f"Max capacity : {connection.max_link_capacity}",
            ]

        else:
            return

        padding = 10
        line_h = self.screen.font.get_height() + 3
        box_w = max(self.screen.font.size(line)[0]
                    for line in lines) + padding * 2
        box_h = len(lines) * line_h + padding * 2

        mx, my = self.mouse_pos
        bx = mx + 16
        by = my + 16
        # Keep tooltip inside screen
        if bx + box_w > self.screen.width:
            bx = mx - box_w - 8
        if by + box_h > self.screen.height:
            by = my - box_h - 8

        box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        box_surf.fill((20, 20, 35, 210))
        pygame.draw.rect(box_surf, (100, 100, 160, 200),
                         box_surf.get_rect(), 1)
        self.screen.screen.blit(box_surf, (bx, by))

        for j, line in enumerate(lines):
            color = (255, 255, 100) if j == 0 else Screen.TEXT_COLOR
            surf = self.screen.font.render(line, True, color)
            self.screen.screen.blit(surf,
                                    (bx + padding, by + padding + j * line_h))

    def _draw_timeline(self) -> None:
        """Draw a scrubber bar at the bottom."""
        bar_x = Screen.PADDING
        bar_y = self.screen.height - 48
        bar_w = self.screen.width - Screen.PADDING * 2
        bar_h = 6

        pygame.draw.rect(self.screen.screen, (40, 40, 65),
                         (bar_x, bar_y, bar_w, bar_h), border_radius=3)

        progress = self.current_turn / self.max_turn if self.max_turn else 0
        filled_w = int(bar_w * progress)
        if filled_w > 0:
            pygame.draw.rect(self.screen.screen, (100, 140, 255),
                             (bar_x, bar_y, filled_w, bar_h), border_radius=3)

        knob_x = bar_x + filled_w
        pygame.draw.circle(self.screen.screen, (180, 200, 255),
                           (knob_x, bar_y + bar_h // 2), 8)

        for t in range(self.max_turn + 1):
            tx = bar_x + int(bar_w * t /
                             self.max_turn) if self.max_turn else bar_x
            pygame.draw.line(self.screen.screen, (60, 60, 90),
                             (tx, bar_y - 4), (tx, bar_y + bar_h + 4), 1)
            tick_label = self.screen.font.render(str(t), True, (70, 70, 100))
            self.screen.screen.blit(tick_label, (tx - tick_label.get_width()
                                                 // 2, bar_y + bar_h + 6))

    def _draw_ui(self) -> None:
        self.screen.draw_text("FLY-IN VISUALIZER", 20, 10,
                              color=(180, 180, 255),
                              font=self.screen.title_font)

        turn_int = int(self.current_turn)
        self.screen.draw_text(f"Turn: {turn_int} / {self.max_turn}",
                              self.screen.width - 200, 10)

        self.screen.draw_text(
            "SPACE: pause  ←/→: step  R: restart  ESC: quit",
            20, self.screen.height - 22, color=(70, 70, 100)
        )

    def _handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    self.last_time = time.time()

                if event.key == pygame.K_r:
                    self.current_turn = 0.0
                    self.paused = False
                    self.last_time = time.time()

                if event.key == pygame.K_RIGHT:
                    self.paused = True
                    self.current_turn = min(self.max_turn,
                                            math.floor(self.current_turn) + 1)

                if event.key == pygame.K_LEFT:
                    self.paused = True
                    self.current_turn = max(0,
                                            math.ceil(self.current_turn) - 1)

        return True

    def run(self) -> None:
        self.last_time = time.time()

        while self._handle_events():

            now = time.time()
            self.last_time = now

            self._update_hover()

            self.screen.clear()

            self._draw_connections()
            self._draw_paths()
            self._draw_hubs()
            self._draw_drones()

            self._draw_timeline()
            self._draw_ui()
            self._draw_tooltip()
            self.screen.flip()
            self.screen.tick(60)

        self.screen.quit()
