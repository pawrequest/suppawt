# serenity.actions.py
"""Actions that can be performed with Firefly and its crew."""

def change_pilot(firefly, pilot):
    """Changes the pilot on a :class:`serenity.ship.Firefly` instance to the
    given value.

    :param firefly: :class:`Firefly <serenity.ship.Firefly>` instance who's
        :attr:`~.ship.Firefly.pilot` attribute is to be changed
    :param pilot: String with the new pilot's name
    """
    # This is a silly example that really should be a method on the object
    firefly.pilot = pilot
