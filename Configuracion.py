# --- Archivo de Configuración (Configuracion.py) ---
# Contiene todas las constantes y datos de "diseño"

# --- Configuración General ---
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 20
GRAVITY = 0.5
PLAYER_REACH = 5 
DAY_NIGHT_DURATION = 120 # Duración total del ciclo en segundos (2 minutos)

# --- Configuración del Mundo ---
WORLD_WIDTH, WORLD_HEIGHT = 800, 200 

# --- IDs de Bloques ---
BLOCK_AIR = 0
BLOCK_GRASS = 1
BLOCK_DIRT = 2
BLOCK_STONE = 3
BLOCK_SAND = 4
BLOCK_SNOW = 5
BLOCK_COAL = 6      
BLOCK_MANA_CRYSTAL = 7 
BLOCK_SHADOW_MUSHROOM = 8 
BLOCK_RUNE_ORE = 9 
BLOCK_WOOD = 10 
BLOCK_LEAVES = 11
BLOCK_IRON_ORE = 12     
BLOCK_GOLD_ORE = 13     
BLOCK_DIAMOND_ORE = 14  

# --- Colores (Diseño) ---
COLORS = {
    # Bloques
    BLOCK_AIR: (135, 206, 235), 
    BLOCK_GRASS: (34, 139, 34),
    BLOCK_DIRT: (139, 69, 19),
    BLOCK_STONE: (100, 100, 100),
    BLOCK_SAND: (237, 201, 175),
    BLOCK_SNOW: (250, 250, 250),
    BLOCK_COAL: (50, 50, 50),
    BLOCK_MANA_CRYSTAL: (100, 100, 255),
    BLOCK_SHADOW_MUSHROOM: (128, 0, 128),
    BLOCK_RUNE_ORE: (255, 100, 0),
    BLOCK_WOOD: (101, 67, 33),
    BLOCK_LEAVES: (0, 100, 0),
    BLOCK_IRON_ORE: (210, 180, 140), 
    BLOCK_GOLD_ORE: (255, 215, 0), 
    BLOCK_DIAMOND_ORE: (185, 242, 255),
    
    # Items (no-bloques)
    "Tablon de Madera": (153, 102, 51),
    "Palo": (139, 69, 19),
    "Pico de Madera": (200, 200, 150),
    "Pico de Piedra": (150, 150, 150),
    "Pico de Hierro": (210, 210, 210),
    "Pico de Diamante": (200, 255, 255),
}
SKY = COLORS[BLOCK_AIR]

# --- Nombres de Items y Bloques ---
# Usado por el inventario
BLOCK_NAMES = {
    BLOCK_GRASS: "Pasto",
    BLOCK_DIRT: "Tierra",
    BLOCK_STONE: "Piedra",
    BLOCK_SAND: "Arena",
    BLOCK_SNOW: "Nieve",
    BLOCK_COAL: "Carbon",
    BLOCK_MANA_CRYSTAL: "Cristal de Mana",
    BLOCK_SHADOW_MUSHROOM: "Hongo Sombrio",
    BLOCK_RUNE_ORE: "Mena Runica",
    BLOCK_WOOD: "Madera",
    BLOCK_LEAVES: "Hojas",
    BLOCK_IRON_ORE: "Mena de Hierro",
    BLOCK_GOLD_ORE: "Mena de Oro",
    BLOCK_DIAMOND_ORE: "Mena de Diamante",
    
    # Nombres de Items (para que coincidan)
    "Tablon de Madera": "Tablon de Madera",
    "Palo": "Palo",
    "Pico de Madera": "Pico de Madera",
    "Pico de Piedra": "Pico de Piedra",
    "Pico de Hierro": "Pico de Hierro",
    "Pico de Diamante": "Pico de Diamante",
}

# --- Base de Datos de Recetas ---
RECIPES = {
    "Tablon de Madera": { "materials": { "Madera": 1 }, "result": "Tablon de Madera", "count": 4 },
    "Palo": { "materials": { "Tablon de Madera": 2 }, "result": "Palo", "count": 4 },
    "Pico de Madera": { "materials": { "Tablon de Madera": 3, "Palo": 2 }, "result": "Pico de Madera", "count": 1 },
    "Pico de Piedra": { "materials": { "Piedra": 3, "Palo": 2 }, "result": "Pico de Piedra", "count": 1 },
    "Pico de Hierro": { "materials": { "Mena de Hierro": 3, "Palo": 2 }, "result": "Pico de Hierro", "count": 1 },
    "Pico de Diamante": { "materials": { "Mena de Diamante": 3, "Palo": 2 }, "result": "Pico de Diamante", "count": 1 },
}
