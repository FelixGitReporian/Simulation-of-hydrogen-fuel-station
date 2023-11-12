from components.simulatable import Simulatable
from components.serializable import Serializable

class Charger_fc(Serializable, Simulatable):
    '''
    Charging the battery by the fuel cell

    Info: assuming that the charging efficiency and power are static
    '''

    def __init__(self, power_stack,file_path):
        '''

        Parameters
        ----------
        power_stack: float. Charger power from fuel cell stack
        '''

        # Read component parameters from json file
        if file_path:
            self.load(file_path)

        else:
            print('Attention: No json file for power component efficiency specified')

        self.power_stack = power_stack

        # FC stack efficiency
        self.efficiency_bc = self.efficiency_bc

        # Charging efficiency
        self.efficiency = self.efficiency_bc * self.efficiency_stack

        # Charging power value
        self.power = self.power_stack * self.efficiency

        # Compression and transportation efficiency
        self.efficiency_com_tran = self.efficiency_com_tran