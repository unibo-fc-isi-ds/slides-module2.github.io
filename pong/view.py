import pygame

from dpongpy.model import *
from typing import Iterable


def rect(rectangle: Rectangle) -> pygame.Rect:
    return pygame.Rect(rectangle.top_left, rectangle.size)


class PongView:
    def __init__(self, pong: Pong):
        self._pong = pong

    def render(self):
        raise NotImplemented


class ShowNothingPongView(PongView):
    def render(self):
        pass


class ScreenPongView(PongView):
    def __init__(self, pong: Pong, screen: pygame.Surface = None):
        super().__init__(pong)
        self._screen = screen or pygame.display.set_mode(pong.size)

    def render(self):
        self._screen.fill("black")
        self.render_ball(self._pong.ball)
        self.render_paddles(self._pong.paddles)

    def render_ball(self, ball: Ball):
        pygame.draw.ellipse(self._screen, "white", rect(ball.bounding_box), width=0)

    def render_paddles(self, paddles: Iterable[Paddle]):
        for paddle in paddles:
            self.render_paddle(paddle)

    def render_paddle(self, paddle: Paddle):
        pygame.draw.rect(self._screen, "white", rect(paddle.bounding_box), width=0)
