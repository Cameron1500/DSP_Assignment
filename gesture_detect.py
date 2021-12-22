import numpy as np

class GestureDetect:
    def __init__(self, threshold, wait_samples=100):
        self.threshold = threshold
        self.pos = False
        self.neg = False

        # Number of samples below threshold before gesture is guessed
        self.wait_samples = 100
        self.sample_count = 0

        # Record Peaks
        self.tracking = False
        self.inital_peak = 0
        self.peak_count = 0

    def processSample(self, sample):
        # Current Signs
        pos = sample >= self.threshold
        neg = sample <= -self.threshold

        # Determine Peak Start/Stop
        if (pos and not self.pos) or (neg and not self.neg): # Start of positive/negative peak
            tracking = True

        if self.pos and not pos: # End of positive peak
            if self.peak_count == 0:
                self.inital_peak = 1
            self.peak_count += 1
        if self.neg and not neg: # End of negative peak
            if self.peak_count == 0:
                self.inital_peak = -1
            self.peak_count += 1

        # Wait for Movement to stop
        if (not pos) and (not neg):
            self.sample_count = 0
        else:
            self.sample_count += 1
        
        # Guess Gesture
        if self.sample_count >= self.wait_samples:
            # Guess Movement
            if self.peak_count <= 2:
                print("Moved ", end="")
                if self.inital_peak:
                    print("Left.")
                else:
                    print("Right.")
            elif self.peak_count > 3:
                print("Device shook {} times.".format(int(self.peak_count/2)))

            # Reset
            self.tracking = False
            self.sample_count = 0
            self.peak_count = 0

        # Update Trackings
        self.pos = pos
        self.neg = neg        