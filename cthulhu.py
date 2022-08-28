import serial

class CthulhuShield(object):

  N_CHANNELS = 18

  REMAP = [
    15, 16, 17, 18,
    11, 12, 13, 14,
    7,   8,  9, 10,
    3,   4,  5,  6,
         1,  2
  ]

  def __init__(self, port='/dev/tty.usbmodem114401'):
    self.ard = serial.Serial(port, 9600, timeout=5)
    self.ard.flush()

  def stim(self, idxes):
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
