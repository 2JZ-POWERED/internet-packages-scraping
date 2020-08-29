class Package:
    def __init__(self, volume, duration, price):
        self.price = price
        self.volume = volume
        self.duration = duration

    is_time_limited = False
    is_local = False

    description = None

    def price_per_gig(self):
        return int(self.price / self.volume * 1024)

    def price_per_month(self):
        return int(self.price / self.duration * 30 * 24)

    def __str__(self) -> str:
        return ('Local' if self.is_local else 'nLocal') + ' - ' \
               + ((str(self.duration) + 'H') if self.duration < 24 else (str(int(self.duration / 24)) + 'D')) + ' - ' \
               + str(self.volume) + 'MB - ' \
               + str(self.price) + 'T - ' \
               + str(self.price_per_gig()) + 'T/G ' \
               + str(self.price_per_month()) + 'T/M ' \
               + self.description
