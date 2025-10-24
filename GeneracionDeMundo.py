import random
from perlin_noise import PerlinNoise
import Configuracion as s

# --- Funciones de Generación del Mundo ---

def place_tree(world_data, x, y_surface):
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

def generate_world():
    print("Generando mundo (esto puede tardar un momento)...")
    seed = random.randint(0, 10000)
    height_noise = PerlinNoise(octaves=4, seed=seed)
    biome_noise = PerlinNoise(octaves=2, seed=seed + 1)
    resource_noise = PerlinNoise(octaves=8, seed=seed + 2) 
    cave_noise = PerlinNoise(octaves=5, seed=seed + 3)

    world_data = []
    
    for x in range(s.WORLD_WIDTH):
        column = []
        biome_val = biome_noise(x / 100.0)
        height_val = height_noise(x / 50.0)
        
        base_height = s.WORLD_HEIGHT - 50 
        height = int(height_val * 20 + base_height) 
        
        biome_type = "forest"
        if biome_val > 0.1:
            biome_type = "mountain"
            height -= int(height_val * 25) 
        elif biome_val < -0.1:
            biome_type = "desert"
            height += int(height_val * 5) 
            
        for y in range(s.WORLD_HEIGHT):
            block_id = s.BLOCK_AIR
            cave_val = cave_noise([x / 30.0, y / 30.0])

            if y < height: 
                block_id = s.BLOCK_AIR
            elif y == height: 
                if biome_type == "forest": block_id = s.BLOCK_GRASS
                elif biome_type == "desert": block_id = s.BLOCK_SAND
                elif biome_type == "mountain" and y < base_height - 10: block_id = s.BLOCK_SNOW 
                else: block_id = s.BLOCK_GRASS 
            elif y < height + 4: 
                block_id = s.BLOCK_DIRT if biome_type != "desert" else s.BLOCK_SAND
            else: 
                block_id = s.BLOCK_STONE
            
            if y > height + 1 and cave_val > 0.3:
                block_id = s.BLOCK_AIR

            if block_id == s.BLOCK_STONE:
                res_val = resource_noise([x / 15.0, y / 15.0])
                depth_ratio = y / s.WORLD_HEIGHT
                
                if res_val > 0.45 and depth_ratio > 0.85: block_id = s.BLOCK_DIAMOND_ORE
                elif res_val > 0.42 and depth_ratio > 0.75: block_id = s.BLOCK_GOLD_ORE
                elif res_val > 0.38 and depth_ratio > 0.6: block_id = s.BLOCK_IRON_ORE
                elif res_val > 0.35: block_id = s.BLOCK_COAL
                if res_val > 0.35 and biome_type == "mountain" and depth_ratio > 0.5: block_id = s.BLOCK_MANA_CRYSTAL
                if res_val > 0.38 and depth_ratio > 0.6: block_id = s.BLOCK_RUNE_ORE

            if block_id == s.BLOCK_GRASS and biome_type == "forest":
                 res_val = resource_noise([x / 10.0, y / 10.0])
                 if res_val > 0.35: 
                    block_id = s.BLOCK_SHADOW_MUSHROOM
                    
            column.append(block_id)
        world_data.append(column)
    
    print("Plantando árboles...")
    for x in range(1, s.WORLD_WIDTH - 1):
        for y in range(s.WORLD_HEIGHT - 1, 1, -1):
            if world_data[x][y] == s.BLOCK_GRASS:
                if random.random() < 0.15: # 15% prob
                    place_tree(world_data, x, y)
                break 
                
    print("¡Mundo generado!")
    return world_data

def find_spawn_y(world_data, x):
    for y in range(s.WORLD_HEIGHT - 1): 
        if world_data[x][y] != s.BLOCK_AIR:
            return y - 3 
    return s.WORLD_HEIGHT // 2
