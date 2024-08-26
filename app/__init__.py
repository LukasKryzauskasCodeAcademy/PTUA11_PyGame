import pygame

pygame.init()
from config import Config
from .Fighter import Fighter, HealthBar
from .Drawing import Drawer, DamageText, green, red, white, screen, screen_width, bottom_panel, screen_height
from .Button import Button
from .Audio import AudioPlayer

conf = Config()

# Parameters
fps = conf.FPS

# Group is similar to python list
damage_text_group = pygame.sprite.Group()
drawer = Drawer()


def combat_loop():
    # Parameters
    clock = pygame.time.Clock()

    # Create each fighter object
    knight = Fighter(200, 260, 'Knight', 30, 10, 3)
    bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
    bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)
    bandit_list = [bandit1, bandit2]

    # Create each fighters healthBar
    knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
    bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
    bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

    # Define game variables
    current_fighter = 1  # 1- player
    total_fighters = len(bandit_list) + current_fighter
    action_cooldown = 0
    action_wait_time = 90
    potion_effect = 15
    clicked = False
    game_over = 0

    # Function for game loop

    run = True
    while run:

        clock.tick(fps)
        # Draw background
        drawer.draw_bg()
        # Draw panel
        drawer.draw_panel(knight, bandit_list)
        knight_health_bar.draw(knight.hp, screen)
        bandit1_health_bar.draw(bandit1.hp, screen)
        bandit2_health_bar.draw(bandit2.hp, screen)
        # Create buttons
        potion_button = Button(screen, 100, screen_height - bottom_panel + 70, drawer.potion_img, 64, 64)
        restart_button = Button(screen, 330, 120, drawer.restart_img, 120, 30)

        # Draw Fighters
        knight.update()
        knight.draw(screen)
        for bandit in bandit_list:
            bandit.update()
            bandit.draw(screen)

        # Draw damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        # Control player actions
        # Reset action variables
        attack = False
        potion = False
        target = None
        # Make sure mouse is Visible
        pygame.mouse.set_visible(True)
        # Get mouse position
        pos = pygame.mouse.get_pos()
        for count, bandit in enumerate(bandit_list):
            if bandit.rect.collidepoint(pos):
                # Hide mouse
                pygame.mouse.set_visible(False)
                # Show sword in place of mouse cursor
                screen.blit(drawer.sword_img, pos)
                if clicked and bandit.alive:
                    attack = True
                    target = bandit_list[count]

        # Draw buttons
        if potion_button.draw():
            potion = True
        drawer.draw_text(str(knight.potions), red, 150, screen_height - bottom_panel + 70)

        if game_over == 0:
            # Player action
            if knight.alive:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        # Look for player action
                        # Attack
                        if attack and target is not None:
                            knight.attack(target)
                            AudioPlayer.sword_hit.play()

                            current_fighter += 1
                            action_cooldown = 0
                        # Potion
                        if potion:
                            if knight.potions > 0:
                                # Check if potion would heal beyond max hp
                                if knight.max_hp - knight.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = knight.max_hp - knight.hp
                                knight.hp += heal_amount
                                knight.potions -= 1
                                AudioPlayer.potion.play()
                                # Healing text
                                damage_text = DamageText(knight.rect.centerx, knight.rect.y,
                                                         str(heal_amount),
                                                         green)
                                damage_text_group.add(damage_text)

                                current_fighter += 1
                                action_cooldown = 0
            else:
                game_over = -1

            # Enemy action
            for count, bandit in enumerate(bandit_list):
                if current_fighter == 2 + count:
                    if bandit.alive:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                            # Check if bandit needs to heal
                            if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                                # Check if potion would heal beyond max hp
                                if bandit.max_hp - bandit.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = bandit.max_hp - bandit.hp
                                bandit.hp += heal_amount
                                bandit.potions -= 1
                                AudioPlayer.potion.play()
                                # Healing text
                                damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount),
                                                         green)
                                damage_text_group.add(damage_text)

                                current_fighter += 1
                                action_cooldown = 0
                            # Attack
                            else:
                                bandit.attack(knight)
                                AudioPlayer.sword_hit.play()
                                current_fighter += 1
                                action_cooldown = 0
                    else:
                        current_fighter += 1

            # If all fighter had a turn
            if current_fighter > total_fighters:
                current_fighter = 1

        # Check if all bandits are dead
        alive_bandits = 0
        for bandit in bandit_list:
            if bandit.alive:
                alive_bandits += 1
        if alive_bandits == 0:
            game_over = 1

        # Check if game is over
        if game_over != 0:
            if game_over == 1:
                screen.blit(drawer.victory_img, (250, 50))
            elif game_over == -1:
                screen.blit(drawer.defeat_img, (290, 50))
            if restart_button.draw():
                knight.reset()
                for bandit in bandit_list:
                    bandit.reset()
                current_fighter = 1
                action_cooldown = 0
                game_over = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()


class CreateApp:
    # Parameters
    pygame.display.set_caption(conf.APP_NAME)

    # Game variables
    game_paused = False
    menu_state = "main"

    # Create button instances
    resume_button = Button(screen, 304, 125, drawer.resume_img, 191, 82)
    options_button = Button(screen, 297, 250, drawer.options_img, 205, 82)
    quit_button = Button(screen, 336, 375, drawer.quit_img, 128, 82)

    audio_button = Button(screen, 225, 200, drawer.audio_img, 349, 82)
    back_button = Button(screen, 332, 450, drawer.back_img, 135, 82)

    # Game loop
    run = True
    while run:
        screen.fill((52, 78, 91))

        # Check if game is paused
        if game_paused:
            # Check menu state
            if menu_state == "main":
                # Display pause screen menu
                if resume_button.draw():
                    game_paused = False
                if options_button.draw():
                    menu_state = "options"
                if quit_button.draw():
                    run = False
            else:
                # Display options menu
                if audio_button.draw():
                    pass
                if back_button.draw():
                    menu_state = "main"
        else:
            # Keep running the game
            drawer.draw_text("Press ESC to pause", white, 320, 250)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    # combat_loop()

    pygame.quit()
