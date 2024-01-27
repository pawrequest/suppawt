# serenity.ship.py
class Firefly:
    """This class represents the ship which might be considered a main
    character.
    """

    def __init__(self, passengers=3):
        """Initialize a Firefly object

        :param passengers: number of passengers aboard
        """
        self.passengers = passengers
        self.direction = 0
        self.pilot = "Wash"

    def crazy_ivan(self):
        """Changes direction by 180 degrees. 

        :returns: new direction
        """
        self.direction = (self.direction + 180) % 360
        return self.direction
