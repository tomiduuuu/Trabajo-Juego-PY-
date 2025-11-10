import random
from perlin_noise import PerlinNoise
import Configuracion as s

def place_tree(world_data, x, y_surface, biome_type="forest"):
    if biome_type == "forest":
        tree_height = random.randint(4, 6)
        for i in range(tree_height):
            if y_surface - i >= 0:
                world_data[x][y_surface - i] = s.BLOCK_WOOD
        
        leaf_top_y = y_surface - tree_height
        for lx in range(x - 2, x + 3):
            for ly in range(leaf_top_y - 2, leaf_top_y + 2):
                if 0 <= lx < s.WORLD_WIDTH and 0 <= ly < s.WORLD_HEIGHT:
                    if world_data[lx][ly] == s.BLOCK_AIR:
                        world_data[lx][ly] = s.BLOCK_LEAVES
                        
    elif biome_type == "jungle":
        tree_height = random.randint(6, 8)
        for i in range(tree_height):
            if y_surface - i >= 0:
                world_data[x][y_surface - i] = s.BLOCK_JUNGLE_WOOD
        
        leaf_top_y = y_surface - tree_height
        for lx in range(x - 3, x + 4):
            for ly in range(leaf_top_y - 3, leaf_top_y + 3):
                if 0 <= lx < s.WORLD_WIDTH and 0 <= ly < s.WORLD_HEIGHT:
                    if abs(lx - x) + abs(ly - leaf_top_y) < 4:  # Forma más redondeada
                        if world_data[lx][ly] == s.BLOCK_AIR:
                            world_data[lx][ly] = s.BLOCK_JUNGLE_LEAVES

def generate_structure(world_data, start_x, start_y, structure_type):
    """Genera estructuras en el mundo"""
    if structure_type == "castle":
        # Torres del castillo
        for tower_x in [start_x, start_x + 8]:
            for y in range(start_y - 15, start_y):
                if 0 <= tower_x < s.WORLD_WIDTH and 0 <= y < s.WORLD_HEIGHT:
                    world_data[tower_x][y] = s.BLOCK_STONE
        
        # Paredes
        for wall_x in range(start_x, start_x + 9):
            if 0 <= wall_x < s.WORLD_WIDTH:
                world_data[wall_x][start_y] = s.BLOCK_STONE
                
        # Puerta
        world_data[start_x + 4][start_y] = s.BLOCK_AIR
        world_data[start_x + 4][start_y - 1] = s.BLOCK_AIR
        
    elif structure_type == "house":
        # Base de la casa
        for x in range(start_x, start_x + 5):
            for y in range(start_y - 4, start_y):
                if 0 <= x < s.WORLD_WIDTH and 0 <= y < s.WORLD_HEIGHT:
                    world_data[x][y] = s.BLOCK_WOOD
        
        # Techo
        for x in range(start_x - 1, start_x + 6):
            if 0 <= x < s.WORLD_WIDTH and 0 <= start_y - 5 < s.WORLD_HEIGHT:
                world_data[x][start_y - 5] = s.BLOCK_WOOD
        
        # Puerta
        world_data[start_x + 2][start_y - 1] = s.BLOCK_AIR
        world_data[start_x + 2][start_y - 2] = s.BLOCK_AIR

def generate_world():
    print("Generando mundo (esto puede tardar un momento)...")
    seed = random.randint(0, 10000)
    height_noise = PerlinNoise(octaves=4, seed=seed)
    biome_noise = PerlinNoise(octaves=1, seed=seed + 1)
    resource_noise = PerlinNoise(octaves=8, seed=seed + 2)
    cave_noise = PerlinNoise(octaves=5, seed=seed + 3)
    structure_noise = PerlinNoise(octaves=3, seed=seed + 4)

    world_data = []
    
    for x in range(s.WORLD_WIDTH):
        column = []
        biome_val = biome_noise(x / 200.0)  # Más variación en biomas
        height_val = height_noise(x / 50.0)
        structure_val = structure_noise(x / 100.0)
        
        base_height = s.WORLD_HEIGHT - 50 
        height = int(height_val * 30 + base_height)  # Más variación en altura
        
        # Determinar bioma basado en el valor de ruido
        if biome_val < -0.3:
            biome_type = "desert"
            height += int(height_val * 10)
        elif biome_val < -0.1:
            biome_type = "plains"
        elif biome_val < 0.1:
            biome_type = "forest"
        elif biome_val < 0.3:
            biome_type = "jungle"
            height -= int(height_val * 10)
        else:
            biome_type = "mountain"
            height -= int(height_val * 40)
            
        for y in range(s.WORLD_HEIGHT):
            block_id = s.BLOCK_AIR
            cave_val = cave_noise([x / 30.0, y / 30.0])

            if y < height: 
                block_id = s.BLOCK_AIR
            elif y == height:  # Superficie
                if biome_type == "forest": 
                    block_id = s.BLOCK_GRASS
                elif biome_type == "desert": 
                    block_id = s.BLOCK_DESERT_SAND
                elif biome_type == "plains": 
                    block_id = s.BLOCK_GRASS
                elif biome_type == "jungle": 
                    block_id = s.BLOCK_JUNGLE_GRASS
                elif biome_type == "mountain": 
                    if y < base_height - 20: 
                        block_id = s.BLOCK_SNOW
                    else:
                        block_id = s.BLOCK_STONE
            elif y < height + 4:  # Subsuelo superficial
                if biome_type == "desert": 
                    block_id = s.BLOCK_SAND
                elif biome_type == "jungle":
                    block_id = s.BLOCK_MUD
                else:
                    block_id = s.BLOCK_DIRT
            else:  # Roca madre
                block_id = s.BLOCK_STONE
            
            # Generar cuevas
            if y > height + 1 and cave_val > 0.2:
                block_id = s.BLOCK_AIR

            # Generar recursos según profundidad y bioma
            if block_id == s.BLOCK_STONE:
                res_val = resource_noise([x / 15.0, y / 15.0])
                depth_ratio = y / s.WORLD_HEIGHT
                
                # Minerales básicos (más comunes)
                if res_val > 0.4: block_id = s.BLOCK_COAL
                if res_val > 0.42: block_id = s.BLOCK_COPPER_ORE
                if res_val > 0.45: block_id = s.BLOCK_TIN_ORE
                
                # Minerales más profundos
                if res_val > 0.48 and depth_ratio > 0.6: block_id = s.BLOCK_IRON_ORE
                if res_val > 0.5 and depth_ratio > 0.7: block_id = s.BLOCK_SILVER_ORE
                if res_val > 0.52 and depth_ratio > 0.75: block_id = s.BLOCK_GOLD_ORE
                if res_val > 0.55 and depth_ratio > 0.85: block_id = s.BLOCK_DIAMOND_ORE
                if res_val > 0.58 and depth_ratio > 0.9: block_id = s.BLOCK_PLATINUM_ORE
                
                # Recursos especiales por bioma
                if res_val > 0.35 and biome_type == "mountain" and depth_ratio > 0.5: 
                    block_id = s.BLOCK_MANA_CRYSTAL
                if res_val > 0.38 and depth_ratio > 0.6: 
                    block_id = s.BLOCK_RUNE_ORE

            # Vegetación superficial por bioma
            if block_id in [s.BLOCK_GRASS, s.BLOCK_JUNGLE_GRASS]:
                 res_val = resource_noise([x / 10.0, y / 10.0])
                 if res_val > 0.35 and biome_type == "forest": 
                    block_id = s.BLOCK_SHADOW_MUSHROOM
                    
            column.append(block_id)
        world_data.append(column)
    
    print("Plantando árboles y generando estructuras...")
    for x in range(1, s.WORLD_WIDTH - 1):
        surface_y = None
        for y in range(s.WORLD_HEIGHT - 1, 1, -1):
            if world_data[x][y] in [s.BLOCK_GRASS, s.BLOCK_JUNGLE_GRASS, s.BLOCK_DESERT_SAND]:
                surface_y = y
                break
                
        if surface_y:
            # Determinar bioma local para árboles
            biome_val = biome_noise(x / 200.0)
            if biome_val < -0.3:
                biome_type = "desert"
            elif biome_val < 0.1:
                biome_type = "forest"
            elif biome_val < 0.3:
                biome_type = "jungle"
            else:
                biome_type = "mountain"
            
            # Generar árboles
            if biome_type in ["forest", "jungle"] and random.random() < 0.1:
                place_tree(world_data, x, surface_y, biome_type)
            
            # Generar estructuras
            structure_val = structure_noise(x / 100.0)
            if abs(structure_val) > 0.7 and x > 100 and x < s.WORLD_WIDTH - 100:
                if structure_val > 0.7 and random.random() < 0.01:
                    generate_structure(world_data, x, surface_y, "castle")
                elif structure_val < -0.7 and random.random() < 0.02:
                    generate_structure(world_data, x, surface_y, "house")
                
    print("¡Mundo generado!")
    return world_data

def find_spawn_y(world_data, x):
    for y in range(s.WORLD_HEIGHT - 1): 
        if world_data[x][y] != s.BLOCK_AIR:
            return y - 3 
    return s.WORLD_HEIGHT // 2