import serial
import time


class CthulhuShield(object):

  N_CHANNELS = 18

  REMAP = [
    15, 16, 17, 18,
    11, 12, 13, 14,
    7,   8,  9, 10,
    3,   4,  5,  6,
         1,  2
  ]

  def __init__(self, port='/dev/tty.usbmodem114401', debug_mode=False, conn_delay=3):
    self.debug_mode = debug_mode
    if not self.debug_mode:
      self.ard = serial.Serial(port, 9600, timeout=5)
      self.ard.flush()
      time.sleep(conn_delay)

  def stim(self, idxes):
    if not self.debug_mode:
      packet = bytearray()
      if idxes == []:
        packet.append(0)
      else:
        for i in idxes:
          packet.append(self.REMAP[i])
      packet.append(0)
      self.ard.write(packet)

  def stop(self):
    self.stim([])
