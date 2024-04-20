# -*- coding : utf8 -*-
import pygame as pg


def dprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def get_pygame_attribut(entier: int):
    for attribut in dir(pg):
        if attribut[0] in "AZERTYUIOPMLKJUHGFDSQWXCVBN":
            if entier == getattr(pg, attribut):
                dprint("Event:", attribut)
                return


pg.init()
screen = pg.display.set_mode((800, 480), pg.RESIZABLE, 24)

dprint([att for att in dir(screen) if att[0] not in "AZERTYUIOPMLKJUHGFDSQWXCVBN"])

clock = pg.time.Clock()

running: bool = True
new_fps: str = ""
last_fps: str = ""
w: int = 0
h: int = 0
w, h = screen.get_size()
# quarterscreen = screen.subsurface(0, 0, w//2, h//2)
quarterscreen = pg.Surface((w//2, h//2))
quarterscreen.fill((20, 60, 30))
pg.draw.line(quarterscreen, (10, 250, 10), (0, 0), (w//2, h//2), 1)
pg.draw.line(quarterscreen, (10, 250, 10), (w//2, 0), (0, h//2), 1)

x, y = 0, 0
dx = 1
while running:
    if x > 400 or x < 0:
        dx *= -1
    x += dx
    screen.fill((20, 30, 60))
    screen.blit(quarterscreen, (x, y))
    pg.display.update()

    fps = clock.tick(25)
    new_fps = f"{clock.get_fps():3.0f} FPS"
    if new_fps != last_fps:
        pg.display.set_caption(new_fps)
        last_fps = new_fps

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type in [pg.WINDOWCLOSE, 
                pg.JOYDEVICEADDED, 
                pg.AUDIODEVICEADDED,
                pg.AUDIO_S8,
                pg.AUDIO_S16,
                pg.ACTIVEEVENT,
                pg.TEXTEDITING,
                pg.VIDEOEXPOSE,
                pg.WINDOWENTER,
                pg.WINDOWSHOWN,
                pg.WINDOWMOVED,
                pg.WINDOWMINIMIZED,
                pg.WINDOWRESTORED,
                pg.WINDOWFOCUSGAINED, 
                pg.WINDOWFOCUSLOST]:
            pass
        elif event.type in [pg.VIDEORESIZE]:
            w, h = screen.get_size()
            quarterscreen = screen.subsurface(0, 0, w//2, h//2)
        elif event.type in [pg.KMOD_LGUI]:
            pass 
        elif event.type in [pg.MOUSEWHEEL]:
            pass 
        elif event.type in [pg.MOUSEBUTTONDOWN]:
            pass 
        elif event.type in [pg.MOUSEBUTTONUP]:
            pass 
        elif event.type in [pg.KEYDOWN]:
            pass 
        elif event.type in [pg.KEYUP]:
            if event.key == pg.K_ESCAPE:
                running = False
        else:
            get_pygame_attribut(event.type)


pg.quit()
