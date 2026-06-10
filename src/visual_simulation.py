import pygame
import math
from typing import Any
from .screen import Screen
from .hub import Hub
from .colors import Colors
from .drone_map import DroneMap
from .zone_type import ZoneType


class VisualSimulation:
    """
    Visualizes drone paths on a map using pygame.

    Controls:
        LEFT/RIGHT  : step back/forward one turn
        ESC         : exit simulation
        R           : restart
    """

    def __init__(self,
                 drone_solutions: list[dict[int, tuple[str, tuple[int, int]]]],
                 drone_map: DroneMap) -> None:
        self.drone_solutions = drone_solutions
        self.current_turn = 0
        self.max_turn = self._get_max_turn()
        self.drone_map = drone_map
        self.screen = Screen()
        self._adjust_screen_size()

        self.hovered_hub: Any = None
        self.hovered_connection: Any = None
        self.mouse_pos: tuple[int, int] = (0, 0)

        all_coordinates = self._get_all_coordinates()
        self.min_x = min(coordinate[0] for coordinate in all_coordinates)
        self.min_y = min(coordinate[1] for coordinate in all_coordinates)
        self.max_x = max(coordinate[0] for coordinate in all_coordinates)
        self.max_y = max(coordinate[1] for coordinate in all_coordinates)

    def _get_max_turn(self) -> int:
        if not self.drone_solutions:
            return 0

        return max(turn for solution in self.drone_solutions
                   for turn in solution.keys())

    def _adjust_screen_size(self) -> None:
        """Resize the pygame window so it fits within the physical display."""
        info = pygame.display.Info()
        new_surface = pygame.display.set_mode((info.current_w, info.current_h),
                                              pygame.RESIZABLE)
        self.screen.screen = new_surface
        self.screen.height = info.current_h
        self.screen.width = info.current_w

    def _get_all_coordinates(self) -> list[tuple[int, int]]:
        """Get all drones coordinates"""
        return [hub.coordinates for hub in self.drone_map.hub.values()]

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

    def _dist(self, p1: tuple[float, float], p2: tuple[float, float]) -> float:
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def _dist_point_to_segment(self, new_point: tuple[int, int],
                               point_a: tuple[int, int],
                               point_b: tuple[int, int]) -> float:
        """Distance from point p to segment [a, b]."""
        ax, ay = point_a
        bx, by = point_b
        px, py = new_point
        dx, dy = bx - ax, by - ay
        if dx == 0 and dy == 0:
            return self._dist(new_point, point_a)
        t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy)
                       / (dx * dx + dy * dy)))
        return self._dist(new_point, (ax + t * dx, ay + t * dy))

    def _drones_at_hub(self, hub_name: str, turn: int) -> list[int]:
        """Return list of drone indices present at hub_name at given turn."""
        result = []
        for i, solution in enumerate(self.drone_solutions):
            if turn in solution and solution[turn][0] == hub_name:
                result.append(i)
        return result

    def _drones_on_connection(self, connection: Any, turn: int) -> list[int]:
        """Return drone indices currently on this connection at given turn."""
        result = []
        for i, solution in enumerate(self.drone_solutions):
            turns = sorted(solution.keys())
            for j in range(len(turns) - 1):
                t0, t1 = turns[j], turns[j + 1]
                if t0 <= turn < t1:
                    h0 = solution[t0][0]
                    h1 = solution[t1][0]
                    if ({h0, h1} == {connection.zone_1, connection.zone_2}):
                        result.append(i)
        return result

    def _drones_stopped_on_connection(self, connection: Any,
                                      turn: int) -> list[int]:
        """Drones stopped on a connection (restricted hub gap turn)."""
        result = []
        for i, solution in enumerate(self.drone_solutions):
            if turn in solution:
                continue
            turns = sorted(solution.keys())
            prev = [t for t in turns if t < turn]
            next_ = [t for t in turns if t > turn]
            if not prev or not next_:
                continue
            h0 = solution[prev[-1]][0]
            h1 = solution[next_[0]][0]
            if {h0, h1} == {connection.zone_1, connection.zone_2}:
                result.append(i)
        return result

    def _update_hover(self) -> None:
        """Update hover information"""
        mouse_x, mouse_y = self.mouse_pos
        hubs = self.drone_map.hub

        self.hovered_hub = None
        for hub in hubs.values():
            pos = self._to_screen(hub.coordinates)
            if self._dist((mouse_x, mouse_y), pos) <= 28:
                self.hovered_hub = hub
                self.hovered_connection = None
                return

        self.hovered_connection = None
        if self.drone_map.connection:
            for connection in self.drone_map.connection:
                if connection.zone_1 in hubs and connection.zone_2 in hubs:
                    p1 = self._to_screen(hubs[connection.zone_1].coordinates)
                    p2 = self._to_screen(hubs[connection.zone_2].coordinates)
                    if (self._dist_point_to_segment((mouse_x, mouse_y), p1, p2)
                       <= 10):
                        self.hovered_connection = connection
                        return

    def _draw_connections(self) -> None:
        """Draw connections"""
        hubs = self.drone_map.hub

        for connection in self.drone_map.connection:
            if connection.zone_1 not in hubs or connection.zone_2 not in hubs:
                continue
            p1 = self._to_screen(hubs[connection.zone_1].coordinates)
            p2 = self._to_screen(hubs[connection.zone_2].coordinates)

            is_hovered = (self.hovered_connection is connection)
            color = Colors.ORANGE.value if is_hovered else Colors.PURPLE.value
            width = 5 if is_hovered else 3
            pygame.draw.line(self.screen.screen, color, p1, p2, width)

            drone_count = len(self._drones_stopped_on_connection(
                connection, self.current_turn))
            if drone_count > 0:
                mid_x = (p1[0] + p2[0]) // 2
                mid_y = (p1[1] + p2[1]) // 2
                label = self.screen.font.render(str(drone_count), True,
                                                Colors.WHITE.value)
                self.screen.screen.blit(label,
                                        (mid_x - label.get_width() // 2,
                                         mid_y - label.get_height() // 2))

    @staticmethod
    def _get_hub_edge_color(hub: Hub) -> tuple[int, int, int]:
        if hub.zone == ZoneType.BLOCKED:
            return Colors.RED.value
        if hub.zone == ZoneType.NORMAL:
            return Colors.GREEN.value
        elif hub.zone == ZoneType.RESTRICTED:
            return Colors.YELLOW.value
        return Colors.LIGHT_BLUE.value

    def _draw_hubs(self) -> None:
        """
        Draw hubs into the simulation.
        Each hub has a central part (this color can be changed in metadata) and
        an extra ledge which color represent the hub zone type
        """
        hubs = self.drone_map.hub

        for hub in hubs.values():
            pos = self._to_screen(hub.coordinates)
            is_hovered = (self.hovered_hub is hub)
            radius = Screen.HUB_RADIUS + (6 if is_hovered else 0)

            edge_color = VisualSimulation._get_hub_edge_color(hub)
            pygame.draw.circle(self.screen.screen, hub.color.value,
                               pos, radius)
            pygame.draw.circle(self.screen.screen, edge_color,
                               pos, radius, 2)

            if hub.name == self.drone_map.end_hub.name:
                if hub.color != Colors.LIGHT_YELLOW:
                    star = self.screen.font.render("★", True,
                                                   Colors.LIGHT_YELLOW.value)
                else:
                    star = self.screen.font.render("★", True,
                                                   Colors.LIGHT_YELLOW.value)
                self.screen.screen.blit(star,
                                        (pos[0] - star.get_width() // 2,
                                         pos[1] - star.get_height() // 2))

    def _draw_drones(self) -> None:
        """Draw drones into the simulation"""
        for i, solution in enumerate(self.drone_solutions):
            color = Screen.PATH_COLORS[i % len(Screen.PATH_COLORS)]
            pos = self._interpolate_drone_pos(solution, self.current_turn)
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

        for hub in self.drone_map.hub.values():
            drone_count = len(self._drones_at_hub(hub.name, self.current_turn))
            if drone_count > 0 and hub != self.drone_map.end_hub:
                hub_pos = self._to_screen(hub.coordinates)
                label = self.screen.font.render(str(drone_count), True,
                                                Colors.WHITE.value)
                self.screen.screen.blit(label,
                                        (hub_pos[0] - label.get_width() // 2,
                                         hub_pos[1] - label.get_height() // 2))

    def _interpolate_drone_pos(
         self, solution: dict[int, tuple[str, tuple[int, int]]], turn: float
         ) -> tuple[int, int] | None:
        turns = sorted(solution.keys())
        if not turns:
            return None
        if turn <= turns[0]:
            return self._to_screen(solution[turns[0]][1])
        if turn >= turns[-1]:
            return self._to_screen(solution[turns[-1]][1])
        for i in range(len(turns) - 1):
            t0, t1 = turns[i], turns[i + 1]
            if t0 <= turn <= t1:
                alpha = (turn - t0) / (t1 - t0)
                p0 = self._to_screen(solution[t0][1])
                p1 = self._to_screen(solution[t1][1])
                return (int(p0[0] + (p1[0] - p0[0]) * alpha),
                        int(p0[1] + (p1[1] - p0[1]) * alpha))
        return None

    def _draw_tooltip(self) -> None:
        """Draw info tooltip for hovered hub or connection."""
        lines: list[str] = []

        if self.hovered_hub is not None:
            hub = self.hovered_hub
            drones = self._drones_at_hub(hub.name, self.current_turn)
            lines = [
                f"HUB: {hub.name}",
                f"Coords : {hub.coordinates}",
                f"Max drones : {hub.max_drones}",
                f"Number of drones : {len(drones)}",
            ]

        elif self.hovered_connection is not None:
            connection = self.hovered_connection
            drones = self._drones_on_connection(connection, self.current_turn)
            lines = [
                "CONNECTION",
                f"{connection.zone_1}  <->  {connection.zone_2}",
                f"Max capacity : {connection.max_link_capacity}",
                f"Number of drones : {len(drones)}",
            ]

        else:
            return

        padding = 10
        line_h = self.screen.font.get_height() + 3
        box_w = max(self.screen.font.size(line)[0]
                    for line in lines) + padding * 2
        box_h = len(lines) * line_h + padding * 2

        mouse_x, mouse_y = self.mouse_pos
        bx = mouse_x + 16
        by = mouse_y + 16
        if bx + box_w > self.screen.width:
            bx = mouse_x - box_w - 8
        if by + box_h > self.screen.height:
            by = mouse_y - box_h - 8

        box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        box_surf.fill((20, 20, 35, 210))
        pygame.draw.rect(box_surf, (100, 100, 160, 200),
                         box_surf.get_rect(), 1)
        self.screen.screen.blit(box_surf, (bx, by))

        for j, line in enumerate(lines):
            color = Colors.LIGHT_YELLOW.value if j == 0 else Colors.GREY.value
            surf = self.screen.font.render(line, True, color)
            self.screen.screen.blit(surf,
                                    (bx + padding, by + padding + j * line_h))

    def _draw_ui(self) -> None:
        """Show simulation information:
            - title
            - current turn
            - possible keyboard command
        """
        self.screen.draw_text("FLY-IN VISUALIZER", 20, 10,
                              color=Colors.LIGHT_GREY.value,
                              font=self.screen.title_font)

        self.screen.draw_text(f"Turn: {self.current_turn} / {self.max_turn}",
                              self.screen.width - 150, 10)

        self.screen.draw_text(
            "←/→: STEP  R: RESTART  F: FULL SCREEN  ESC: QUIT",
            20, self.screen.height - 22, color=Colors.GREY.value
        )

        self._draw_hub_legend()

    def _draw_hub_legend(self) -> None:
        """Draw hub legend based on their zone type"""
        legend = [
            (Colors.GREEN,      "Normal"),
            (Colors.YELLOW,     "Restricted"),
            (Colors.LIGHT_BLUE, "Priority"),
            (Colors.RED,        "Blocked"),
        ]

        box_w = 140
        line_h = self.screen.font.get_height()
        box_h = len(legend) * line_h + 18
        start_x = self.screen.width - box_w - 10
        start_y = self.screen.height - box_h - 10

        box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        box_surf.fill((20, 20, 35, 210))
        pygame.draw.rect(box_surf, (100, 100, 160, 200),
                         box_surf.get_rect(), 5)
        self.screen.screen.blit(box_surf, (start_x, start_y))

        for i, (color, label) in enumerate(legend):
            current_y = start_y + 10 + i * line_h
            pygame.draw.circle(self.screen.screen, Colors.BLACK.value,
                               (start_x + 20, current_y + 6), 7)
            pygame.draw.circle(self.screen.screen, color.value,
                               (start_x + 20, current_y + 6), 7, 2)
            self.screen.draw_text(label, start_x + 35, current_y - 2,
                                  color=Colors.GREY.value)

    def _handle_events(self) -> bool:
        """
        Handle the user input:
            - ESC: Quit simulation
            - mouse movement
            - r key: reset the simulation
            - f key: toggle full screen
            - left/right key: move/move back one turn
        """
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_r:
                    self.current_turn = 0

                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()

                if event.key == pygame.K_RIGHT:
                    if self.current_turn < self.max_turn:
                        self.current_turn += 1
                        self.drone_map.print_all_drone_position_and_id(
                            self.current_turn)

                if event.key == pygame.K_LEFT:
                    if self.current_turn > 0:
                        self.current_turn -= 1
                        self.drone_map.print_all_drone_position_and_id(
                            self.current_turn)

        return True

    def run(self) -> None:
        """Run the simulation"""
        print()

        try:
            while self._handle_events():

                screen_width, screen_height = self.screen.screen.get_size()
                if (screen_width != self.screen.width or
                   screen_height != self.screen.height):
                    self.screen.width = screen_width
                    self.screen.height = screen_height

                self._update_hover()

                self.screen.clear_last_frame()

                self._draw_connections()
                self._draw_hubs()
                self._draw_drones()

                self._draw_ui()
                self._draw_tooltip()
                self.screen.display_on_screen()
                self.screen.set_fps(60)

        except KeyboardInterrupt:
            self.screen.exit_simulation()
