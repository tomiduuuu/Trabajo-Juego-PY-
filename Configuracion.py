# --- Archivo de Configuración (Configuracion.py) ---
import pygame

# --- Configuración General ---
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 20
GRAVITY = 0.5
PLAYER_REACH = 5 
DAY_NIGHT_DURATION = 120

# --- Configuración del Mundo ---
WORLD_WIDTH, WORLD_HEIGHT = 1600, 400

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
BLOCK_COPPER_ORE = 15
BLOCK_TIN_ORE = 16
BLOCK_SILVER_ORE = 17
BLOCK_TUNGSTEN_ORE = 18
BLOCK_PLATINUM_ORE = 19
BLOCK_HELLSTONE = 20
BLOCK_OBSIDIAN = 21
BLOCK_CLAY = 22
BLOCK_MUD = 23
BLOCK_JUNGLE_GRASS = 24
BLOCK_JUNGLE_WOOD = 25
BLOCK_JUNGLE_LEAVES = 26
BLOCK_DESERT_SAND = 27
BLOCK_HARD_SAND = 28
BLOCK_ICE = 29
BLOCK_HARD_ICE = 30

# --- Items y Herramientas ---
ITEM_WOODEN_SWORD = 100
ITEM_STONE_SWORD = 101
ITEM_IRON_SWORD = 102
ITEM_WOODEN_BOW = 103
ITEM_WOODEN_ARROW = 104
ITEM_WOODEN_PICKAXE = 105
ITEM_STONE_PICKAXE = 106
ITEM_IRON_PICKAXE = 107
ITEM_COPPER_PICKAXE = 108
ITEM_SILVER_PICKAXE = 109
ITEM_GOLDEN_PICKAXE = 110
ITEM_WOODEN_AXE = 111
ITEM_STONE_AXE = 112
ITEM_IRON_AXE = 113
ITEM_HEALTH_POTION = 114
ITEM_MANA_POTION = 115

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
    BLOCK_COPPER_ORE: (184, 115, 51),
    BLOCK_TIN_ORE: (192, 192, 192),
    BLOCK_SILVER_ORE: (200, 200, 220),
    BLOCK_TUNGSTEN_ORE: (100, 100, 150),
    BLOCK_PLATINUM_ORE: (150, 200, 255),
    BLOCK_HELLSTONE: (255, 100, 0),
    BLOCK_OBSIDIAN: (30, 30, 40),
    BLOCK_CLAY: (160, 140, 120),
    BLOCK_MUD: (80, 60, 40),
    BLOCK_JUNGLE_GRASS: (0, 80, 0),
    BLOCK_JUNGLE_WOOD: (80, 50, 20),
    BLOCK_JUNGLE_LEAVES: (0, 60, 0),
    BLOCK_DESERT_SAND: (240, 220, 180),
    BLOCK_HARD_SAND: (220, 200, 160),
    BLOCK_ICE: (200, 230, 255),
    BLOCK_HARD_ICE: (180, 210, 240),
    
    # Items
    ITEM_WOODEN_SWORD: (150, 120, 80),
    ITEM_STONE_SWORD: (150, 150, 150),
    ITEM_IRON_SWORD: (200, 200, 200),
    ITEM_WOODEN_BOW: (120, 80, 40),
    ITEM_WOODEN_ARROW: (150, 100, 50),
    ITEM_WOODEN_PICKAXE: (150, 120, 80),
    ITEM_STONE_PICKAXE: (150, 150, 150),
    ITEM_IRON_PICKAXE: (200, 200, 200),
    ITEM_COPPER_PICKAXE: (184, 115, 51),
    ITEM_SILVER_PICKAXE: (200, 200, 220),
    ITEM_GOLDEN_PICKAXE: (255, 215, 0),
    ITEM_WOODEN_AXE: (150, 120, 80),
    ITEM_STONE_AXE: (150, 150, 150),
    ITEM_IRON_AXE: (200, 200, 200),
    ITEM_HEALTH_POTION: (255, 0, 0),
    ITEM_MANA_POTION: (0, 0, 255),
    
    # Materiales básicos
    "Tablon de Madera": (153, 102, 51),
    "Palo": (139, 69, 19),
    "Lingote de Cobre": (184, 115, 51),
    "Lingote de Hierro": (210, 180, 140),
    "Lingote de Oro": (255, 215, 0),
    "Lingote de Plata": (200, 200, 220),
    "Lingote de Platino": (150, 200, 255),
    "Carbon": (50, 50, 50),
    "Cristal de Mana": (100, 100, 255),
    "Hongo Sombrio": (128, 0, 128),
    "Mena Runica": (255, 100, 0),
}

SKY = COLORS[BLOCK_AIR]

# --- Nombres de Items y Bloques ---
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
    BLOCK_COPPER_ORE: "Mena de Cobre",
    BLOCK_TIN_ORE: "Mena de Estaño",
    BLOCK_SILVER_ORE: "Mena de Plata",
    BLOCK_TUNGSTEN_ORE: "Mena de Tungsteno",
    BLOCK_PLATINUM_ORE: "Mena de Platino",
    BLOCK_HELLSTONE: "Piedra Infernal",
    BLOCK_OBSIDIAN: "Obsidiana",
    BLOCK_CLAY: "Arcilla",
    BLOCK_MUD: "Lodo",
    BLOCK_JUNGLE_GRASS: "Pasto de Jungla",
    BLOCK_JUNGLE_WOOD: "Madera de Jungla",
    BLOCK_JUNGLE_LEAVES: "Hojas de Jungla",
    BLOCK_DESERT_SAND: "Arena del Desierto",
    BLOCK_HARD_SAND: "Arena Compacta",
    BLOCK_ICE: "Hielo",
    BLOCK_HARD_ICE: "Hielo Compacto",
    
    # Items
    ITEM_WOODEN_SWORD: "Espada de Madera",
    ITEM_STONE_SWORD: "Espada de Piedra",
    ITEM_IRON_SWORD: "Espada de Hierro",
    ITEM_WOODEN_BOW: "Arco de Madera",
    ITEM_WOODEN_ARROW: "Flecha de Madera",
    ITEM_WOODEN_PICKAXE: "Pico de Madera",
    ITEM_STONE_PICKAXE: "Pico de Piedra",
    ITEM_IRON_PICKAXE: "Pico de Hierro",
    ITEM_COPPER_PICKAXE: "Pico de Cobre",
    ITEM_SILVER_PICKAXE: "Pico de Plata",
    ITEM_GOLDEN_PICKAXE: "Pico de Oro",
    ITEM_WOODEN_AXE: "Hacha de Madera",
    ITEM_STONE_AXE: "Hacha de Piedra",
    ITEM_IRON_AXE: "Hacha de Hierro",
    ITEM_HEALTH_POTION: "Poción de Vida",
    ITEM_MANA_POTION: "Poción de Maná",
    
    # Materiales básicos
    "Tablon de Madera": "Tablon de Madera",
    "Palo": "Palo",
    "Lingote de Cobre": "Lingote de Cobre",
    "Lingote de Hierro": "Lingote de Hierro",
    "Lingote de Oro": "Lingote de Oro",
    "Lingote de Plata": "Lingote de Plata",
    "Lingote de Platino": "Lingote de Platino",
    "Carbon": "Carbon",
    "Cristal de Mana": "Cristal de Mana",
    "Hongo Sombrio": "Hongo Sombrio",
    "Mena Runica": "Mena Runica",
}

# --- Base de Datos de Recetas ---
RECIPES = {
    # Materiales básicos
    "Tablon de Madera": { "materials": { "Madera": 1 }, "result": "Tablon de Madera", "count": 4 },
    "Palo": { "materials": { "Tablon de Madera": 2 }, "result": "Palo", "count": 4 },
    "Lingote de Cobre": { "materials": { "Mena de Cobre": 3 }, "result": "Lingote de Cobre", "count": 1 },
    "Lingote de Hierro": { "materials": { "Mena de Hierro": 3 }, "result": "Lingote de Hierro", "count": 1 },
    "Lingote de Oro": { "materials": { "Mena de Oro": 3 }, "result": "Lingote de Oro", "count": 1 },
    "Lingote de Plata": { "materials": { "Mena de Plata": 3 }, "result": "Lingote de Plata", "count": 1 },
    "Lingote de Platino": { "materials": { "Mena de Platino": 3 }, "result": "Lingote de Platino", "count": 1 },
    
    # Herramientas de Madera
    "Pico de Madera": { "materials": { "Tablon de Madera": 3, "Palo": 2 }, "result": "Pico de Madera", "count": 1 },
    "Hacha de Madera": { "materials": { "Tablon de Madera": 3, "Palo": 2 }, "result": "Hacha de Madera", "count": 1 },
    "Espada de Madera": { "materials": { "Tablon de Madera": 2, "Palo": 1 }, "result": "Espada de Madera", "count": 1 },
    
    # Herramientas de Piedra
    "Pico de Piedra": { "materials": { "Piedra": 3, "Palo": 2 }, "result": "Pico de Piedra", "count": 1 },
    "Hacha de Piedra": { "materials": { "Piedra": 3, "Palo": 2 }, "result": "Hacha de Piedra", "count": 1 },
    "Espada de Piedra": { "materials": { "Piedra": 2, "Palo": 1 }, "result": "Espada de Piedra", "count": 1 },
    
    # Herramientas de Cobre
    "Pico de Cobre": { "materials": { "Lingote de Cobre": 3, "Palo": 2 }, "result": "Pico de Cobre", "count": 1 },
    
    # Herramientas de Hierro
    "Pico de Hierro": { "materials": { "Lingote de Hierro": 3, "Palo": 2 }, "result": "Pico de Hierro", "count": 1 },
    "Hacha de Hierro": { "materials": { "Lingote de Hierro": 3, "Palo": 2 }, "result": "Hacha de Hierro", "count": 1 },
    "Espada de Hierro": { "materials": { "Lingote de Hierro": 2, "Palo": 1 }, "result": "Espada de Hierro", "count": 1 },
    
    # Herramientas de Plata
    "Pico de Plata": { "materials": { "Lingote de Plata": 3, "Palo": 2 }, "result": "Pico de Plata", "count": 1 },
    
    # Herramientas de Oro
    "Pico de Oro": { "materials": { "Lingote de Oro": 3, "Palo": 2 }, "result": "Pico de Oro", "count": 1 },
    
    # Armas a distancia
    "Arco de Madera": { "materials": { "Tablon de Madera": 3, "Palo": 1 }, "result": "Arco de Madera", "count": 1 },
    "Flecha de Madera": { "materials": { "Palo": 1, "Piedra": 1 }, "result": "Flecha de Madera", "count": 5 },
    
    # Pociones
    "Poción de Vida": { "materials": { "Hongo Sombrio": 1, "Cristal de Mana": 1 }, "result": "Poción de Vida", "count": 1 },
    "Poción de Maná": { "materials": { "Cristal de Mana": 2 }, "result": "Poción de Maná", "count": 1 },
    
    # Palas
    "Pala de Madera": { "materials": { "Tablon de Madera": 3, "Palo": 2 }, "result": "Pala de Madera", "count": 1 },
    "Pala de Piedra": { "materials": { "Piedra": 3, "Palo": 2 }, "result": "Pala de Piedra", "count": 1 },
    "Pala de Hierro": { "materials": { "Lingote de Hierro": 3, "Palo": 2 }, "result": "Pala de Hierro", "count": 1 },
    "Pala de Diamante": { "materials": { "Mena de Diamante": 3, "Palo": 2 }, "result": "Pala de Diamante", "count": 1 },
    
    # Hachas
    "Hacha de Madera": { "materials": { "Tablon de Madera": 3, "Palo": 2 }, "result": "Hacha de Madera", "count": 1 },
    "Hacha de Piedra": { "materials": { "Piedra": 3, "Palo": 2 }, "result": "Hacha de Piedra", "count": 1 },
    "Hacha de Hierro": { "materials": { "Lingote de Hierro": 3, "Palo": 2 }, "result": "Hacha de Hierro", "count": 1 },
    "Hacha de Diamante": { "materials": { "Mena de Diamante": 3, "Palo": 2 }, "result": "Hacha de Diamante", "count": 1 },
}

# --- Niveles de Herramientas ---
TOOL_LEVELS = {
    "Pico de Madera": 1,
    "Pico de Piedra": 2,
    "Pico de Cobre": 3,
    "Pico de Hierro": 4,
    "Pico de Plata": 5,
    "Pico de Oro": 6,
}

# --- Dureza de Bloques (tiempo en segundos para minar con la mano) ---
BLOCK_HARDNESS = {
    BLOCK_DIRT: 0.5,
    BLOCK_GRASS: 0.6,
    BLOCK_SAND: 0.5,
    BLOCK_CLAY: 0.8,
    BLOCK_MUD: 0.7,
    BLOCK_WOOD: 1.5,
    BLOCK_LEAVES: 0.2,
    BLOCK_STONE: 3.0,
    BLOCK_COAL: 2.0,
    BLOCK_COPPER_ORE: 3.0,
    BLOCK_IRON_ORE: 4.0,
    BLOCK_SILVER_ORE: 5.0,
    BLOCK_GOLD_ORE: 6.0,
    BLOCK_DIAMOND_ORE: 7.0,
    BLOCK_PLATINUM_ORE: 8.0,
    BLOCK_OBSIDIAN: 15.0,
    BLOCK_MANA_CRYSTAL: 4.0,
    BLOCK_RUNE_ORE: 5.0,
}

# --- Velocidad de Herramientas (multiplicador de velocidad) ---
TOOL_SPEED = {
    "Mano": 1.0,
    "Pico de Madera": 2.0,
    "Pico de Piedra": 3.0,
    "Pico de Cobre": 4.0,
    "Pico de Hierro": 5.0,
    "Pico de Plata": 6.0,
    "Pico de Oro": 7.0,
    "Pico de Diamante": 8.0,
    "Pala de Madera": 2.0,
    "Pala de Piedra": 3.0,
    "Pala de Hierro": 5.0,
    "Pala de Diamante": 8.0,
    "Hacha de Madera": 2.0,
    "Hacha de Piedra": 3.0,
    "Hacha de Hierro": 5.0,
    "Hacha de Diamante": 8.0,
}

# --- Herramientas efectivas por tipo de bloque ---
EFFECTIVE_TOOLS = {
    # Piedra y minerales - Picos
    BLOCK_STONE: ["pico"],
    BLOCK_COAL: ["pico"],
    BLOCK_COPPER_ORE: ["pico"],
    BLOCK_IRON_ORE: ["pico"],
    BLOCK_SILVER_ORE: ["pico"],
    BLOCK_GOLD_ORE: ["pico"],
    BLOCK_DIAMOND_ORE: ["pico"],
    BLOCK_PLATINUM_ORE: ["pico"],
    BLOCK_OBSIDIAN: ["pico"],
    BLOCK_MANA_CRYSTAL: ["pico"],
    BLOCK_RUNE_ORE: ["pico"],
    
    # Tierra y arena - Palas
    BLOCK_DIRT: ["pala"],
    BLOCK_GRASS: ["pala"],
    BLOCK_SAND: ["pala"],
    BLOCK_DESERT_SAND: ["pala"],
    BLOCK_HARD_SAND: ["pala"],
    BLOCK_CLAY: ["pala"],
    BLOCK_MUD: ["pala"],
    
    # Madera - Hachas
    BLOCK_WOOD: ["hacha"],
    BLOCK_JUNGLE_WOOD: ["hacha"],
    BLOCK_LEAVES: ["hacha", "pala"],  # Se puede con ambos
    BLOCK_JUNGLE_LEAVES: ["hacha", "pala"],
}

# --- Texturas de Grietas para Minería ---
CRACK_TEXTURES = {
    0: None,  # Sin grieta
    1: [  # Grieta nivel 1 (25%)
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ],
    2: [  # Grieta nivel 2 (50%)
        [1, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ],
    3: [  # Grieta nivel 3 (75%)
        [1, 1, 1, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ],
    4: [  # Grieta nivel 4 (100%)
        [1, 1, 1, 1, 0],
        [1, 1, 1, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
}

# --- Sistema de Sprites ---
# --- Sistema de Sprites ---
def create_block_sprite(color, size=TILE_SIZE):
    """Crea un sprite básico para un bloque"""
    sprite = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(sprite, color, (0, 0, size, size))
    
    # Agregar bordes para dar profundidad (usando max() para evitar valores negativos)
    pygame.draw.rect(sprite, (max(0, color[0]-20), max(0, color[1]-20), max(0, color[2]-20)), (0, 0, size, 2))  # Borde superior
    pygame.draw.rect(sprite, (max(0, color[0]-20), max(0, color[1]-20), max(0, color[2]-20)), (0, 0, 2, size))  # Borde izquierdo
    pygame.draw.rect(sprite, (min(255, color[0]+20), min(255, color[1]+20), min(255, color[2]+20)), (0, size-2, size, 2))  # Borde inferior
    pygame.draw.rect(sprite, (min(255, color[0]+20), min(255, color[1]+20), min(255, color[2]+20)), (size-2, 0, 2, size))  # Borde derecho
    
    return sprite

def create_tool_sprite(base_color, tool_type, size=32):
    """Crea sprites para herramientas"""
    sprite = pygame.Surface((size, size), pygame.SRCALPHA)
    
    if tool_type == "pico":
        # Palo
        pygame.draw.rect(sprite, (101, 67, 33), (14, 8, 4, 20))
        # Cabeza del pico
        pygame.draw.polygon(sprite, base_color, [
            (8, 8), (24, 8), (20, 16), (12, 16)
        ])
        
    elif tool_type == "hacha":
        # Palo
        pygame.draw.rect(sprite, (101, 67, 33), (14, 8, 4, 20))
        # Cabeza del hacha
        pygame.draw.polygon(sprite, base_color, [
            (8, 8), (20, 8), (20, 16), (12, 16)
        ])
        
    elif tool_type == "pala":
        # Palo
        pygame.draw.rect(sprite, (101, 67, 33), (14, 8, 4, 20))
        # Cabeza de la pala
        pygame.draw.rect(sprite, base_color, (10, 8, 12, 8))
        
    elif tool_type == "espada":
        # Empuñadura
        pygame.draw.rect(sprite, (101, 67, 33), (14, 8, 4, 16))
        # Hoja
        pygame.draw.polygon(sprite, base_color, [
            (12, 4), (20, 4), (18, 24), (14, 24)
        ])
        
    elif tool_type == "arco":
        # Forma del arco
        pygame.draw.arc(sprite, (101, 67, 33), (8, 8, 16, 16), 0, 3.14, 3)
        # Cuerda
        pygame.draw.line(sprite, (200, 200, 200), (8, 16), (24, 16), 2)
        
    elif tool_type == "poción":
        # Frasco
        pygame.draw.rect(sprite, base_color, (10, 8, 12, 16))
        pygame.draw.rect(sprite, (255, 255, 255), (10, 8, 12, 4))
        # Cuello
        pygame.draw.rect(sprite, (200, 200, 200), (13, 4, 6, 4))
        
    return sprite

# --- Sprites pre-creados ---
SPRITES = {}

# Crear sprites de bloques
SPRITES[BLOCK_GRASS] = create_block_sprite((34, 139, 34))
SPRITES[BLOCK_DIRT] = create_block_sprite((139, 69, 19))
SPRITES[BLOCK_STONE] = create_block_sprite((100, 100, 100))
SPRITES[BLOCK_SAND] = create_block_sprite((237, 201, 175))
SPRITES[BLOCK_SNOW] = create_block_sprite((250, 250, 250))
SPRITES[BLOCK_COAL] = create_block_sprite((50, 50, 50))
SPRITES[BLOCK_MANA_CRYSTAL] = create_block_sprite((100, 100, 255))
SPRITES[BLOCK_SHADOW_MUSHROOM] = create_block_sprite((128, 0, 128))
SPRITES[BLOCK_RUNE_ORE] = create_block_sprite((255, 100, 0))
SPRITES[BLOCK_WOOD] = create_block_sprite((101, 67, 33))
SPRITES[BLOCK_LEAVES] = create_block_sprite((0, 100, 0))
SPRITES[BLOCK_IRON_ORE] = create_block_sprite((210, 180, 140))
SPRITES[BLOCK_GOLD_ORE] = create_block_sprite((255, 215, 0))
SPRITES[BLOCK_DIAMOND_ORE] = create_block_sprite((185, 242, 255))
SPRITES[BLOCK_COPPER_ORE] = create_block_sprite((184, 115, 51))
SPRITES[BLOCK_SILVER_ORE] = create_block_sprite((200, 200, 220))
SPRITES[BLOCK_PLATINUM_ORE] = create_block_sprite((150, 200, 255))

# Crear sprites de herramientas
SPRITES["Pico de Madera"] = create_tool_sprite((150, 120, 80), "pico")
SPRITES["Pico de Piedra"] = create_tool_sprite((150, 150, 150), "pico")
SPRITES["Pico de Cobre"] = create_tool_sprite((184, 115, 51), "pico")
SPRITES["Pico de Hierro"] = create_tool_sprite((200, 200, 200), "pico")
SPRITES["Pico de Plata"] = create_tool_sprite((200, 200, 220), "pico")
SPRITES["Pico de Oro"] = create_tool_sprite((255, 215, 0), "pico")
SPRITES["Pico de Diamante"] = create_tool_sprite((185, 242, 255), "pico")

SPRITES["Hacha de Madera"] = create_tool_sprite((150, 120, 80), "hacha")
SPRITES["Hacha de Piedra"] = create_tool_sprite((150, 150, 150), "hacha")
SPRITES["Hacha de Hierro"] = create_tool_sprite((200, 200, 200), "hacha")
SPRITES["Hacha de Diamante"] = create_tool_sprite((185, 242, 255), "hacha")

SPRITES["Pala de Madera"] = create_tool_sprite((150, 120, 80), "pala")
SPRITES["Pala de Piedra"] = create_tool_sprite((150, 150, 150), "pala")
SPRITES["Pala de Hierro"] = create_tool_sprite((200, 200, 200), "pala")
SPRITES["Pala de Diamante"] = create_tool_sprite((185, 242, 255), "pala")

SPRITES["Espada de Madera"] = create_tool_sprite((150, 120, 80), "espada")
SPRITES["Espada de Piedra"] = create_tool_sprite((150, 150, 150), "espada")
SPRITES["Espada de Hierro"] = create_tool_sprite((200, 200, 200), "espada")

SPRITES["Arco de Madera"] = create_tool_sprite((150, 120, 80), "arco")
SPRITES["Flecha de Madera"] = create_tool_sprite((139, 69, 19), "poción")  # Usamos sprite de poción temporalmente

SPRITES["Poción de Vida"] = create_tool_sprite((255, 0, 0), "poción")
SPRITES["Poción de Maná"] = create_tool_sprite((0, 0, 255), "poción")

# Sprites para materiales básicos
SPRITES["Tablon de Madera"] = create_block_sprite((153, 102, 51), 32)
SPRITES["Palo"] = create_tool_sprite((139, 69, 19), "pico")  # Sprite temporal
SPRITES["Lingote de Cobre"] = create_block_sprite((184, 115, 51), 32)
SPRITES["Lingote de Hierro"] = create_block_sprite((210, 180, 140), 32)
SPRITES["Lingote de Oro"] = create_block_sprite((255, 215, 0), 32)
SPRITES["Lingote de Plata"] = create_block_sprite((200, 200, 220), 32)
SPRITES["Lingote de Platino"] = create_block_sprite((150, 200, 255), 32)
SPRITES["Carbon"] = create_block_sprite((50, 50, 50), 32)
SPRITES["Cristal de Mana"] = create_block_sprite((100, 100, 255), 32)
SPRITES["Hongo Sombrio"] = create_block_sprite((128, 0, 128), 32)
SPRITES["Mena Runica"] = create_block_sprite((255, 100, 0), 32)