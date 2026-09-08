import pygame
import random
from pathlib import Path

font_path = Path(__file__).parent / "assets" / "PressStart2P-Regular.ttf"
high_score_file = Path(__file__).parent / "high_score.txt"

pygame.init()

def load_high_score():
     try:
        return int(high_score_file.read_text())
     except (FileNotFoundError, ValueError):
          return 0

def save_high_score(high_score):
     high_score_file.write_text(str(high_score))

def create_food(snake_body, snake_size):
    while True:
        food_x = random.randrange(0, 600, snake_size)
        food_y = random.randrange(0, 400, snake_size)

        if (food_x, food_y) not in snake_body:
            return food_x, food_y

screen = pygame.display.set_mode((600,450))
pygame.display.set_caption("Snake")

score_font = pygame.font.Font(str(font_path), 10)
game_over_font = pygame.font.Font(str(font_path), 50)

high_score = load_high_score()

snake_size = 20

game_running = True

Start_Screen = True

snake_speed = 20

def reset_game(snake_size, snake_speed):
    snake_x = 300
    snake_y = 300

    direction_x = 0
    direction_y = -snake_speed

    snake_body = [
        (snake_x, snake_y),
        (snake_x, snake_y + snake_size),
        (snake_x, snake_y + snake_size * 2)
    ]

    food_x, food_y = create_food(snake_body, snake_size)

    score = 0
    game_over = False

    return(
        snake_x,
        snake_y,
        direction_x,
        direction_y,
        snake_body,
        food_x,
        food_y,
        score,
        game_over
    )

(
    snake_x,
    snake_y,
    direction_x,
    direction_y,
    snake_body,
    food_x,
    food_y,
    score,
    game_over
) = reset_game(snake_size, snake_speed)

clock = pygame.time.Clock()

while game_running:
    direction_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                            (
                                snake_x,
                                snake_y,
                                direction_x,
                                direction_y,
                                snake_body,
                                food_x,
                                food_y,
                                score,
                                game_over
                            ) = reset_game(snake_size, snake_speed)

                            direction_changed = True

            elif event.key == pygame.K_q and game_over:
                 game_running = False

            elif event.key == pygame.K_SPACE and Start_Screen:
                 Start_Screen = False
                 direction_changed = True
                  
            elif not Start_Screen and not game_over and not direction_changed:
                if event.key == pygame.K_w and direction_y == 0:
                    direction_x = 0
                    direction_y = -snake_speed
                    direction_changed = True

                elif event.key == pygame.K_a and direction_x == 0:
                    direction_x = -snake_speed
                    direction_y = 0
                    direction_changed = True

                elif event.key == pygame.K_s and direction_y == 0:
                    direction_x = 0
                    direction_y = snake_speed
                    direction_changed = True

                elif event.key == pygame.K_d and direction_x == 0:
                    direction_x = snake_speed
                    direction_y = 0
                    direction_changed = True


    screen.fill((20, 20, 20))

    if Start_Screen:
        Start_Screen_text = game_over_font.render(
            "Snake",
            True,
            (255,255,255)
        )

        Start_button_text = score_font.render(
            "Press Space to Start",
            True,
            (255,255,255)
        )

        screen.blit(Start_Screen_text, (190,160))
        screen.blit(Start_button_text,(210, 220))

    else:
        pygame.draw.rect(
                screen,
                (255,0,0),
                (food_x,food_y,snake_size,snake_size)
            )
        
        for body_x, body_y in snake_body:
            pygame.draw.rect(
                screen,
                (0,255,0),
                (body_x,body_y,snake_size,snake_size)
            )

        if not game_over:
            snake_x += direction_x
            snake_y += direction_y

            new_head = (snake_x, snake_y)
            snake_body.insert(0, new_head)

            if snake_x == food_x and snake_y == food_y:
                score +=1 
                food_x, food_y = create_food(snake_body, snake_size)
            else:
                snake_body.pop()

            hit_self = new_head in snake_body[1:]

            hit_wall = (
                snake_x < 0
                or snake_x >= 600
                or snake_y < 0
                or snake_y >= 400
            )

            if score > high_score:
                high_score = score
                save_high_score(high_score)

            if hit_wall or hit_self:
                game_over = True


        pygame.draw.rect(
            screen,
            (35,35,35),
            (0, 400, 600, 50)
        )

        score_text = score_font.render(
            f"Score: {score}",
            True,
            (255,255,255)
        )

        high_score_text = score_font.render(
            f"High Score: {high_score}",
            True,
            (255,255,255)
        )

        

        screen.blit(score_text, (30,420))
        screen.blit(high_score_text, (440,420))


        if game_over:
            game_over_text = game_over_font.render(
                "Game Over",
                True,
                (255,255,255)
            )
            restart_quit_text = score_font.render(
                "Press R to restart or Q to quit",
                True,
                (255,255,255)
            )

            screen.blit(game_over_text, (80,160))
            screen.blit(restart_quit_text,(140, 220))

    pygame.display.update()
    clock.tick(10)

pygame.quit()