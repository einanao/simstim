from datetime import datetime, timezone
import time
import sys
import json
import os
import argparse

import numpy as np
import pygame
from pygame.locals import *

from cthulhu import CthulhuShield


LOG_DIR = 'logs'

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)


def get_current_iso_time():
  return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


class NumpyJSONEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, np.bool_):
      return bool(obj)
    if isinstance(obj, np.int64):
      return int(obj)
    if isinstance(obj, np.ndarray):
      return obj.tolist()
    return json.JSONEncoder.default(self, obj)


class CthulhuGrid(object):

  N_CHANNELS = 18

  def __init__(self, shield, display, scale=20, radius=10, log_dir=LOG_DIR, exp_name=None):
    assert shield.N_CHANNELS == self.N_CHANNELS

    if exp_name is None:
      timestamp = get_current_iso_time()
      exp_name = '%s.json' % timestamp

    self.shield = shield
    self.display = display
    self.radius = radius
    self.log_path = os.path.join(log_dir, '%s.json' % timestamp)

    ys = np.arange(0, self.N_CHANNELS, 1) // 4
    xs = np.concatenate((np.tile(np.arange(0, 4, 1), 4), [1, 2]))
    self.poses = np.concatenate((xs[:, np.newaxis], ys[:, np.newaxis]), axis=1)
    self.poses *= scale
    self.poses += scale
    assert self.poses.shape[0] == self.N_CHANNELS

    self.log = []
    self.reveal = True
    self.n_resets = 0

  def render(self):
    for i, s in enumerate(self.states):
      if self.reveal:
        p = self.pattern[i]
        if s and not p:
          color = RED
        elif not s and p:
          color = BLUE
        elif s and p:
          color = GREEN
        else:
          color = GRAY
      else:
        color = BLACK if s else GRAY
      pygame.draw.circle(self.display, color, self.poses[i,:], self.radius)

  def save(self):
    with open(self.log_path, 'w') as f:
      json.dump(self.log, f, cls=NumpyJSONEncoder)

  def record(self, event):
    event['timestamp'] = time.time()
    self.log.append(event)
    self.save()
    print(event)

  def toggle(self, idx):
    self.states[idx] = not self.states[idx]
    self.record({'name': 'toggle', 'idx': idx})

  def click(self, pos):
    pos = np.array(pos)
    dists = np.linalg.norm(pos[np.newaxis, :]-self.poses, axis=1)
    idxes = np.where(dists < self.radius)[0]
    assert len(idxes) <= 1
    if len(idxes) == 1:
      idx = idxes[0]
      self.toggle(idx)

  def submit(self):
    if not self.reveal:
      self.reveal = True
      self.record({'name': 'submit'})

  def sample(self):
    n = len(self.states)
    k = np.random.choice(list(range(1, 1+n)))
    pattern = np.zeros(n).astype(bool)
    pattern[:k] = True
    np.random.shuffle(pattern)
    return pattern

  def reset(self):
    if self.reveal:
      self.states = np.zeros(self.N_CHANNELS).astype(bool)
      self.reveal = False
      self.pattern = self.sample()
      on_idxes = np.where(self.pattern)[0]
      self.shield.stim(on_idxes)
      self.record({'name': 'reset', 'pattern': self.pattern, 'states': self.states})
      self.n_resets += 1
      print('n_resets: %d' % self.n_resets)


parser = argparse.ArgumentParser()
parser.add_argument('--debug_mode', action='store_true')
parser.add_argument('--log_dir', type=str, default=LOG_DIR)
parser.add_argument('--exp_name', type=str, default=None)
def main():
  args = parser.parse_args()

  if not os.path.exists(args.log_dir):
    os.makedirs(args.log_dir)

  pygame.init()

  FPS = 30
  FramePerSec = pygame.time.Clock()

  display = pygame.display.set_mode((100,125))
  display.fill(WHITE)

  shield = CthulhuShield(debug_mode=args.debug_mode)
  shield.stop()
  grid = CthulhuGrid(shield, display, log_dir=args.log_dir, exp_name=args.exp_name)
  grid.reset()
  while True:
    grid.render()
    pygame.display.update()
    for event in pygame.event.get():
      if event.type == MOUSEBUTTONDOWN:
        grid.click(event.pos)
      elif event.type == KEYDOWN:
        if event.key == pygame.K_RETURN:
          grid.submit()
        elif event.key == pygame.K_RIGHT:
          grid.reset()
      elif event.type == QUIT:
        grid.save()
        shield.stop()
        pygame.quit()
        sys.exit()

    FramePerSec.tick(FPS)


if __name__ == '__main__':
  main()
