class Robot:
    def __init__(self, pos_x, pos_x_wall, step=0.1, speed_on_start=0, acceleration=999):
        # pozycja na starcie symulacji
        self.pos_x = pos_x
        # pozycja ściany na starcie symulacji
        self.pos_x_wall = pos_x_wall
        # rozmiar kroku symulacji
        self.step = step
        # prędkość na starcie symulacji
        self.speed = speed_on_start
        # prędkość docelowa pojazdu
        self.target_speed = 0
        # przyścpieszenie pojazdu
        self.acceleration = acceleration

    def get_distance(self):
        return abs(self.pos_x_wall - self.pos_x)

    def get_pos(self):
        return self.pos_x

    def next_step(self):

        self.pos_x += self.speed * self.step

        if self.target_speed > self.speed: # przyśpiesz
            # nie przyśpieszaj bardziej niż trzeba
            if self.speed + self.acceleration * self.step >= self.target_speed:
                self.speed = self.target_speed
            else:
                self.speed += self.acceleration * self.step
        elif self.target_speed < self.speed: # zwolnij
            # nie zwalniaj bardziej niż trzeba
            if self.speed - self.acceleration * self.step <= self.target_speed:
                self.speed = self.target_speed
            else:
                self.speed -= self.acceleration * self.step

    def set_target_speed(self, target_speed):
        self.target_speed = target_speed
