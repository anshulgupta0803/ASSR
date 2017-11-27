#!/usr/bin/env python
import ASSR
import sys

ac = ASSR.AudioCorrection(sys.argv[1], 'tfSessions/2017-11-26-20:08:45-0.870725/session.ckpt')
ac.process()
ac.saveCorrectedAudio()
