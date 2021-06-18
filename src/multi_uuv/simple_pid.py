class Controller():
    def __init__(self, p_gain=1.0, i_gain=0.0, d_gain=0.0):
        self.p_gain = p_gain
        self.i_gain = i_gain
        self.d_gain = d_gain
        self.saturation = [-100, 100]
        self.integral_limits = [-100, 100]
        self._integral = 0.0

    def update(self, error, dt):
        self._update_integral(error, dt)
        u = error * self.p_gain + self._integral
        u = max(self.saturation[0], min(self.saturation[1], u))
        return u

    def _update_integral(self, error, dt):
        delta_integral = dt * error * self.i_gain
        self._integral = max(
            self.integral_limits[0],
            min(self.integral_limits[1], self._integral + delta_integral))

    @property
    def saturation(self):
        return self._saturation

    @saturation.setter
    def saturation(self, boundaries):
        lower = float(boundaries[0])
        upper = float(boundaries[1])
        if lower > upper:
            self._saturation = [upper, lower]
        else:
            self._saturation = [lower, upper]

    @property
    def integral_limits(self):
        return self._integral_limits

    @integral_limits.setter
    def integral_limits(self, boundaries):
        lower = float(boundaries[0])
        upper = float(boundaries[1])
        if lower > upper:
            self._integral_limits = [upper, lower]
        else:
            self._integral_limits = [lower, upper]

    @property
    def p_gain(self):
        return self._p_gain

    @p_gain.setter
    def p_gain(self, value):
        self._p_gain = float(value)

    @property
    def i_gain(self):
        return self._i_gain

    @i_gain.setter
    def i_gain(self, value):
        self._i_gain = float(value)

    @property
    def d_gain(self):
        return self._d_gain

    @d_gain.setter
    def d_gain(self, value):
        self._d_gain = float(value)
