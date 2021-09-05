class GcDataStructure:
    def __init__(self):
        self.linear_usd_oil=0.0
        self.linear_oil_usd=0.0
        self.nonlinear_usd_oil=0.0
        self.nonlinear_oil_usd=0.0

    def set_linear(self, data):
        self.linear_usd_oil=data[0]
        self.linear_oil_usd=data[1]

    def set_nonlinear(self, data):
        self.nonlinear_usd_oil=data[0]
        self.nonlinear_oil_usd=data[1]

