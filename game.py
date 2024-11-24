import pygame
import sys
import os

class Player:
    def __init__(self, position, radius, speed, idle_sprite_path, run_sprite_path, scale=1.0):
        self.position = pygame.Vector2(position)
        self.radius = radius
        self.speed = speed
        self.scale = scale  # Add scale attribute

        # Load animation frames
        self.idle_sprites = self.load_frames(idle_sprite_path, 22)  # Adjust 22 to the number of idle frames you have
        self.run_sprites = self.load_frames(run_sprite_path, 8)  # Run animation has 8 frames
        self.current_sprite = 0
        self.idle_timer = 0
        self.run_timer = 0
        self.idle_animation_speed = 100  # milliseconds between frames
        self.run_animation_speed = 50  # milliseconds between frames for run animation
        self.moving = False

    def load_frames(self, path, frame_count):
        """Loads the frames for the animation."""
        frames = []
        for i in range(frame_count):
            frame_path = os.path.join(path, f"{i:02}.png")
            try:
                # Load frame and scale it
                frame = pygame.image.load(frame_path).convert_alpha()
                if self.scale != 1.0:
                    frame = pygame.transform.scale(frame, (int(frame.get_width() * self.scale), 
                                                            int(frame.get_height() * self.scale)))
                frames.append(frame)
            except pygame.error as e:
                print(f"Error loading frame {i:02}.png: {e}")
        return frames

    def handle_movement(self, dt):
        """Handles player movement."""
        keys = pygame.key.get_pressed()
        self.moving = False

        
        if keys[pygame.K_a]:
            self.position.x -= self.speed * dt
            self.moving = True
        if keys[pygame.K_d]:
            self.position.x += self.speed * dt
            self.moving = True

    def check_border_collision(self, screen_width, screen_height):
        """Checks and handles border collision."""
        if self.position.x - self.radius < 0:  # Left border
            self.position.x = self.radius
        if self.position.x + self.radius > screen_width:  # Right border
            self.position.x = screen_width - self.radius
        if self.position.y - self.radius < 0:  # Top border
            self.position.y = self.radius
        if self.position.y + self.radius > screen_height:  # Bottom border
            self.position.y = screen_height - self.radius

    def draw(self, screen, dt):
        """Draws the player character to the screen."""
        sprite_x = int(self.position.x - (self.run_sprites[0].get_width() / 2))
        sprite_y = int(self.position.y - (self.run_sprites[0].get_height() / 2))

        if not self.moving:
            # Idle animation logic
            self.idle_timer += dt * 1000  # Convert dt to milliseconds for proper timing
            if self.idle_timer >= self.idle_animation_speed:
                self.idle_timer = 0
                self.current_sprite = (self.current_sprite + 1) % len(self.idle_sprites)

            # Draw the current idle frame
            screen.blit(self.idle_sprites[self.current_sprite], (sprite_x, sprite_y))
        else:
            # Running animation logic
            self.idle_timer = 0
            # Update sprite frame for run animation, make sure index is within bounds
            self.current_sprite = (self.current_sprite + 1) % len(self.run_sprites)

            # Draw the current run frame
            screen.blit(self.run_sprites[self.current_sprite], (sprite_x, sprite_y))




class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([700, 600])
        pygame.display.set_caption("Game Name")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.player = Player(
            position=(self.screen.get_width() / 2, self.screen.get_height() / 2),
            radius=40,
            speed=300,
            idle_sprite_path="C:/Users/Eu/Documents/JogoPlataforma/player/idle",  # Path to your idle frames
            run_sprite_path="C:/Users/Eu/Documents/JogoPlataforma/player/run",  # Path to your run frames
            scale=3  # changes the scale
        )
        self.dt = 0

    def run(self):
        """Runs the main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Calculate delta time
            self.dt = self.clock.get_time() / 1000  # Convert ms to seconds

            # Handle movement and collisions
            self.player.handle_movement(self.dt)
            self.player.check_border_collision(self.screen.get_width(), self.screen.get_height())

            # Clear screen
            self.screen.fill((0, 0, 255))  # Blue background

            # Draw the player
            self.player.draw(self.screen, self.dt)

            # Update display
            pygame.display.flip()

            # Limit frame rate
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
