import pygame
import maps
from pygame.locals import *
import math
import numpy as np
from random import randint
import player
import camera
import roborange
import holes
import path
import sensors
import gym
from gym import spaces

PATH = False
USE_SENSORS = True
SHOW_SENSORS = True


class Simulation(gym.Env):
    def __init__(self):
        metadata = {'render.modes': ['human']}
        pygame.init()

        self.action_space = spaces.Discrete(4)
        low = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        high = np.array([4000, 4000, 360, 700, 700, 700, 700, 700, 700,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000])

        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        self.score = 0
        self.stepscore = 0
        self.stepcount = 0
        self.holescore = 10

        self.map_s = pygame.sprite.Group()
        self.player_s = pygame.sprite.Group()
        self.path_s = pygame.sprite.Group()
        self.hole_s = pygame.sprite.Group()
        self.range_s = pygame.sprite.Group()
        self.sensor_s = pygame.sprite.Group()
        self.drill = 0

        self.screen = pygame.display.set_mode((1800, 1000))


        self.clock = pygame.time.Clock()
        self.CENTER_X = int(pygame.display.Info().current_w / 2)
        self.CENTER_Y = int(pygame.display.Info().current_h / 2)
        self.running = True
        start_angle = 270
        self.car = player.Player(start_angle)
        self.cam = camera.Camera()
        self.robrange = roborange.RoRange(start_angle)
        self.current_map = maps.Map()
        self.path = path.Path()

        # Sensoren erstellen
        if USE_SENSORS:
            self.sensor1 = sensors.Sensor(0)
            self.sensor2 = sensors.Sensor(30)
            self.sensor3 = sensors.Sensor(150)
            self.sensor4 = sensors.Sensor(180)
            self.sensor5 = sensors.Sensor(210)
            self.sensor6 = sensors.Sensor(330)
            self.sensor_s.add(self.sensor1)
            self.sensor_s.add(self.sensor2)
            self.sensor_s.add(self.sensor3)
            self.sensor_s.add(self.sensor4)
            self.sensor_s.add(self.sensor5)
            self.sensor_s.add(self.sensor6)

            # create new holes
            hole0 = holes.Holes(527, 364)
            hole0.add(self.hole_s)
            hole1 = holes.Holes(1755, 706)
            hole1.add(self.hole_s)
            hole2 = holes.Holes(2431, 377)
            hole2.add(self.hole_s)
            hole3 = holes.Holes(3614, 829)
            hole3.add(self.hole_s)
            hole4 = holes.Holes(1849, 437)
            hole4.add(self.hole_s)
            hole5 = holes.Holes(2092, 1047)
            hole5.add(self.hole_s)
            hole6 = holes.Holes(1432, 1189)
            hole6.add(self.hole_s)
            hole7 = holes.Holes(1775, 986)
            hole7.add(self.hole_s)
            hole8 = holes.Holes(2977, 393)
            hole8.add(self.hole_s)
            hole9 = holes.Holes(885, 554)
            hole9.add(self.hole_s)
            hole10 = holes.Holes(3123, 1100)
            hole10.add(self.hole_s)
            hole11 = holes.Holes(1306, 1293)
            hole11.add(self.hole_s)
            hole12 = holes.Holes(2610, 218)
            hole12.add(self.hole_s)
            hole13 = holes.Holes(3448, 588)
            hole13.add(self.hole_s)
            hole14 = holes.Holes(3635, 1104)
            hole14.add(self.hole_s)
            hole15 = holes.Holes(3307, 1277)
            hole15.add(self.hole_s)
            hole16 = holes.Holes(1853, 881)
            hole16.add(self.hole_s)
            hole17 = holes.Holes(3375, 1260)
            hole17.add(self.hole_s)
            hole18 = holes.Holes(1576, 304)
            hole18.add(self.hole_s)
            hole19 = holes.Holes(1448, 1019)
            hole19.add(self.hole_s)
            hole20 = holes.Holes(2452, 517)
            hole20.add(self.hole_s)
            hole21 = holes.Holes(1066, 1226)
            hole21.add(self.hole_s)
            hole22 = holes.Holes(2484, 1329)
            hole22.add(self.hole_s)
            hole23 = holes.Holes(1109, 1169)
            hole23.add(self.hole_s)
            hole24 = holes.Holes(3345, 1343)
            hole24.add(self.hole_s)
            hole25 = holes.Holes(1224, 381)
            hole25.add(self.hole_s)
            hole26 = holes.Holes(3455, 336)
            hole26.add(self.hole_s)
            hole27 = holes.Holes(2389, 831)
            hole27.add(self.hole_s)
            hole28 = holes.Holes(3071, 212)
            hole28.add(self.hole_s)
            hole29 = holes.Holes(2185, 626)
            hole29.add(self.hole_s)
            hole30 = holes.Holes(3620, 332)
            hole30.add(self.hole_s)
            hole31 = holes.Holes(3669, 1063)
            hole31.add(self.hole_s)
            hole32 = holes.Holes(3381, 394)
            hole32.add(self.hole_s)
            hole33 = holes.Holes(3081, 924)
            hole33.add(self.hole_s)
            hole34 = holes.Holes(2373, 657)
            hole34.add(self.hole_s)
            hole35 = holes.Holes(995, 1490)
            hole35.add(self.hole_s)
            hole36 = holes.Holes(2516, 1225)
            hole36.add(self.hole_s)
            hole37 = holes.Holes(2154, 579)
            hole37.add(self.hole_s)
            hole38 = holes.Holes(2435, 562)
            hole38.add(self.hole_s)
            hole39 = holes.Holes(1207, 476)
            hole39.add(self.hole_s)

            # create list of hole coordinates and IR´s
            self.holestate = []
            for hole in self.hole_s:
                dist_x = hole.x - self.car.x
                dist_y = hole.y - self.car.y
                self.holestate.append(dist_x)
                self.holestate.append(dist_y)
                self.holestate.append(hole.IR)

        # create observation state array
        self.state = np.array([self.car.x, self.car.y, self.car.dir, self.sensor1.delta, self.sensor2.delta,
                               self.sensor3.delta, self.sensor4.delta, self.sensor5.delta, self.sensor6.delta])
        holearray = np.array(self.holestate)
        self.state = np.append(self.state, holearray)

        self.map_s.add(self.current_map)
        self.player_s.add(self.car)
        self.range_s.add(self.robrange)
        self.path_s.add(self.path)
        self.robrange.dir = self.car.dir
        pygame.display.set_caption('RoboSimAI')
        pygame.mouse.set_visible(True)
        self.font = pygame.font.Font(None, 24)

        self.background = pygame.Surface(self.screen.get_size())

        self.background.fill((210, 210, 250))

    def step(self, action):
        # action[0] in range -1, 1: speed
        # action[1] in range -1, 1: steering
        # action[2] in range -1, 1: drill

        self.stepscore = 0
        self.stepcount += 1
        self.holestate = []

        holes_in_range = self.check_collision(self.robrange, self.hole_s, False)
        if holes_in_range:
            for hole in self.hole_s.sprites():
                for hole_IR in holes_in_range:
                    if hole == hole_IR:
                        hole.IR = 4000
                    else:
                        hole.IR = 0
                dist_x = hole.x - self.car.x
                dist_y = hole.y - self.car.y
                self.holestate.append(dist_x)
                self.holestate.append(dist_y)
                self.holestate.append(hole.IR)
        else:
            for hole in self.hole_s.sprites():
                dist_x = hole.x - self.car.x
                dist_y = hole.y - self.car.y
                self.holestate.append(dist_x)
                self.holestate.append(dist_y)
                self.holestate.append(0)



        len_holelist = len(self.holestate)
        append_length = 120 - len_holelist

        if action == 0:
            for hole in holes_in_range:
                self.hole_s.remove(hole)
            self.stepscore += len(holes_in_range)*self.holescore
            self.stepscore -= 4
        if action == 1:
            self.car.speed = 10
            self.robrange.speed = 10
            self.robrange.update()
            self.car.update()
            self.stepscore -= 0.1
        if action == 2:
            self.car.steerleft()
            self.robrange.steerleft()
            self.stepscore -= 0.12
        if action == 3:
            self.car.steerright()
            self.robrange.steerright()
            self.stepscore -= 0.12



        self.path_s.update(self.cam.x, self.cam.y)
        self.hole_s.update(self.cam.x, self.cam.y)
        self.map_s.update(self.cam.x, self.cam.y)

        if USE_SENSORS:
            self.sensor_s.update(self.car.dir, self.CENTER_X, self.CENTER_Y)
            self.measure(self.sensor_s)

        self.cam.set_pos(self.car.x, self.car.y)

        self.score += self.stepscore
        append_length = int(append_length / 3)

        if append_length == 0:
            self.state = np.array([self.car.x, self.car.y, self.car.dir, self.sensor1.delta, self.sensor2.delta,
                                   self.sensor3.delta, self.sensor4.delta, self.sensor5.delta, self.sensor6.delta])
            holearray = np.array(self.holestate)
            self.state = np.append(self.state, holearray)
        else:
            listof0 = [0, 0, 0] * append_length
            self.state = np.array([self.car.x, self.car.y, self.car.dir, self.sensor1.delta, self.sensor2.delta,
                                   self.sensor3.delta, self.sensor4.delta, self.sensor5.delta, self.sensor6.delta])
            holearray = np.array(self.holestate)
            zeroarray = np.array(listof0)
            self.state = np.append(self.state, holearray)
            self.state = np.append(self.state, zeroarray)


        ################################################# render
        pygame.event.pump()
        # Show text data.
        text_fps = self.font.render('FPS: ' + str(int(self.clock.get_fps())), 1, (255, 127, 0))
        textpos_fps = text_fps.get_rect(centery=25, centerx=60)
        text_score = self.font.render("Score: " + str(self.score), 1, (255, 127, 0))
        textpos_score = text_score.get_rect(centery=50, centerx=60)
        if USE_SENSORS:
            text_s1 = self.font.render('S1: ' + str(int(self.sensor1.delta)), 1, (255, 127, 0))
            textpos_s1 = text_s1.get_rect(centery=75, centerx=60)
            text_s2 = self.font.render('S2: ' + str(int(self.sensor2.delta)), 1, (255, 127, 0))
            textpos_s2 = text_s1.get_rect(centery=100, centerx=60)
            text_s3 = self.font.render('S3: ' + str(int(self.sensor3.delta)), 1, (255, 127, 0))
            textpos_s3 = text_s1.get_rect(centery=125, centerx=60)
            text_s4 = self.font.render('S4: ' + str(int(self.sensor4.delta)), 1, (255, 127, 0))
            textpos_s4 = text_s1.get_rect(centery=150, centerx=60)
            text_s5 = self.font.render('S5: ' + str(int(self.sensor5.delta)), 1, (255, 127, 0))
            textpos_s5 = text_s1.get_rect(centery=175, centerx=60)
            text_s6 = self.font.render('S6: ' + str(int(self.sensor6.delta)), 1, (255, 127, 0))
            textpos_s6 = text_s1.get_rect(centery=200, centerx=60)

        self.screen.blit(self.background, (0, 0))
        if PATH:
            self.path.image.fill((255, 127, 0), Rect(self.car.x, self.car.y, 5, 5))

        self.path_s.draw(self.screen)
        self.range_s.draw(self.screen)
        self.map_s.draw(self.screen)
        if SHOW_SENSORS:
            self.sensor_s.draw(self.screen)
        self.player_s.draw(self.screen)
        self.hole_s.draw(self.screen)

        self.screen.blit(text_fps, textpos_fps)
        self.screen.blit(text_score, textpos_score)
        if USE_SENSORS:
            self.screen.blit(text_s1, textpos_s1)
            self.screen.blit(text_s2, textpos_s2)
            self.screen.blit(text_s3, textpos_s3)
            self.screen.blit(text_s4, textpos_s4)
            self.screen.blit(text_s5, textpos_s5)
            self.screen.blit(text_s6, textpos_s6)

        pygame.display.update()
        self.clock.tick(120)
        ############################################################ render
        done = 0
        if self.check_collision(self.car, self.map_s):
            done = 1
            self.car.reset()
            self.stepscore -= 5
        if self.score < -500:
            done = 1
        if self.stepcount > 2500:
            done = 1
        if not self.hole_s.sprites():
            done = 1

        return self.state, self.stepscore, done, {}

    def reset(self):
        self.stepscore = 0
        self.score = 0
        self.stepcount = 0
        self.holestate = []
        self.car.reset()

        if PATH:
            self.path.reset()
        self.score = 0
        self.robrange.reset()
        # reset sensor values
        for r in self.sensor_s:
            r.delta = 700
        # create new holes
        self.hole_s.empty()
        #add holes

        hole0 = holes.Holes(827, 464)
        hole0.add(self.hole_s)
        hole1 = holes.Holes(1755, 706)
        hole1.add(self.hole_s)
        hole2 = holes.Holes(2431, 477)
        hole2.add(self.hole_s)
        hole3 = holes.Holes(3614, 829)
        hole3.add(self.hole_s)
        hole4 = holes.Holes(1849, 437)
        hole4.add(self.hole_s)
        hole5 = holes.Holes(2092, 1047)
        hole5.add(self.hole_s)
        hole6 = holes.Holes(1432, 1189)
        hole6.add(self.hole_s)
        hole7 = holes.Holes(1775, 986)
        hole7.add(self.hole_s)
        hole8 = holes.Holes(2977, 493)
        hole8.add(self.hole_s)
        hole9 = holes.Holes(885, 554)
        hole9.add(self.hole_s)
        hole10 = holes.Holes(3123, 1100)
        hole10.add(self.hole_s)
        hole11 = holes.Holes(1306, 1293)
        hole11.add(self.hole_s)
        hole12 = holes.Holes(2610, 418)
        hole12.add(self.hole_s)
        hole13 = holes.Holes(3448, 588)
        hole13.add(self.hole_s)
        hole14 = holes.Holes(3435, 1104)
        hole14.add(self.hole_s)
        hole15 = holes.Holes(3307, 1277)
        hole15.add(self.hole_s)
        hole16 = holes.Holes(1853, 881)
        hole16.add(self.hole_s)
        hole17 = holes.Holes(3375, 1260)
        hole17.add(self.hole_s)
        hole18 = holes.Holes(1576, 504)
        hole18.add(self.hole_s)
        hole19 = holes.Holes(1448, 1019)
        hole19.add(self.hole_s)
        hole20 = holes.Holes(2452, 517)
        hole20.add(self.hole_s)
        hole21 = holes.Holes(1066, 1226)
        hole21.add(self.hole_s)
        hole22 = holes.Holes(2484, 1329)
        hole22.add(self.hole_s)
        hole23 = holes.Holes(1109, 1169)
        hole23.add(self.hole_s)
        hole24 = holes.Holes(3345, 1343)
        hole24.add(self.hole_s)
        hole25 = holes.Holes(1224, 481)
        hole25.add(self.hole_s)
        hole26 = holes.Holes(3455, 636)
        hole26.add(self.hole_s)
        hole27 = holes.Holes(2389, 831)
        hole27.add(self.hole_s)
        hole28 = holes.Holes(3071, 412)
        hole28.add(self.hole_s)
        hole29 = holes.Holes(2185, 626)
        hole29.add(self.hole_s)
        hole30 = holes.Holes(3620, 432)
        hole30.add(self.hole_s)
        hole31 = holes.Holes(3469, 1063)
        hole31.add(self.hole_s)
        hole32 = holes.Holes(3381, 494)
        hole32.add(self.hole_s)
        hole33 = holes.Holes(3081, 924)
        hole33.add(self.hole_s)
        hole34 = holes.Holes(2373, 657)
        hole34.add(self.hole_s)
        hole35 = holes.Holes(995, 1490)
        hole35.add(self.hole_s)
        hole36 = holes.Holes(2516, 1225)
        hole36.add(self.hole_s)
        hole37 = holes.Holes(2154, 579)
        hole37.add(self.hole_s)
        hole38 = holes.Holes(2435, 562)
        hole38.add(self.hole_s)
        hole39 = holes.Holes(1207, 476)
        hole39.add(self.hole_s)

        # create list of hole coordinates and IR´s

        for hole in self.hole_s:
            dist_x = hole.x - self.car.x
            dist_y = hole.y - self.car.y
            self.holestate.append(dist_x)
            self.holestate.append(dist_y)
            self.holestate.append(hole.IR)

        # create observation state array

        self.state = np.array([self.car.x, self.car.y, self.car.dir, self.sensor1.delta, self.sensor2.delta,
                               self.sensor3.delta, self.sensor4.delta, self.sensor5.delta, self.sensor6.delta])
        holearray = np.array(self.holestate)
        self.state = np.append(self.state, holearray)

        return self.state

    def render(self, mode='human'):
        pass

    def check_collision(self, sprite, sprite_group, dokill=False):
        spritelist = pygame.sprite.spritecollide(sprite, sprite_group, dokill, pygame.sprite.collide_mask)
        if spritelist:
            return spritelist
        else:
            return []

    def measure(self, sensor_s):
        for sensor in sensor_s:
            if sensor.rotangle >= 360:
                sensor.rotangle -= 360
            if sensor.rotangle <= 0:
                dx0 = sensor.rect.bottomleft[0]
                dx1 = sensor.rect.bottomleft[1]
            if 0 < sensor.rotangle <= 90:
                dx0 = sensor.rect.bottomright[0]
                dx1 = sensor.rect.bottomright[1]
            if 90 < sensor.rotangle <= 180:
                dx0 = sensor.rect.topright[0]
                dx1 = sensor.rect.topright[1]
            if 180 < sensor.rotangle <= 270:
                dx0 = sensor.rect.topleft[0]
                dx1 = sensor.rect.topleft[1]
            if 270 < sensor.rotangle < 360:
                dx0 = sensor.rect.bottomleft[0]
                dx1 = sensor.rect.bottomleft[1]

            offset_x = -self.current_map.rect.topleft[0] + sensor.rect.topleft[0]
            offset_y = -self.current_map.rect.topleft[1] + sensor.rect.topleft[1]
            sensor.mask = pygame.mask.from_surface(sensor.image)
            if self.current_map.mask.overlap(sensor.mask, (offset_x, offset_y)) is not None:
                ix, iy = self.current_map.mask.overlap(sensor.mask, (offset_x, offset_y))
                dx = - ix - self.current_map.rect.topleft[0] + dx0
                dy = - iy - self.current_map.rect.topleft[1] + dx1
                sensor.delta = math.sqrt(dx ** 2 + dy ** 2)
                if sensor.delta >= 700:
                    sensor.delta = 700
            else:
                sensor.delta = 700
