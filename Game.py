import pygame, sys, random

def splash_screen():
    global game_started
    screen.fill(bg_color)
    # Draw the start button
    start_button = pygame.Rect(screen_width / 2 - 50, ((2 * screen_height) / 3) - 25, 100, 50)
    pygame.draw.rect(screen, "black", start_button)

    # Draw the title with stroke
    draw_text_with_stroke('Cole-Pong', font_large, verde_colegial, screen_width / 2 - 150, (screen_height / 3) - 100, 2)

    # Draw the start button text without stroke
    start_text = font_small.render('Start', True, verde_colegial)
    screen.blit(start_text, (screen_width / 2 - 35, ((2 * screen_height) / 3) - 20))

    # Event handling for splash screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                game_started = True  # Start the game when clicking on the button
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_started = True  # Start the game with space bar

    pygame.display.flip()

def end_screen():
    global game_ended, game_started,start_ball_movement
    screen.fill(bg_color)

    # Draw the retry button
    retry_button = pygame.Rect(screen_width / 4 - 50, ((2 * screen_height) / 3) - 25, 100, 50)
    pygame.draw.rect(screen, "black", retry_button)

    # Draw the home button
    home_button = pygame.Rect(3*screen_width / 4 - 50, ((2 * screen_height) / 3) - 25, 100, 50)
    pygame.draw.rect(screen, "black", home_button)

    # Draw the 'You Lost' with stroke
    draw_text_with_stroke('You Lost', font_large, verde_colegial, screen_width / 2 - 122, (screen_height / 3) - 100, 2)

    # Draw the retry button text without stroke
    retry_text = font_small.render('Retry', True, verde_colegial)
    screen.blit(retry_text, (screen_width / 4 - 38, ((2 * screen_height) / 3) - 20))

    # Draw the home button text without a stroke
    home_text = font_small.render('Home', True, verde_colegial)
    screen.blit(home_text, (3*screen_width / 4 - 40, ((2 * screen_height) / 3) - 20))

    # Event handling for end screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if retry_button.collidepoint(event.pos):
                restart()  # Restart the game without going to splash screen
            if home_button.collidepoint(event.pos):
                print('aqui')
                start_ball_movement = False
                game_ended = False
                game_started = False



        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            restart()  # Restart the game when space is pressed

    pygame.display.flip()

def draw_text_with_stroke(text, font, color, x, y, stroke_width):
    """
    Draws text with a stroke by rendering it multiple times with an offset around the main text.
    """
    base_text = font.render(text, True, color)
    # Render stroke text around the base text
    for offset_x in range(-stroke_width, stroke_width + 1):
        for offset_y in range(-stroke_width, stroke_width + 1):
            if offset_x != 0 or offset_y != 0:  # Only render on the outline
                stroke_text = font.render(text, True, "black")
                screen.blit(stroke_text, (x + offset_x, y + offset_y))
    # Render the base text on top
    screen.blit(base_text, (x, y))

def draw_paddle_with_stroke(paddle, paddle_color, stroke_width):
    """
    Draws the paddle with a stroke by first drawing a larger rectangle as the stroke.
    """
    # Draw the stroke (larger rectangle behind the paddle)
    pygame.draw.rect(screen, "black", paddle.inflate(stroke_width*2, stroke_width*2))
    # Draw the original paddle
    pygame.draw.rect(screen, paddle_color, paddle)

def ball_movement():
    global ball_speed_x, ball_speed_y, score, start_ball_movement, game_ended

    if not start_ball_movement:
        return

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle
            score += 1
            ball_speed_y *= -1
            ball_speed_x *= random.choice((1, -1))
            ball_speed_y *= 1.05  # Increase speed slightly

    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        game_ended = True  # Game ends if the ball goes below the screen

def player_movement():
    player.x += player_speed  # Move the player paddle horizontally

    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def restart():
    global ball_speed_x, ball_speed_y, score, start_ball_movement, high_score, game_started, game_ended

    if score > high_score:
        high_score = score

    # Reset ball and player positions
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y, ball_speed_x = 0, 0
    player.centerx = screen_width / 2

    # Reset game variables
    score = 0
    start_ball_movement = False
    game_ended = False  # Game is no longer in the end state
    game_started = True  # Skip splash screen and go directly into gameplay

# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
pygame.mixer.music.load("Music/Banda_Colegial.mp3")
pygame.mixer.music.play(-1,0,600)
clock = pygame.time.Clock()

# Main Window setup
screen_width = int(540 * .75)
screen_height = int(960 * .75)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Cole-Pong')
icon = pygame.image.load('Images/Paw Logo 01 Background Removed.png')
ball_image = pygame.image.load('Images/Paw Logo 01 Background Removed.png').convert_alpha()
ball_image = pygame.transform.scale(ball_image, (30, 30))
pygame.display.set_icon(icon)

# Colors
verde_colegial = (51, 113, 55)
paddle_color = (141, 152, 167)
bg_color = pygame.Color(238, 246, 253)

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)  # Ball (centered)
player = pygame.Rect(screen_width / 2 - 45, screen_height - 20, 100, 15)  # Player paddle

# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0

# Score Variables
score = 0
high_score = 0

# Score Text setup
font_xsmall = pygame.font.Font('Fonts/SourceSansPro-Bold.otf', 18)
font_small = pygame.font.Font('Fonts/SourceSansPro-Bold.otf', 32)
font_medium = pygame.font.Font('Fonts/SourceSansPro-Bold.otf', int(32 * 1.5))
font_large = pygame.font.Font('Fonts/SourceSansPro-Bold.otf', 64)

start_ball_movement = False
game_started = False
game_ended = False

# Main game loop
while True:
    name = "Armando J. Santiago Merle"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed = -6
            if event.key == pygame.K_RIGHT:
                player_speed = 6
            if event.key == pygame.K_SPACE and game_started and not start_ball_movement:
                ball_speed_x = random.choice((-7, 7))
                ball_speed_y = 7 * -1
                start_ball_movement = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 6
            if event.key == pygame.K_RIGHT:
                player_speed -= 6

    if not game_started and not game_ended:
        splash_screen()  # Show splash screen when game hasn't started
    elif game_ended:
        end_screen()  # Show end screen when the game ends
    else:
        if start_ball_movement:
            ball_movement()
        player_movement()

        # Visuals
        screen.fill(bg_color)
        draw_paddle_with_stroke(player, verde_colegial, 2)
        screen.blit(ball_image, ball)

        # Render the current score with stroke
        draw_text_with_stroke(f'{score}', font_large, verde_colegial, screen_width / 2 - 20, 10, 2)

        # Render the high score with stroke
        draw_text_with_stroke(f'High Score: {high_score}', font_xsmall, verde_colegial, (3 * screen_width) / 4 - 15, 10, 2)

        pygame.display.flip()
        clock.tick(60)