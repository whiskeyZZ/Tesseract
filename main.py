import pygame

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.start()

    def start(self):

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("black")

            self.draw_field()

            pygame.display.flip()

    def draw_field(self):
        pygame.draw.line(self.screen, (255, 255, 255), (0, 0), (self.screen_width // 4, self.screen_height // 3), width=2 )
        pygame.draw.line(self.screen, (255, 255, 255), (0, self.screen_height), (self.screen_width // 4, (self.screen_height // 3) * 2), width=2 )
        pygame.draw.line(self.screen, (255, 255, 255), (self.screen_width, 0), ((self.screen_width // 4) * 3, self.screen_height // 3), width=2 )
        pygame.draw.line(self.screen, (255, 255, 255), (self.screen_width, self.screen_height), ((self.screen_width // 4) * 3, (self.screen_height // 3) * 2), width=2 )
        pygame.draw.line(self.screen, (255, 255, 255), (self.screen_width // 4, self.screen_height // 3), (self.screen_width // 4, (self.screen_height // 3) * 2))
        pygame.draw.line(self.screen, (255, 255, 255), (self.screen_width // 4, self.screen_height // 3), ((self.screen_width // 4) * 3, self.screen_height // 3))
        pygame.draw.line(self.screen, (255, 255, 255), ((self.screen_width // 4) * 3, (self.screen_height // 3) * 2), (self.screen_width // 4, (self.screen_height // 3) * 2), width=2 )
        pygame.draw.line(self.screen, (255, 255, 255), ((self.screen_width // 4) * 3, (self.screen_height // 3) * 2), ((self.screen_width // 4) * 3, self.screen_height // 3), width=2 )
                       
Main()