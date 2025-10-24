import pygame
import math
import random

# Importar las secciones del juego (¡CON NOMBRES EN ESPAÑOL!)
import Configuracion as s
import GeneracionDeMundo as world_gen
import UtilidadesDelMundo as world_utils
import Jugador as player_module
import Entidades as entities
import Ui as ui

def main():
    # --- Inicialización ---
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
    pygame.display.set_caption("Voxel World 2D - Modular")
    clock = pygame.time.Clock()
    
    # Fuentes y UI
    font_ui = pygame.font.SysFont(None, 24)
    font_title = pygame.font.SysFont(None, 50)
    notification_manager = ui.NotificationManager(font_ui)
    
    # --- Creación del Mundo ---
    world_data = world_gen.generate_world()
    spawn_x = s.WORLD_WIDTH // 2
    spawn_y = world_gen.find_spawn_y(world_data, spawn_x)
    
    # --- Entidades ---
    player = player_module.Player(spawn_x, spawn_y)
    enemies = []
    
    # --- Variables de Juego ---
    offset_x, offset_y = 0, 0
    running = True
    game_state = "class_selection" 
    
    # Control de movimiento
    moving_left = False
    moving_right = False
    
    # Control de Día/Noche
    game_time = 0
    day_duration = s.DAY_NIGHT_DURATION 
    is_night = False
    
    # Control de Crafteo y Ataque
    crafting_ui = ui.CraftingUI(s.RECIPES, font_ui, notification_manager)
    attack_timer = 0

    while running:
        
        # --- Actualizar Reloj y Tiempo de Juego ---
        dt = clock.tick(60) / 1000.0 # Delta time en segundos
        
        if game_state == "playing":
            game_time = (game_time + dt) % day_duration
            was_day = not is_night
            is_night = game_time > (day_duration / 2)
            
            # Evento: Se hace de noche
            if is_night and was_day:
                notification_manager.add_notification("Se ha hecho de noche...", (255, 100, 100))
                # Spawnear enemigos
                for _ in range(5):
                    ex_col = (player.rect.x // s.TILE_SIZE) + random.randint(-20, 20)
                    if 0 < ex_col < s.WORLD_WIDTH:
                        ey = world_gen.find_spawn_y(world_data, ex_col)
                        if ey < s.WORLD_HEIGHT - 5: # No spawnear en el vacío
                            enemies.append(entities.Zombie(ex_col * s.TILE_SIZE, (ey - 1) * s.TILE_SIZE))
            
            # Evento: Se hace de día
            if not is_night and not was_day:
                notification_manager.add_notification("Amanece...", (255, 255, 100))
                enemies.clear() # Despawnear

        # --- Manejo de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # --- TECLAS PRESIONADAS ---
            if event.type == pygame.KEYDOWN:
                if game_state == "playing":
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        moving_left = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        moving_right = True
                    if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                        if not player.inventory_open: player.jump()
                    
                    if event.key == pygame.K_f:
                        if not player.inventory_open and attack_timer <= 0:
                            player.attack()
                            attack_timer = 0.5 
                            
                            attack_rect = player.get_attack_rect()
                            for enemy in enemies[:]: 
                                if enemy.rect.colliderect(attack_rect):
                                    enemy.take_damage(player, 25) 
                                    if enemy.health <= 0:
                                        enemies.remove(enemy)
                                        player.add_xp(50)

                    if event.key == pygame.K_e:
                        player.inventory_open = not player.inventory_open
                    
                    if event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        player.hotbar_selected = event.key - pygame.K_1 
                        
                elif game_state == "class_selection":
                    if event.key == pygame.K_1: player.set_clase("Guerrero"); game_state = "playing"
                    if event.key == pygame.K_2: player.set_clase("Mago"); game_state = "playing"
                    if event.key == pygame.K_3: player.set_clase("Alquimista"); game_state = "playing"
                    if event.key == pygame.K_4: player.set_clase("Arquero"); game_state = "playing"

            # --- TECLAS SOLTADAS ---
            if event.type == pygame.KEYUP:
                if game_state == "playing":
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        moving_left = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        moving_right = False

            # --- Rueda del Ratón ---
            if event.type == pygame.MOUSEWHEEL:
                if game_state == "playing" and not player.inventory_open:
                    if event.y > 0: player.hotbar_selected = (player.hotbar_selected - 1) % 9
                    elif event.y < 0: player.hotbar_selected = (player.hotbar_selected + 1) % 9

            # --- Clics del Ratón ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "playing":
                    mx, my = pygame.mouse.get_pos()
                    
                    if player.inventory_open:
                        clicked_recipe = crafting_ui.check_click(mx, my, player)
                        if clicked_recipe:
                            ui.craft_item(player, clicked_recipe, notification_manager)
                    
                    else:
                        gx = (mx + offset_x) // s.TILE_SIZE
                        gy = (my + offset_y) // s.TILE_SIZE
                        
                        if event.button == 1: 
                            world_utils.modify_block(world_data, player, gx, gy, s.BLOCK_AIR, notification_manager)
                        if event.button == 3: 
                            block_to_place = player.get_selected_block_id()
                            if block_to_place:
                                world_utils.modify_block(world_data, player, gx, gy, block_to_place, notification_manager)
                
        # --- Lógica del Juego ---
        if game_state == "playing":
            if attack_timer > 0:
                attack_timer -= dt

            if not player.inventory_open:
                player.update(world_data, moving_left, moving_right)
            else:
                player.vx = 0 
            
            offset_x = player.rect.x - (s.WIDTH // 2) + (player.rect.width // 2)
            offset_y = player.rect.y - (s.HEIGHT // 2) + (player.rect.height // 2)

            for enemy in enemies[:]:
                enemy.update(world_data, player.rect)
                if enemy.rect.colliderect(player.rect) and not player.invincible:
                    player.take_damage(10, notification_manager)
            
            player.update_invincibility(dt)

        # --- Dibujado ---
        night_overlay = pygame.Surface((s.WIDTH, s.HEIGHT))
        if is_night:
            darkness = max(0, min(180, (game_time - (day_duration / 2)) * 10))
            night_overlay.set_alpha(darkness)
        else:
            darkness = max(0, 180 - (game_time * 10))
            night_overlay.set_alpha(darkness)
        night_overlay.fill((0, 0, 30))
        
        screen.fill(s.SKY)
        world_utils.draw_world(screen, world_data, offset_x, offset_y)
        
        player.draw(screen, offset_x, offset_y)
        for enemy in enemies:
            enemy.draw(screen, offset_x, offset_y)

        screen.blit(night_overlay, (0, 0))

        if game_state == "playing":
            ui.draw_hud(screen, player, font_ui)
            if player.inventory_open:
                ui.draw_inventory_screen(screen, player, font_ui, font_title, crafting_ui)
        elif game_state == "class_selection":
            ui.draw_class_selection(screen, font_ui, font_title)
            
        notification_manager.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
