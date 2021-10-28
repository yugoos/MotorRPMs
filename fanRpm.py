# import math
# import numpy

from saleae.range_measurements import DigitalMeasurer

_RPM = 'RPM'

class FanRpmMeasurer(DigitalMeasurer):
    supported_measurements = [_RPM]

    # Initialize your measurement extension here
    # Each measurement object will only be used once, so feel free to do all per-measurement initialization here
    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)

        self.previous_bitstate = None
        self.initial_t = None
        self.duration = None
        self.falling_edge_count = None

    # This method will be called one or more times per measurement with batches of data
    # data has the following interface
    #   * Iterate over to get transitions in the form of pairs of `Time`, Bitstate (`True` for high, `False` for low)
    # `Time` currently only allows taking a difference with another `Time`, to produce a `float` number of seconds
    def process_data(self, data):
        for t, bitstate in data:
            # Find the initial bitstate and time
            if self.initial_t is None:
                self.initial_t = t
                self.duration = 0
                self.falling_edge_count = 0
                self.previous_bitstate = bitstate

            else:
                # Calculate the new duration time
                self.duration = t - self.initial_t
                
                # If the current bitstate is low and the previous bitstate is high, count the transition
                if not bitstate and self.previous_bitstate:
                    self.falling_edge_count += 1
                
                #hold bitstate for next iteration
                self.previous_bitstate = bitstate

    # This method is called after all the relevant data has been passed to `process_data`
    # It returns a dictionary of the request_measurements values
    def measure(self):
        values = {}

        if _RPM in self.requested_measurements:
            if float(self.duration) > 0:
                values[_RPM] = int((self.falling_edge_count / 2) / (float(self.duration) / 60))
        return values
