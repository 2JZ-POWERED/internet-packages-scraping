class Package:
    def __init__(self, volume, duration, price):
        self.price = price
        self.volume = volume
        self.duration = duration

    is_time_limited = False
    is_local = False

    description = None

    def price_per_gig(self) -> int:
        return int(self.price / self.volume * 1024)

    def price_per_month(self) -> int:
        return int(self.price / self.duration * 30 * 24)

    def __repr__(self) -> str:
        return f'{"LCL" if self.is_local else "INT"} ' \
               f' {str(self.duration) + "H" if self.duration < 24 else str(int(self.duration / 24)) + "D":>4} ' \
               f' {self.volume:>6} MB  {self.price:>6} T ' \
               f' {self.price_per_gig():>7} T/G  {self.price_per_month():>7} T/M ' \
               f' {("Time: " + self.description) if self.description else ""}'
