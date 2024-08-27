from sys import modules

import pygame
from tkinter import messagebox

pygame.init()
from config import Config
from .fighter import Fighter, HealthBar
from .drawing import Drawer, DamageText, draw_text, screen, screen_width, bottom_panel, screen_height
from .widgets import Button, Slider
from .audio import AudioPlayer, set_music_volume
from .save_system import SaveFile
from .db import Database, engine
from sqlalchemy.orm import Session

conf = Config()
save = SaveFile()

with Session(engine(conf.SQLALCHEMY_DATABASE_URI)) as session:
    database = Database(session)

# Parameters
clock = pygame.time.Clock()
fps = conf.FPS

# Game variables
game_paused = True
menu_state = "main"

# Group is similar to python list
damage_text_group = pygame.sprite.Group()
drawer = Drawer()
audio = AudioPlayer(save.save_data["music_volume"], save.save_data["effects_volume"])


def menu():
    global game_paused, menu_state
    # Create button instances
    play_button = Button(screen, screen_width / 2 - 100, 200, drawer.button_img, 200, 80)
    resume_button = Button(screen, screen_width / 2 - 100, 200, drawer.button_img, 200, 80)
    options_button = Button(screen, screen_width / 2 - 75, 300, drawer.button_img, 150, 80)
    quit_button = Button(screen, screen_width / 2 - 75, 400, drawer.button_img, 150, 80)

    audio_button = Button(screen, screen_width / 2 - 150, 200, drawer.button_img, 300, 80)
    back_button = Button(screen, screen_width / 2 - 65, 450, drawer.button_img, 130, 80)

    # Audio slider
    music_slider = Slider((screen_width // 2, screen_height // 2 - 100), (200, 30), audio.music_volume, 0, 1)
    effects_slider = Slider((screen_width // 2, screen_height // 2), (200, 30), audio.effects_volume, 0, 1)
    sliders = [music_slider, effects_slider]

    # Game loop
    run = True
    while run:
        clock.tick(fps)
        screen.fill((52, 78, 91))
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()  # 0-Left click, 1-Middle click, 2-Right click
        # Check if game is paused
        if game_paused:
            # Check menu state
            if menu_state == "main":
                # Display main menu
                draw_text("Pygame rpg project", "red", 290, 100)
                if play_button.draw("Play"):
                    menu_state = "pause"
                    game_paused = False
                    audio.load_music("Combat")
                    combat_loop()
                if options_button.draw("Options"):
                    menu_state = "optionsmain"
                if quit_button.draw("Quit"):
                    if messagebox.askquestion('Are you sure?', 'Do you want to quit?') == messagebox.YES:
                        save.save()
                        run = False
                        pygame.quit()
            elif menu_state == "pause":
                # Display pause screen menu
                if resume_button.draw("Resume"):
                    game_paused = False
                if options_button.draw("Options"):
                    menu_state = "optionspause"
                if quit_button.draw("Quit"):
                    if messagebox.askquestion('Are you sure?',
                                              'Do you want to save before quitting?') == messagebox.YES:
                        save.save()
                    run = False
                    menu_state = "main"
                    audio.load_music("Menu")
            elif menu_state == "optionspause" or menu_state == "optionsmain":
                # Display options menu
                if audio_button.draw("Audio"):
                    menu_state = "audio"
                if back_button.draw("Back"):
                    menu_state = menu_state[7:]
            elif menu_state == "audio":
                draw_text("Music", "white", screen_width // 2 - 35, screen_height // 2 - 150)
                draw_text("Sound Effects", "white", screen_width // 2 - 70, screen_height // 2 - 50)
                for count, slider in enumerate(sliders):
                    if slider.container_rect.collidepoint(mouse_pos) and mouse[0]:
                        slider.move_slider(mouse_pos)
                        if count == 0:
                            set_music_volume(slider.get_value())
                            save.save_data["music_volume"] = slider.get_value()
                        elif count == 1:
                            audio.set_effects_volume(slider.get_value())
                            save.save_data["effects_volume"] = slider.get_value()
                    slider.render(screen)
                if back_button.draw("Back"):
                    menu_state = "options"
        else:
            game_paused = False
            run = False

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
            if event.type == pygame.QUIT:
                save.save()
                run = False
        pygame.display.update()


def combat_loop():
    global game_paused, menu_state
    # Create each fighter object
    enemy1 = database.read(1)
    enemy2 = database.read(2)
    knight = Fighter(200, 260, 'Knight', 30, 10, 3)
    bandit1 = Fighter(550, 270, enemy1.name, enemy1.max_hp, enemy1.strength, enemy1.potions)
    bandit2 = Fighter(700, 270, enemy2.name, enemy2.max_hp, enemy2.strength, enemy2.potions)
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
    game_over = 0

    # Function for game loop

    run = True
    while run:
        clock.tick(fps)

        if game_paused:
            menu()
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
        mouse = pygame.mouse.get_pressed()  # 0-Left click, 1-Middle click, 2-Right click
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
                if mouse[0] and bandit.alive:
                    attack = True
                    target = bandit_list[count]

        # Draw buttons
        if potion_button.draw():
            potion = True
        draw_text(str(knight.potions), "red", 150, screen_height - bottom_panel + 70)

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
                            audio.sword_hit.play()

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
                                audio.potion.play()
                                # Healing text
                                damage_text = DamageText(knight.rect.centerx, knight.rect.y,
                                                         str(heal_amount),
                                                         "green")
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
                                audio.potion.play()
                                # Healing text
                                damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount),
                                                         "green")
                                damage_text_group.add(damage_text)

                                current_fighter += 1
                                action_cooldown = 0
                            # Attack
                            else:
                                bandit.attack(knight)
                                audio.sword_hit.play()
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
                    menu_state = "pause"
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()


def run_game():
    # Parameters
    pygame.display.set_caption(conf.APP_NAME)
    menu()
    pygame.quit()
