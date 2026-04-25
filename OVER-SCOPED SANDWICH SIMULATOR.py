import sys
import os
import random
import math
import json
from pathlib import Path # type: ignore
from PyQt6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, pyqtProperty, QPoint, QTimer, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QLinearGradient, QRadialGradient, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QStackedWidget, QLineEdit, QSlider, QTextEdit,
    QScrollArea, QProgressBar, QGridLayout, QFrame, QTabWidget
)

# --- Configuration & Constants ---
if getattr(sys, 'frozen', False):
    # Running as a bundled executable
    RESOURCE_DIR = Path(sys._MEIPASS)
    DATA_DIR = Path(os.environ.get("APPDATA", Path.home())) / "Overscoped Sandwich Simulator"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
else:
    # Running in normal Python environment
    RESOURCE_DIR = Path(__file__).resolve().parent
    DATA_DIR = RESOURCE_DIR

SAVE_FILE = DATA_DIR / "save_data.json"
COLLECTIBLES_FILE = DATA_DIR / "collectibles.json"
SOUNDS_DIR = RESOURCE_DIR / "sounds"
IMAGES_DIR = RESOURCE_DIR / "images"
MUSIC_FILE = SOUNDS_DIR / "background_music.mp3"

COLORS = {
    "primary": "#ffca28",
    "primary_hover": "#ffd54f",
    "primary_border": "#ffa000",
    "accent": "#f06292",
    "text_dark": "#5d4037",
    "sky_top": "#81d4fa",
    "sky_bottom": "#29b6f6",
    "cloud": "#ffffff",
    "cloud_outline": "#bbdefb"
}

SFX_FILES = {
    "serve_sandwich": SOUNDS_DIR / "sfx_serve_sandwich.wav",
    "customer_leave": SOUNDS_DIR / "sfx_customer_leave.wav",
    "button_click": SOUNDS_DIR / "sfx_button_click.wav",
    "achievement": SOUNDS_DIR / "sfx_achievement.wav",
    "ingredients": {
        "Bread": SOUNDS_DIR / "sfx_bread.wav",
        "Fresh Tomato": SOUNDS_DIR / "sfx_tomato.wav",
        "Premium Ham": SOUNDS_DIR / "sfx_ham.wav",
        "Cosmic Cheese": SOUNDS_DIR / "sfx_cheese.wav",
        "Martian Pepper": SOUNDS_DIR / "sfx_pepper.wav",
        "Storm Pickles": SOUNDS_DIR / "sfx_pickle.wav",
        "Void Matter": SOUNDS_DIR / "sfx_void.wav",
    }
}

GAME_COLORS = {
    "Bread": "#d7ccc8",
    "Fresh Tomato": "#ef5350",
    "Premium Ham": "#8d6e63",
    "Cosmic Cheese": "#fff176",
    "Martian Pepper": "#ff5722",
    "Storm Pickles": "#4caf50",
    "Void Matter": "#212121",
    "Plate": "#cfd8dc"
}

LOCATIONS = {
    1: {
        "name": "Your Front Garden", "days": 7, "rank": "Beginner Chef", "req": 500, 
        "fail": "You couldn't ketchup to demand.",
        "intro": "You begin your empire in your garden, where you craft simple tomato sandwiches for neighbors and random dogs.",
        "success_msg": "The government arrives to shut you down, but you sell your house just in time to buy a shop!",
        "profit_mult": 1,
        "sky": ["#81d4fa", "#29b6f6"],
        "rent": 20,
        "rent_name": "Garden Permit",
        "music_file": SOUNDS_DIR / "music_garden.mp3",
        "bg_file": IMAGES_DIR / "bg_garden.png",
    },
    2: {
        "name": "Small Sandwich Shop", "days": 12, "rank": "Amateur Entrepreneur", "req": 5000, 
        "fail": "You've been ham-handled by justice.",
        "intro": "The government arrived and seized your garden! You relocate to a small shop. Premium ham is now on the menu.",
        "success_msg": "The Global Sandwich Ban hits! You build a rocket out of stale bread and launch into the unknown.",
        "profit_mult": 10,
        "sky": ["#4fc3f7", "#0288d1"],
        "rent": 200, 
        "rent_name": "Shop Rent",
        "music_file": SOUNDS_DIR / "music_shop.mp3",
        "bg_file": IMAGES_DIR / "bg_shop.png",
    },
    3: {
        "name": "The Moon Base", "days": 15, "rank": "Space Chef", "req": 100000, 
        "fail": "Moon Melt: The sandwich was too strong.",
        "intro": "The Global Sandwich Ban forced you into space. You've landed on the Moon. Cosmic Cheese awaits!",
        "success_msg": "The Lunar Authority demands a shutdown. You ignite your engines and head for the red planet.",
        "profit_mult": 100,
        "sky": ["#212121", "#000000"],
        "rent": 5000,
        "rent_name": "Oxygen Tax",
        "music_file": SOUNDS_DIR / "music_moon.mp3",
        "bg_file": IMAGES_DIR / "bg_moon.png",
    },
    4: {
        "name": "Mars Diner", "days": 20, "rank": "Interplanetary Tycoon", "req": 10000000, 
        "fail": "Absorbed into the Martian cult of flavor.",
        "intro": "Gravity distortion laws forced you off the Moon. Welcome to Mars! Beware the heat of Martian Peppers.",
        "success_msg": "A flavor riot breaks out! You narrowly escape the Martian Senate's wrath, boosting toward Jupiter.",
        "profit_mult": 5000,
        "sky": ["#bf360c", "#3e2723"],
        "rent": 250000,
        "rent_name": "Cooling Utilities",
        "music_file": SOUNDS_DIR / "music_mars.mp3",
        "bg_file": IMAGES_DIR / "bg_mars.png",
    },
    5: {
        "name": "Jupiter Floating Bar", "days": 25, "rank": "Gas Giant Gourmet", "req": 1000000000, 
        "fail": "You became static in the sandwich industry.",
        "intro": "Fleeing the flavor riots on Mars, you've reached Jupiter. Storm Pickles provide an electric kick.",
        "success_msg": "The gravitational pressure is crushing the bar! You warp out just as the shop implodes.",
        "profit_mult": 200000,
        "sky": ["#4a148c", "#1a237e"],
        "rent": 15000000,
        "rent_name": "Gravity Stabilization",
        "music_file": SOUNDS_DIR / "music_jupiter.mp3",
        "bg_file": IMAGES_DIR / "bg_jupiter.png",
    },
    6: {
        "name": "Ton-216 (Black Hole)", "days": 40, "rank": "Galactic Master Chef", "req": 6000000000000000000, 
        "fail": "It is Day 40 and you're short of 6 Quintillion. Chockster Gumes won't even look at you. You jump into Ton-216's darkness.",
        "intro": "The bar is imploding! You've jumped to the edge of Ton-216. Use Void Matter to reach 6 Quintillion.",
        "success_msg": "You've done it. You have the money. But the black hole beckons...",
        "profit_mult": 100000000,
        "sky": ["#000000", "#000000"],
        "rent": 1000000000,
        "rent_name": "Void Maintenance",
        "music_file": SOUNDS_DIR / "music_blackhole.mp3",
        "bg_file": IMAGES_DIR / "bg_blackhole.png",
    }
}

SECRET_RECIPES = {
    "The Classic": {"ingredients": ["Bread", "Fresh Tomato", "Bread"], "bonus_mult": 5},
    "Ham & Cheese Delight": {"ingredients": ["Bread", "Premium Ham", "Cosmic Cheese", "Bread"], "bonus_mult": 10},
    "Spicy Martian": {"ingredients": ["Bread", "Martian Pepper", "Premium Ham", "Bread"], "bonus_mult": 20},
    "Jupiterian Feast": {"ingredients": ["Bread", "Storm Pickles", "Cosmic Cheese", "Premium Ham", "Bread"], "bonus_mult": 50},
    "Void Sandwich": {"ingredients": ["Bread", "Void Matter", "Void Matter", "Bread"], "bonus_mult": 1000},
    "The Everything": {"ingredients": ["Bread", "Fresh Tomato", "Premium Ham", "Cosmic Cheese", "Martian Pepper", "Storm Pickles", "Void Matter", "Bread"], "bonus_mult": 5000},
}

SANDWICH_ADJECTIVES = [
    "Soggy", "Crispy", "Fluffy", "Spicy", "Cheesy", "Meaty", "Fresh", "Stale",
    "Cosmic", "Martian", "Stormy", "Void-touched", "Legendary", "Epic", "Humble",
    "Greasy", "Toasted", "Frozen", "Radioactive", "Quantum", "Interdimensional"
]
SANDWICH_NOUNS = [
    "Melt", "Stack", "Dream", "Delight", "Behemoth", "Orb", "Creation",
    "Masterpiece", "Abomination", "Pile", "Tower", "Concoction", "Feast",
    "Snack", "Monstrosity", "Wonder", "Anomaly", "Singularity"
]

MARKET_EVENTS = {
    "Tomato Blight": {"ingredient": "Fresh Tomato", "cost_mult": 2.5, "value_mult": 1.5, "message": "A sudden blight has hit the tomato crops! Prices soar, but so does demand."},
    "Ham Export Ban": {"ingredient": "Premium Ham", "cost_mult": 3.0, "value_mult": 1.0, "message": "Intergalactic trade disputes have halted ham exports. Expect shortages and high prices."},
    "Cheese Surplus": {"ingredient": "Cosmic Cheese", "cost_mult": 0.5, "value_mult": 1.2, "message": "A massive surplus of Cosmic Cheese! Buy low, sell high!"},
    "Pepper Rush": {"ingredient": "Martian Pepper", "cost_mult": 1.5, "value_mult": 2.0, "message": "Everyone wants Martian Peppers today! High demand, higher profits."},
    "Pickle Frenzy": {"ingredient": "Storm Pickles", "cost_mult": 2.0, "value_mult": 2.5, "message": "Lightning storms on Jupiter yielded record pickle harvests! Everyone wants them."},
    "Void Leak": {"ingredient": "Void Matter", "cost_mult": 0.3, "value_mult": 3.0, "message": "A crack in spacetime leaks cheap Void Matter. The stuff practically sells itself!"},
    "Supply Chain Crisis": {"ingredient": "Bread", "cost_mult": 4.0, "value_mult": 1.0, "message": "Bread shortage across the galaxy! Even the basics are expensive today."},
    "Normal Market": {"ingredient": None, "cost_mult": 1.0, "value_mult": 1.0, "message": "The market is stable today. Business as usual."},
    "Golden Hour": {"ingredient": None, "cost_mult": 0.8, "value_mult": 1.5, "message": "Everything is discounted and customers are generous! A golden day for sandwich makers."},
}

BRANCHING_EVENTS = [
    {
        "title": "FOOD CRITIC VISIT",
        "text": "A famous food critic has arrived! They want to try your best sandwich.",
        "option_a": "Give a FREE sandwich for a PR boost",
        "option_b": "Charge DOUBLE and risk a bad review",
        "effect_a": {"hype": 0.3, "money_mult": 0},
        "effect_b": {"hype": -0.15, "money_mult": 2.5},
    },
    {
        "title": "MYSTERY SUPPLIER",
        "text": "A shady figure offers you rare ingredients at a steep discount... or is it a scam?",
        "option_a": "Accept the deal (risky but cheap)",
        "option_b": "Decline and play it safe",
        "effect_a": {"money_mult": -0.3, "ingredient_discount": 0.5},  # 50% discount next day
        "effect_b": {"hype": 0.05},
    },
    {
        "title": "HEALTH INSPECTOR",
        "text": "The health inspector is here! Your kitchen is... questionable.",
        "option_a": "Bribe them (costs money, avoids penalty)",
        "option_b": "Accept the fine (lose money, gain reputation for honesty)",
        "effect_a": {"money_mult": -0.2, "hype": -0.1},
        "effect_b": {"money_mult": -0.4, "hype": 0.2},
    },
    {
        "title": "SANDWICH COMPETITION",
        "text": "A rival chef challenges you to a sandwich-off! Winner takes the prize pot.",
        "option_a": "Accept the challenge (50/50 chance)",
        "option_b": "Decline and focus on customers",
        "effect_a": {"competition": True},
        "effect_b": {"hype": 0.02},
    },
    {
        "title": "CELEBRITY ENDORSEMENT",
        "text": "A celebrity offers to endorse your shop... for a hefty fee.",
        "option_a": "Pay for the endorsement",
        "option_b": "Save your money",
        "effect_a": {"money_mult": -0.5, "hype": 0.5},
        "effect_b": {},
    },
    {
        "title": "ALIEN DELEGATION",
        "text": "An alien delegation wants to place a bulk order. They pay well but the order is massive.",
        "option_a": "Accept the bulk order",
        "option_b": "Politely decline",
        "effect_a": {"money_mult": 3.0, "hype": 0.1},
        "effect_b": {"hype": -0.05},
    },
]

UPGRADES = {
    "Heat Sink": {"cost": 50000, "location": 4, "desc": "Reduces spiciness buildup by 50%", "effect": "spice_resist"},
    "Gravity Boots": {"cost": 20000, "location": 3, "desc": "Sandwiches drop faster on the Moon", "effect": "moon_speed"},
    "Storm Shield": {"cost": 5000000, "location": 5, "desc": "Reduces screen shake on Jupiter by 70%", "effect": "shake_resist"},
    "Void Anchor": {"cost": 500000000, "location": 6, "desc": "Reduces daily rent in the Black Hole by 50%", "effect": "rent_discount"},
    "Speed Hands": {"cost": 1000, "location": 1, "desc": "Customers wait 50% longer", "effect": "patience_boost"},
    "Hype Machine": {"cost": 5000, "location": 2, "desc": "Hype decays 50% slower", "effect": "hype_slow"},
    "Auto-Fryer": {"cost": 100000, "location": 3, "desc": "All sandwich values increased by 25%", "effect": "value_boost"},
    "Quantum Mixer": {"cost": 10000000, "location": 4, "desc": "Secret recipe bonuses doubled", "effect": "recipe_boost"},
}

ACHIEVEMENTS = {
    "First Sale": {"desc": "Serve your first sandwich", "check": lambda s: s.get("total_served", 0) >= 1, "reward": "money_100"},
    "100 Served": {"desc": "Serve 100 sandwiches", "check": lambda s: s.get("total_served", 0) >= 100, "reward": "hype_0.1"},
    "1000 Served": {"desc": "Serve 1000 sandwiches", "check": lambda s: s.get("total_served", 0) >= 1000, "reward": "money_mult_1.1"},
    "Tomato King": {"desc": "Use 500 tomatoes", "check": lambda s: s.get("ingredient_counts", {}).get("Fresh Tomato", 0) >= 500, "reward": "hype_0.05"},
    "Ham Lord": {"desc": "Use 300 ham slices", "check": lambda s: s.get("ingredient_counts", {}).get("Premium Ham", 0) >= 300, "reward": "money_5000"},
    "Millionaire": {"desc": "Reach $1M total", "check": lambda s: s.get("money", 0) >= 1000000, "reward": "hype_0.2"},
    "Billionaire": {"desc": "Reach $1B total", "check": lambda s: s.get("money", 0) >= 1000000000, "reward": "hype_0.3"},
    "Perfect Streak 10": {"desc": "10 perfect orders in a row", "check": lambda s: s.get("perfect_streak", 0) >= 10, "reward": "money_mult_1.05"},
    "Moon Landing": {"desc": "Reach the Moon", "check": lambda s: s.get("location_id", 1) >= 3, "reward": "money_10000"},
    "Mars Pioneer": {"desc": "Reach Mars", "check": lambda s: s.get("location_id", 1) >= 4, "reward": "money_100000"},
    "Gas Giant": {"desc": "Reach Jupiter", "check": lambda s: s.get("location_id", 1) >= 5, "reward": "money_1000000"},
    "Event Horizon": {"desc": "Reach the Black Hole", "check": lambda s: s.get("location_id", 1) >= 6, "reward": "money_100000000"},
    "Secret Chef": {"desc": "Discover 3 secret recipes", "check": lambda s: len(s.get("discovered_recipes", [])) >= 3, "reward": "hype_0.3"},
    "Recipe Master": {"desc": "Discover all secret recipes", "check": lambda s: len(s.get("discovered_recipes", [])) >= len(SECRET_RECIPES), "reward": "money_mult_1.2"},
}

COLLECTIBLE_ITEMS = {
    1: [
        {"id": "garden_gnome", "name": "Lucky Garden Gnome", "desc": "Found hiding behind a tomato plant. Seems to bring good fortune.", "chance": 0.05},
        {"id": "golden_spatula", "name": "Golden Spatula", "desc": "A legendary kitchen tool, buried under your front porch.", "chance": 0.03},
    ],
    2: [
        {"id": "vintage_menu", "name": "Vintage Menu", "desc": "An old menu from the original sandwich shop that stood here 100 years ago.", "chance": 0.05},
        {"id": "ham_crown", "name": "Ham Crown", "desc": "A crown made entirely of premium ham. Who made this?", "chance": 0.03},
    ],
    3: [
        {"id": "moon_rock", "name": "Glowing Moon Rock", "desc": "It hums faintly. Smells like cheese.", "chance": 0.05},
        {"id": "astronaut_recipe", "name": "Astronaut's Recipe Book", "desc": "Recipes from the first lunar sandwich chef.", "chance": 0.03},
    ],
    4: [
        {"id": "mars_crystal", "name": "Martian Pepper Crystal", "desc": "A crystallized Martian Pepper. It never stops burning.", "chance": 0.05},
        {"id": "alien_fork", "name": "Alien Fork", "desc": "A utensil from an unknown civilization. Has 7 prongs.", "chance": 0.03},
    ],
    5: [
        {"id": "storm_jar", "name": "Bottled Storm", "desc": "A jar containing a miniature Jupiter storm. It crackles.", "chance": 0.05},
        {"id": "gravity_dice", "name": "Gravity Dice", "desc": "Dice that always land on the same number. Suspicious.", "chance": 0.03},
    ],
    6: [
        {"id": "void_shard", "name": "Void Shard", "desc": "A fragment of nothing. Or everything. Hard to tell.", "chance": 0.05},
        {"id": "universe_crumb", "name": "The Last Crumb", "desc": "The final crumb from the first sandwich ever made, preserved in void amber.", "chance": 0.02},
    ],
}

INGREDIENTS = {
    "Bread": {"cost": 5, "value": 10, "loc": 1},
    "Fresh Tomato": {"cost": 10, "value": 25, "loc": 1},
    "Premium Ham": {"cost": 50, "value": 120, "loc": 2},
    "Cosmic Cheese": {"cost": 500, "value": 1500, "loc": 3},
    "Martian Pepper": {"cost": 5000, "value": 20000, "loc": 4},
    "Storm Pickles": {"cost": 100000, "value": 500000, "loc": 5},
    "Void Matter": {"cost": 100000000, "value": 1000000000, "loc": 6}
}

CUSTOMER_QUOTES = [
    "Is it artisanal? It looks artisanal.",
    "I hope there's no void-hair in this.",
    "My Martian doctor said I need more fiber.",
    "Can I pay in crypto-bread?",
    "I've traveled 4 lightyears for this ham.",
    "Make it snappy, my oxygen is at 4%.",
    "Is this gluten-free void matter?",
    "I'm reporting this to the Galactic Better Business Bureau.",
    "Best sandwich ever! Five stars!",
    "Where's the ham? I specifically asked for ham.",
    "This tastes like it was made with love. And also regret.",
    "Do you deliver to the Andromeda galaxy?",
    "My last sandwich here changed my life. Literally. I evolved.",
    "I used to be a sandwich. Long story.",
    "The void whispers to me through this bread.",
]

CUSTOMER_FEEDBACK_POSITIVE = [
    "Best sandwich ever! Five stars!",
    "This changed my life!",
    "I'll tell all my friends!",
    "Worth every credit.",
    "You're a genius!",
    "I'm coming back tomorrow!",
    "Better than my grandmother's recipe!",
]

CUSTOMER_FEEDBACK_NEGATIVE = [
    "Where's the flavor?",
    "I waited too long for this...",
    "Not what I ordered.",
    "I expected more.",
    "My pet sandworm makes better food.",
    "Refund. Now.",
    "I'm leaving a one-star review.",
]

# --- Utility Functions ---

def format_currency(amount):
    """Handles formatting for normal money up to 6 Quintillion."""
    if amount < 0:
        return f"-{format_currency(abs(amount))}"
    if amount >= 1e18:
        return f"${amount/1e18:.2f}Q"
    elif amount >= 1e15:
        return f"${amount/1e15:.2f}q"
    elif amount >= 1e12:
        return f"${amount/1e12:.2f}T"
    elif amount >= 1e9:
        return f"${amount/1e9:.2f}B"
    elif amount >= 1e6:
        return f"${amount/1e6:.2f}M"
    elif amount >= 1e3:
        return f"${amount/1e3:.1f}k"
    return f"${int(amount)}"


def generate_sandwich_name(ingredients):
    """Generates a fun descriptive name based on ingredients."""
    # Weight adjectives toward ingredient-related ones
    special_adj = []
    if "Martian Pepper" in ingredients:
        special_adj.extend(["Spicy", "Fiery", "Scorching"])
    if "Cosmic Cheese" in ingredients:
        special_adj.extend(["Cheesy", "Cosmic", "Stellar"])
    if "Storm Pickles" in ingredients:
        special_adj.extend(["Stormy", "Electric", "Crackling"])
    if "Void Matter" in ingredients:
        special_adj.extend(["Void-touched", "Abyssal", "Quantum"])
    if "Fresh Tomato" in ingredients:
        special_adj.extend(["Fresh", "Garden", "Juicy"])
    if "Premium Ham" in ingredients:
        special_adj.extend(["Meaty", "Premium", "Smoky"])
    
    adj_pool = special_adj if special_adj else SANDWICH_ADJECTIVES
    adj = random.choice(adj_pool)
    
    # Pick noun based on size
    if len(ingredients) >= 6:
        noun = random.choice(["Behemoth", "Tower", "Monstrosity", "Singularity"])
    elif len(ingredients) >= 4:
        noun = random.choice(["Feast", "Creation", "Masterpiece", "Wonder"])
    else:
        noun = random.choice(SANDWICH_NOUNS)
    
    return f"The {adj} {noun}"


def load_collectibles():
    """Load global collectibles from file."""
    if COLLECTIBLES_FILE.exists() and COLLECTIBLES_FILE.stat().st_size > 0:
        try:
            with open(COLLECTIBLES_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"collected": [], "sandwich_history": []}


def save_collectibles(data):
    """Save global collectibles to file."""
    try:
        with open(COLLECTIBLES_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving collectibles: {e}")


# --- Widget Classes ---

class SandwichRenderer(QWidget):
    def __init__(self):
        super().__init__()
        self.ingredients = []
        self.offsets = {}
        self.wobble = 0
        self.time_val = 0
        self.anim_timer = QTimer(self)
        self.sandstorm_active = False
        self.anim_timer.timeout.connect(self.update_animations)
        self.anim_timer.start(16)

    def add_ingredient(self, name):
        self.ingredients.append(name)
        self.offsets[len(self.ingredients) - 1] = 100.0
        self.update()

    def clear(self):
        self.ingredients = []
        self.offsets = {}
        self.sandstorm_active = False
        self.update()

    def update_animations(self):
        any_moving = False
        self.wobble = (self.wobble + 0.1) % 6.28
        self.time_val += 0.05
        
        is_moon = False
        has_moon_speed = False
        if hasattr(self.parent(), 'session'):
            is_moon = self.parent().session.get('location_id', 1) == 3
            has_moon_speed = "moon_speed" in self.parent().session.get('upgrades', [])

        for idx in list(self.offsets.keys()):
            if self.offsets[idx] > 0.5:
                if is_moon and not has_moon_speed:
                    decay = 0.96
                else:
                    decay = 0.8
                self.offsets[idx] *= decay
                any_moving = True
            else:
                if is_moon:
                    self.offsets[idx] = math.sin(self.wobble + idx) * 3
                    any_moving = True
                else:
                    self.offsets[idx] = 0

        if any_moving:
            self.update()

    def mousePressEvent(self, event):
        game_screen = self.window().findChild(GameScreen)
        if game_screen and game_screen.session.get('location_id') == 4:
            game_screen.cool_down()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.sandstorm_active:
            painter.setOpacity(0.5 + math.sin(self.time_val * 5) * 0.2)
            painter.setBrush(QColor("#c27c0e"))
            painter.drawRect(self.rect())

        is_jupiter = False
        is_void = False
        if hasattr(self.parent(), 'session'):
            is_jupiter = self.parent().session.get('location_id') == 5
            is_void = self.parent().session.get('location_id') == 6
        
        if self.sandstorm_active:
            painter.setOpacity(1.0)

        cx, bottom_y = self.width() // 2, self.height() - 50
        
        # Draw Plate
        painter.setBrush(QColor(GAME_COLORS["Plate"]))
        painter.setPen(QPen(QColor("#90a4ae"), 3))
        painter.drawEllipse(cx - 150, bottom_y - 20, 300, 60)

        # Draw Layers
        layer_height = 25
        for i, ing in enumerate(self.ingredients):
            color = GAME_COLORS.get(ing, "#ffffff")
            offset = self.offsets.get(i, 0)
            
            rect = QRect(cx - 100, bottom_y - (i + 1) * layer_height - int(offset), 200, layer_height)
            
            painter.setBrush(QColor(color))
            painter.setPen(QPen(QColor(0, 0, 0, 50), 2))
            painter.drawRoundedRect(rect, 10, 10)
            
            # Jupiter: Storm Pickle Crackle
            if is_jupiter and ing == "Storm Pickles":
                painter.setPen(QPen(QColor("#ffffff"), 2))
                for _ in range(3):
                    x1 = random.randint(rect.left(), rect.right())
                    y1 = random.randint(rect.top(), rect.bottom())
                    x2 = x1 + random.randint(-10, 10)
                    y2 = y1 + random.randint(-10, 10)
                    painter.drawLine(x1, y1, x2, y2)
            
            # Black Hole: Void Matter pulsing
            if is_void and ing == "Void Matter":
                glow = abs(math.sin(self.time_val * 2)) * 15
                grad = QRadialGradient(rect.center().x(), rect.center().y(), 120 + glow)
                grad.setColorAt(0, QColor(103, 58, 183, 100))
                grad.setColorAt(1, QColor(0, 0, 0, 0))
                painter.fillRect(rect.adjusted(-20, -20, 20, 20), grad)


class StoryOverlay(QWidget):
    def __init__(self, title, text, callback, option_a=None, option_b=None, choice_callback=None):
        super().__init__()
        self.callback = callback
        self.choice_callback = choice_callback
        self.setFixedSize(600, 450)
        self.setStyleSheet("background: rgba(13, 13, 22, 230); border: 4px solid #ffca28; border-radius: 20px;")
        
        layout = QVBoxLayout()
        t_label = QLabel(title)
        t_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #ffca28; border: none;")
        t_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        m_label = QLabel(text)
        m_label.setStyleSheet("font-size: 16px; color: white; border: none;")
        m_label.setWordWrap(True)
        m_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(t_label)
        layout.addSpacing(15)
        layout.addWidget(m_label)
        layout.addSpacing(20)
        
        if option_a and option_b:
            btn_layout = QHBoxLayout()
            btn_a = JuicyButton(option_a)
            btn_a.setFixedWidth(250)
            btn_a.setMinimumHeight(60)
            btn_a.clicked.connect(lambda: self.choose("a"))
            btn_b = JuicyButton(option_b)
            btn_b.setFixedWidth(250)
            btn_b.setMinimumHeight(60)
            btn_b.clicked.connect(lambda: self.choose("b"))
            btn_layout.addWidget(btn_a)
            btn_layout.addWidget(btn_b)
            layout.addLayout(btn_layout)
        else:
            btn = JuicyButton("CONTINUE")
            btn.setFixedWidth(200)
            btn.clicked.connect(self.close_and_continue)
            layout.addWidget(btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(10)
        self.setLayout(layout)

    def choose(self, choice):
        self.setParent(None)
        if self.choice_callback:
            self.choice_callback(choice)

    def close_and_continue(self):
        self.setParent(None)
        if self.callback:
            self.callback()


class Screen:
    MAIN_MENU = 0
    SAVE_SLOTS = 1
    GAME = 2
    UPGRADE_SHOP = 3


class JuicyButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self._scale = 1.0
        self._selected = False
        self.setMinimumHeight(80)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_style()

        self.anim = QPropertyAnimation(self, b"scale_prop")
        self.anim.setDuration(150)
        
        self.press_anim = QPropertyAnimation(self, b"scale_prop")
        self.press_anim.setDuration(50)
        self.press_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    def mousePressEvent(self, event):
        self.press_anim.setEndValue(0.95)
        self.press_anim.start()
        # Play global click sound if available
        main_win = self.window()
        if hasattr(main_win, 'play_ui_sfx'):
            main_win.play_ui_sfx("button_click")
        super().mousePressEvent(event)

    def refresh_style(self):
        border_col = "#ffffff" if self._selected else COLORS["primary_border"]
        bg_col = COLORS["primary_hover"] if self._selected else COLORS["primary"]
        
        self.setStyleSheet(f"""
            JuicyButton {{
                background-color: {bg_col};
                color: {COLORS["text_dark"]};
                border-radius: 30px;
                font-size: 24px;
                font-weight: bold;
                padding: 8px;
                border: 4px solid {border_col};
                margin: 5px;
            }}
            JuicyButton:hover {{
                background-color: {COLORS["primary_hover"]};
                border: 4px solid #ffffff;
            }}
            JuicyButton:pressed {{
                background-color: {COLORS["primary_border"]};
                border: 4px solid #3e2723;
            }}
        """)

    @pyqtProperty(float)
    def scale_prop(self):
        return self._scale

    @scale_prop.setter
    def scale_prop(self, value):
        self._scale = value
        self.update()

    @pyqtProperty(bool)
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        self.refresh_style()

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setEndValue(1.1)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setEndValue(1.0)
        self.anim.start()
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event):
        self.press_anim.setEndValue(1.1 if self.underMouse() else 1.0)
        self.press_anim.start()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(self._scale, self._scale)
        painter.translate(-self.width() / 2, -self.height() / 2)
        super().paintEvent(event)


class CloudTitle(QWidget):
    def __init__(self, text: str):
        super().__init__()
        self._text = text
        self._y_offset = 0
        self.setFixedHeight(140)

    @pyqtProperty(int)
    def y_offset(self):
        return self._y_offset

    @y_offset.setter
    def y_offset(self, value):
        self._y_offset = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.translate(0, self._y_offset)
        painter.setPen(QPen(QColor(COLORS["cloud_outline"]), 4))
        painter.setBrush(QBrush(QColor(COLORS["cloud"])))
        
        w, h = self.width(), self.height()
        mid_x = w // 2
        
        painter.drawEllipse(mid_x - 420, 40, 90, 90)
        painter.drawEllipse(mid_x - 370, 10, 120, 120)
        painter.drawEllipse(mid_x + 330, 40, 90, 90)
        painter.drawEllipse(mid_x + 250, 10, 120, 120)
        painter.drawEllipse(mid_x - 100, 0, 200, 100)
        painter.drawRoundedRect(mid_x - 350, 40, 700, 70, 35, 35)

        font = QFont("Segoe UI", 36)
        font.setBold(True)
        painter.setFont(font)
        
        painter.setPen(QColor(0, 0, 0, 30))
        painter.drawText(self.rect().translated(3, 3), Qt.AlignmentFlag.AlignCenter, self._text)
        
        painter.setPen(QColor("#3949ab"))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._text)


class MainMenu(QWidget):
    def __init__(self, audio_output=None, switch_callback=None):
        super().__init__()
        self.animation = None
        self.audio_output = audio_output
        self.switch_callback = switch_callback
        self.player = None
        self.init_ui()
        self.start_animation()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.addStretch(2)

        cloud_container = QHBoxLayout()
        self.cloud_title = CloudTitle("OVER-SCOPED SANDWICH SIMULATOR")
        self.cloud_title.setMinimumWidth(900)
        cloud_container.addWidget(self.cloud_title)
        main_layout.addLayout(cloud_container)
        main_layout.addSpacing(10)

        # Endless Mode Button (Hidden by default)
        self.endless_btn = JuicyButton("INFINITE VOID (ENDLESS)")
        self.endless_btn.setStyleSheet(self.endless_btn.styleSheet() + "background-color: #4a148c; color: white;")
        self.endless_btn.clicked.connect(self.on_endless)
        self.endless_btn.hide()
        self.check_endless_unlocked()

        # Subtitle
        subtitle = QLabel("THE ULTIMATE OVER-ENGINEERED LUNCH EXPERIENCE")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(
            "font-size: 20px; color: #ffffff; font-weight: bold; letter-spacing: 4px;"
            "background-color: rgba(240, 98, 146, 0.8); padding: 15px; border-radius: 10px;"
        )
        main_layout.addWidget(subtitle)

        # Volume Slider Container
        vol_layout = QHBoxLayout()
        vol_container = QWidget()
        vol_container.setFixedWidth(400)
        vol_inner_layout = QHBoxLayout(vol_container)
        
        vol_label = QLabel("AUDIO")
        vol_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff; background: transparent;")
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal { height: 12px; background: %s; border-radius: 6px; }
            QSlider::handle:horizontal { background: %s; border: 3px solid white; width: 24px; margin: -6px 0; border-radius: 12px; }
        """ % (COLORS["primary_border"], COLORS["accent"]))
        if self.audio_output:
            self.volume_slider.valueChanged.connect(lambda v: self.audio_output.setVolume(v / 100.0))
        
        vol_inner_layout.addWidget(vol_label)
        vol_inner_layout.addWidget(self.volume_slider)
        vol_layout.addStretch()
        vol_layout.addWidget(vol_container)
        vol_layout.addStretch()
        main_layout.addLayout(vol_layout)

        main_layout.addStretch(1)

        # Buttons
        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(500, 0, 500, 0)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        button_layout.setSpacing(20)

        play_button = JuicyButton("START GAME")
        play_button.clicked.connect(self.on_play)
        
        button_layout.addWidget(play_button)
        button_layout.addWidget(self.endless_btn)

        main_layout.addLayout(button_layout)
        main_layout.addStretch(2)

        self.setLayout(main_layout)

    def check_endless_unlocked(self):
        """Unlocks Endless Mode if any save has game_completed flag or reached 6Q."""
        if SAVE_FILE.exists():
            try:
                if os.path.getsize(SAVE_FILE) == 0:
                    return
                with open(SAVE_FILE, 'r') as f:
                    data = json.load(f)
                    for slot in data.values():
                        if slot and (slot.get('game_completed', False) or slot.get('money', 0) >= 6e18):
                            self.endless_btn.show()
                            break
            except:
                pass

    def on_endless(self):
        endless_data = {
            "name": "The Eternal Chef", "day": 1, "money": 100000000, 
            "rank": "Void Legend", "difficulty": "OVER-SCOPED",
            "location_id": 6, "unlocked": list(INGREDIENTS.keys()),
            "is_endless": True, "hype": 0.0,
            "upgrades": list(UPGRADES.keys()),  # All upgrades in endless
            "total_served": 0, "perfect_streak": 0,
            "ingredient_counts": {}, "discovered_recipes": [],
            "achievements_unlocked": [], "loan_amount": 0, "loan_interest_rate": 0,
            "sandwich_history": [],
        }
        if self.switch_callback:
            self.switch_callback(Screen.GAME, endless_data)

    def start_animation(self):
        self.animation = QPropertyAnimation(self.cloud_title, b"y_offset", self)
        self.animation.setDuration(2000)
        self.animation.setStartValue(0)
        self.animation.setKeyValueAt(0.5, -20)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.animation.setLoopCount(-1)
        self.animation.start()

    def on_play(self):
        if self.switch_callback:
            self.switch_callback(Screen.SAVE_SLOTS)


class SaveSlotMenu(QWidget):
    def __init__(self, switch_callback=None, save_trigger=None):
        super().__init__()
        self.switch_callback = switch_callback
        self.selected_slot = None
        self.selected_diff = "NORMAL"
        self.save_slots = self.load_saves()
        self.slot_buttons = {}
        self.diff_buttons = {}
        self.init_ui()
        self.update_slot_visuals()

    def load_saves(self):
        if SAVE_FILE.exists() and SAVE_FILE.stat().st_size > 0:
            if os.path.getsize(SAVE_FILE) == 0:
                return {1: None, 2: None, 3: None}
            try:
                with open(SAVE_FILE, 'r') as f:
                    data = json.load(f)
                    return {int(k): v for k, v in data.items()}
            except Exception as e:
                print(f"Error loading save: {e}")
        return {1: None, 2: None, 3: None}

    def save_to_file(self):
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(self.save_slots, f, indent=4)
        except Exception as e:
            print(f"Error saving to file: {e}")

    def get_slot_text(self, slot_id):
        data = self.save_slots.get(slot_id)
        if data:
            loc_name = LOCATIONS.get(data.get('location_id', 1), LOCATIONS[1])['name']
            return f"SLOT {slot_id}\n{data['name'].upper()}\nDay {data['day']} | {format_currency(data['money'])}\nRank: {data['rank']}\n{loc_name}"
        return f"SLOT {slot_id}\n(EMPTY)"

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addStretch(1)

        title = QLabel("SELECT SAVE SLOT")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 40px; font-weight: bold; color: #ffffff; letter-spacing: 2px;")
        layout.addWidget(title)
        layout.addSpacing(30)

        slot_layout = QHBoxLayout()
        slot_layout.setContentsMargins(100, 0, 100, 0)
        for i in range(1, 4):
            btn = JuicyButton("")
            btn.setFixedHeight(200)
            btn.clicked.connect(lambda _, x=i: self.on_slot_selected(x))
            self.slot_buttons[i] = btn
            slot_layout.addWidget(btn)
        layout.addLayout(slot_layout)

        layout.addSpacing(40)

        details_layout = QVBoxLayout()
        details_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        name_label = QLabel("NAME YOUR SANDWICH EMPIRE:")
        name_label.setStyleSheet("font-size: 18px; color: #ffffff; font-weight: bold;")
        details_layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Bread Zeppelin...")
        self.name_input.setFixedWidth(400)
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                border: 4px solid %s;
                border-radius: 15px;
                padding: 10px;
                font-size: 20px;
                color: #3949ab;
            }
        """ % COLORS["accent"])
        details_layout.addWidget(self.name_input, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(details_layout)
        layout.addSpacing(20)

        diff_layout = QHBoxLayout()
        diff_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        diff_label = QLabel("DIFFICULTY:")
        diff_label.setStyleSheet("font-size: 18px; color: #ffffff; font-weight: bold; margin-right: 10px;")
        diff_layout.addWidget(diff_label)

        for level in ["EASY", "NORMAL", "OVER-SCOPED"]:
            btn = JuicyButton(level)
            btn.setMinimumHeight(50)
            btn.setFixedWidth(150)
            btn.clicked.connect(lambda _, l=level: self.set_difficulty(l))
            self.diff_buttons[level] = btn
            diff_layout.addWidget(btn)
        
        self.set_difficulty("NORMAL")
        
        layout.addLayout(diff_layout)
        layout.addStretch(1)

        nav_layout = QHBoxLayout()
        self.back_btn = JuicyButton("BACK")
        self.back_btn.setFixedWidth(200)
        self.back_btn.clicked.connect(lambda: self.switch_callback(Screen.MAIN_MENU))

        self.delete_btn = JuicyButton("DELETE")
        self.delete_btn.setFixedWidth(200)
        self.delete_btn.clicked.connect(self.on_delete_clicked)
        self.delete_btn.hide()
        
        self.loan_btn = JuicyButton("TAKE LOAN")
        self.loan_btn.setFixedWidth(200)
        self.loan_btn.clicked.connect(self.on_take_loan)
        self.loan_btn.hide()

        self.start_btn = JuicyButton("READY!")
        self.start_btn.setFixedWidth(300)
        self.start_btn.clicked.connect(self.on_ready_clicked)

        nav_layout.addStretch()
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.delete_btn)
        nav_layout.addWidget(self.loan_btn)
        nav_layout.addWidget(self.start_btn)
        nav_layout.addStretch()
        layout.addLayout(nav_layout)
        layout.addSpacing(50)

        self.setLayout(layout)

    def set_difficulty(self, level):
        self.selected_diff = level
        for name, btn in self.diff_buttons.items():
            is_selected = (name == level)
            bg = COLORS["accent"] if is_selected else "#bbdefb"
            txt = "white" if is_selected else COLORS["text_dark"]
            border = "4px solid white" if is_selected else "2px solid #ffffff"
            
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg};
                    color: {txt};
                    border: {border};
                    border-radius: 10px;
                    font-weight: bold;
                    padding: 5px;
                    font-size: 14px;
                }}
                QPushButton:hover {{ background-color: #e3f2fd; color: {COLORS["text_dark"]}; }}
            """)

    def update_slot_visuals(self):
        for i, btn in self.slot_buttons.items():
            btn.setText(self.get_slot_text(i))
            btn.selected = (i == self.selected_slot)

        has_data = self.selected_slot is not None and self.save_slots.get(self.selected_slot) is not None
        self.delete_btn.setVisible(has_data)
        self.loan_btn.setVisible(self.selected_slot is not None)
        if self.selected_slot and self.save_slots.get(self.selected_slot):
            if self.save_slots[self.selected_slot].get('loan_amount', 0) > 0:
                self.loan_btn.setText(f"LOAN: {format_currency(self.save_slots[self.selected_slot]['loan_amount'])}")
                self.loan_btn.setEnabled(False)
            else:
                self.loan_btn.setText("TAKE LOAN")
                self.loan_btn.setEnabled(True)

    def on_slot_selected(self, slot_id):
        self.selected_slot = slot_id
        self.name_input.clear()
        self.update_slot_visuals()

        data = self.save_slots.get(slot_id)
        if data:
            self.name_input.setText(data['name'])
            self.set_difficulty(data.get('difficulty', 'NORMAL'))
        else:
            self.set_difficulty('NORMAL')

    def on_delete_clicked(self):
        if self.selected_slot and self.save_slots.get(self.selected_slot):
            self.save_slots[self.selected_slot] = None
            self.save_to_file()
            self.on_slot_selected(self.selected_slot)

    def on_take_loan(self):
        if self.selected_slot is None:
            return
        if self.save_slots[self.selected_slot] is None:
            self.save_slots[self.selected_slot] = {
                "name": "Unnamed Sandwich Empire", "day": 1, "money": 100, "rank": "Beginner Chef",
                "difficulty": self.selected_diff, "location_id": 1, "unlocked": ["Bread", "Fresh Tomato"],
                "hype": 0.0, "loan_amount": 0, "loan_interest_rate": 0,
                "upgrades": [], "total_served": 0, "perfect_streak": 0,
                "ingredient_counts": {}, "discovered_recipes": [],
                "achievements_unlocked": [], "sandwich_history": [],
            }
        
        # Loan scales with location
        loc_id = self.save_slots[self.selected_slot].get('location_id', 1)
        loan_amounts = {1: 500, 2: 5000, 3: 50000, 4: 5000000, 5: 500000000, 6: 50000000000}
        loan_amount = loan_amounts.get(loc_id, 500)
        
        self.save_slots[self.selected_slot]['loan_amount'] = loan_amount
        self.save_slots[self.selected_slot]['loan_interest_rate'] = 0.1
        self.save_slots[self.selected_slot]['money'] = self.save_slots[self.selected_slot].get('money', 0) + loan_amount
        self.save_to_file()
        self.on_slot_selected(self.selected_slot)

    def on_ready_clicked(self):
        if self.selected_slot is None:
            return

        shop_name = self.name_input.text().strip()
        if not shop_name:
            shop_name = "Unnamed Sandwich Empire"
        
        if self.save_slots[self.selected_slot] is None:
            self.save_slots[self.selected_slot] = {
                "name": shop_name, 
                "day": 1, 
                "money": 100, 
                "rank": "Beginner Chef", 
                "difficulty": self.selected_diff,
                "location_id": 1,
                "unlocked": ["Bread", "Fresh Tomato"],
                "loan_amount": 0,
                "loan_interest_rate": 0,
                "hype": 0.0,
                "upgrades": [],
                "total_served": 0,
                "perfect_streak": 0,
                "ingredient_counts": {},
                "discovered_recipes": [],
                "achievements_unlocked": [],
                "sandwich_history": [],
            }
        else:
            self.save_slots[self.selected_slot]["name"] = shop_name
            self.save_slots[self.selected_slot]["difficulty"] = self.selected_diff
            # Ensure new fields exist for old saves
            self.save_slots[self.selected_slot].setdefault("upgrades", [])
            self.save_slots[self.selected_slot].setdefault("total_served", 0)
            self.save_slots[self.selected_slot].setdefault("perfect_streak", 0)
            self.save_slots[self.selected_slot].setdefault("ingredient_counts", {})
            self.save_slots[self.selected_slot].setdefault("discovered_recipes", [])
            self.save_slots[self.selected_slot].setdefault("achievements_unlocked", [])
            self.save_slots[self.selected_slot].setdefault("sandwich_history", [])

        self.save_to_file()
        self.update_slot_visuals()
        if self.switch_callback:
            self.switch_callback(Screen.GAME, self.save_slots[self.selected_slot])


class UpgradeShopScreen(QWidget):
    """Upgrade shop shown between locations."""
    def __init__(self, switch_callback=None):
        super().__init__()
        self.switch_callback = switch_callback
        self.session = {}
        self.continue_callback = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("UPGRADE SHOP")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 40px; font-weight: bold; color: #ffca28; letter-spacing: 2px;")
        layout.addWidget(title)
        
        subtitle = QLabel("Invest in permanent upgrades before your next destination!")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 18px; color: #ffffff;")
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        
        self.money_label = QLabel("")
        self.money_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.money_label.setStyleSheet("font-size: 22px; color: #ffca28; font-weight: bold;")
        layout.addWidget(self.money_label)
        layout.addSpacing(20)
        
        # Scrollable upgrade grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: rgba(0,0,0,80); border: none; border-radius: 10px;")
        
        self.upgrades_widget = QWidget()
        self.upgrades_layout = QGridLayout(self.upgrades_widget)
        self.upgrades_layout.setSpacing(15)
        scroll.setWidget(self.upgrades_widget)
        layout.addWidget(scroll, 1)
        
        layout.addSpacing(20)
        
        continue_btn = JuicyButton("CONTINUE TO NEXT LOCATION")
        continue_btn.clicked.connect(self.on_continue)
        layout.addWidget(continue_btn)
        layout.addSpacing(20)
        
        self.setLayout(layout)

    def setup_shop(self, session, continue_callback):
        self.session = session
        self.continue_callback = continue_callback
        self.money_label.setText(f"Available Cash: {format_currency(session['money'])}")
        
        # Clear existing buttons
        for i in reversed(range(self.upgrades_layout.count())):
            w = self.upgrades_layout.itemAt(i).widget()
            if w:
                w.setParent(None)
        
        owned = session.get('upgrades', [])
        row, col = 0, 0
        for name, info in UPGRADES.items():
            card = QFrame()
            card.setFixedSize(280, 180)
            card_layout = QVBoxLayout(card)
            
            is_owned = name in owned
            can_afford = session['money'] >= info['cost']
            
            if is_owned:
                card.setStyleSheet("background: rgba(76, 175, 80, 150); border: 3px solid #4caf50; border-radius: 15px;")
            elif can_afford:
                card.setStyleSheet("background: rgba(255, 202, 40, 100); border: 3px solid #ffca28; border-radius: 15px;")
            else:
                card.setStyleSheet("background: rgba(100, 100, 100, 100); border: 3px solid #666; border-radius: 15px;")
            
            name_lbl = QLabel(name)
            name_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: white; border: none;")
            name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            desc_lbl = QLabel(info['desc'])
            desc_lbl.setStyleSheet("font-size: 13px; color: #ddd; border: none;")
            desc_lbl.setWordWrap(True)
            desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            cost_lbl = QLabel(f"Cost: {format_currency(info['cost'])}" if not is_owned else "OWNED")
            cost_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffca28; border: none;")
            cost_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            card_layout.addWidget(name_lbl)
            card_layout.addWidget(desc_lbl)
            card_layout.addWidget(cost_lbl)
            
            if not is_owned and can_afford:
                buy_btn = QPushButton("BUY")
                buy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                buy_btn.setStyleSheet("background: #4caf50; color: white; border-radius: 10px; font-weight: bold; padding: 5px; font-size: 14px; border: none;")
                buy_btn.clicked.connect(lambda _, n=name, c=info['cost']: self.buy_upgrade(n, c))
                card_layout.addWidget(buy_btn)
            
            self.upgrades_layout.addWidget(card, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

    def buy_upgrade(self, name, cost):
        if self.session['money'] >= cost:
            self.session['money'] -= cost
            if 'upgrades' not in self.session:
                self.session['upgrades'] = []
            self.session['upgrades'].append(name)
            self.setup_shop(self.session, self.continue_callback)

    def on_continue(self):
        if self.continue_callback:
            self.continue_callback()


class GameScreen(QWidget):
    def __init__(self, switch_callback=None, save_callback=None):
        super().__init__()
        self.switch_callback = switch_callback
        self.save_callback = save_callback
        self.session = {}
        self.current_order = []
        self.current_sandwich = []
        self.hype = 0.0
        self.day_gross = 0
        self.day_waste = 0
        self.day_served = 0
        self.day_customers_lost = 0
        self.current_market_event = MARKET_EVENTS["Normal Market"]
        self.active_order_text = ""
        self.customer_patience = 100
        self.ingredient_discount = 1.0  # For branching event effects
        self.customer_patience_timer = QTimer(self)
        self.customer_patience_timer.timeout.connect(self.decay_patience)
        self.order_timer = QTimer(self)
        self.order_timer.timeout.connect(self.generate_order)
        self.hazard_timer = QTimer(self)
        self.hazard_timer.timeout.connect(self.trigger_environmental_hazard)
        self.sfx_achievement_player = QMediaPlayer()

        self.init_ui()
        self.spiciness = 0
        self.decay_timer = QTimer(self)
        self.decay_timer.timeout.connect(self.mechanic_update)

    def update_game_data(self, data):
        """Initializes a new gameplay session with save data."""
        self.session = data 
        self.current_location = LOCATIONS.get(data.get('location_id', 1))
        self.game_label.setText(f"{data['name'].upper()} - {self.current_location['name']}")
        
        # Reset transient state
        self.hype = data.get('hype', 0.0)
        self.spiciness = 0
        self.day_gross = 0
        self.day_waste = 0
        self.day_served = 0
        self.day_customers_lost = 0
        self.ingredient_discount = 1.0
        self.current_sandwich = []
        self.current_order = []
        self.sandwich_visual.clear()
        
        # Load lore log
        self.story_log.clear()
        if data.get('lore_log_content'):
            self.story_log.setHtml(data['lore_log_content'])
        
        self.update_tabs()
        self.refresh_stats()
        self.setup_ingredients()
        
        # Dynamic Market Event
        self.current_market_event = random.choice(list(MARKET_EVENTS.values()))
        
        # Difficulty-scaled rent
        diff = data.get('difficulty', 'NORMAL')
        rent = self.current_location['rent']
        if diff == "OVER-SCOPED":
            rent = int(rent * 1.5)
        elif diff == "EASY":
            rent = int(rent * 0.7)
        
        # Apply upgrade: rent discount
        if "rent_discount" in data.get('upgrades', []):
            rent = int(rent * 0.5)
        
        self.effective_rent = rent
        
        # Daily Briefing
        briefing = (
            f"{self.current_location['intro']}\n\n"
            f"MARKET: {self.current_market_event['message']}\n"
            f"RENT/TAX: {format_currency(self.effective_rent)}/day\n"
        )
        if data.get('loan_amount', 0) > 0:
            briefing += f"LOAN DUE: {format_currency(data['loan_amount'] * data.get('loan_interest_rate', 0.1))}/day\n"
        
        # Show difficulty info
        if diff == "OVER-SCOPED":
            briefing += "\nDIFFICULTY: OVER-SCOPED\n- 50% higher rent\n- Faster hype decay\n- Impatient customers\n- Costlier waste"
        
        # Setup SFX
        try:
            if SFX_FILES["achievement"].exists():
                self.sfx_achievement_player.setAudioOutput(self.window().audio_output)
                self.sfx_achievement_player.setSource(QUrl.fromLocalFile(str(SFX_FILES["achievement"].resolve())))
        except:
            pass

        self.customer_patience = 100
        self.customer_patience_timer.start(1000)
        self.show_story_popup("DAILY BRIEFING", briefing)
        self.generate_order()
        self.decay_timer.start(100)

        # Tutorial
        if data['day'] == 1 and data['location_id'] == 1:
            self.show_story_popup("HOW TO PLAY", 
                "1. Pick ingredients on the right.\n"
                "2. Match the CUSTOMER ORDER in the log for a 3x bonus!\n"
                "3. Click SERVE to cash in.\n"
                "4. Hit END DAY to progress. Don't go broke!\n\n"
                "TIP: Discover secret recipes for massive bonuses!")

        # Start hazard timer for locations with hazards
        if self.session.get('location_id') in [3, 4, 5]:
            self.hazard_timer.start(5000)
        else:
            self.hazard_timer.stop()
            self.window().solar_flare_active = False
            self.sandwich_visual.sandstorm_active = False

    def mechanic_update(self):
        # Spiciness Decay
        spice_resist = "spice_resist" in self.session.get('upgrades', [])
        if self.spiciness > 0:
            decay = 0.25 if spice_resist else 0.5
            self.spiciness = max(0, self.spiciness - decay)
            self.refresh_stats()
            
            shake_resist = "shake_resist" in self.session.get('upgrades', [])
            if self.spiciness > 50:
                intensity = int((self.spiciness - 50) / 10)
                if shake_resist:
                    intensity = max(0, int(intensity * 0.3))
                self.window().shake_intensity = intensity
            else:
                self.window().shake_intensity = 0

        # Jupiter Jitter Effect
        if self.session.get('location_id') == 5 and hasattr(self, 'gravity_surge_active') and self.gravity_surge_active:
            for i in range(self.ingredients_panel.count()):
                w = self.ingredients_panel.itemAt(i).widget()
                if w:
                    w.move(w.x() + random.randint(-3, 3), w.y() + random.randint(-3, 3))

        # Hype decay
        if self.hype > 0:
            decay_rate = 0.001
            if self.session.get('difficulty') == "OVER-SCOPED":
                decay_rate = 0.01  # Increased decay
            if "hype_slow" in self.session.get('upgrades', []):
                decay_rate *= 0.5
            self.hype = max(0, self.hype - decay_rate)
            self.session['hype'] = self.hype
            self.refresh_stats()

    def decay_patience(self):
        if self.current_order:
            patience_decay = 5
            if self.session.get('difficulty') == "OVER-SCOPED":
                patience_decay = 15  # Faster decay
            elif self.session.get('difficulty') == "EASY":
                patience_decay = 3
            
            if "patience_boost" in self.session.get('upgrades', []):
                patience_decay = max(1, int(patience_decay * 0.5))
            
            self.customer_patience = max(0, self.customer_patience - patience_decay)
            self.patience_bar.setValue(self.customer_patience)
            
            if self.customer_patience <= 0:
                feedback = random.choice(CUSTOMER_FEEDBACK_NEGATIVE)
                self.log_message(f"<span style='color: #ff5252;'>Customer lost patience and left!</span>")
                self.log_message(f"<i style='color: #ff8a80;'>'{feedback}'</i>")
                try:
                    self.window().play_ui_sfx("customer_leave")
                except:
                    pass
                # Penalty
                penalty = 50 * self.current_location.get('profit_mult', 1)
                if self.session.get('difficulty') == "OVER-SCOPED":
                    penalty *= 2
                self.session['money'] = max(0, self.session['money'] - penalty)
                self.hype = max(0, self.hype - 0.1)
                self.session['hype'] = self.hype
                self.day_customers_lost += 1
                self.session['perfect_streak'] = 0
                self.current_order = []
                self.current_sandwich = []
                self.sandwich_visual.clear()
                self.refresh_stats()
                self.generate_order()

    def cool_down(self):
        self.spiciness = max(0, self.spiciness - 5)
        self.log_message("<span style='color: #03a9f4;'>Clicked to cool down!</span>")

    def refresh_stats(self):
        money_str = format_currency(self.session['money'])
        hype_str = f" | Hype: {int(self.hype * 100)}%" if self.hype > 0 else ""
        loan_str = ""
        if self.session.get('loan_amount', 0) > 0:
            loan_str = f" | Loan: {format_currency(self.session['loan_amount'])} ({(self.session.get('loan_interest_rate', 0.1)*100):.0f}%)"

        spice_str = f" | HEAT: {int(self.spiciness)}%" if self.session.get('location_id') == 4 else ""
        self.stats_label.setText(
            f"Day: {self.session['day']} | Cash: {money_str} | Rank: {self.session['rank']}"
            f"{hype_str}{loan_str}{spice_str}"
        )

    def show_story_popup(self, title, message, callback=None, option_a=None, option_b=None, choice_callback=None):
        self.overlay = StoryOverlay(title, message, callback, option_a, option_b, choice_callback)
        self.overlay.setParent(self)
        geom = self.geometry()
        self.overlay.move((geom.width() - 600) // 2, (geom.height() - 450) // 2)
        self.overlay.show()

    def log_message(self, text):
        self.story_log.append(f"<p style='margin-bottom: 8px;'>{text}</p>")
        self.story_log.verticalScrollBar().setValue(self.story_log.verticalScrollBar().maximum())

    def generate_order(self):
        unlocked = self.session.get('unlocked', ["Bread"])
        loc_id = self.session.get('location_id', 1)
        
        num = random.randint(2, 4)
        if loc_id == 6:
            num = random.randint(6, 10)
        
        self.customer_patience = 100
        self.patience_bar.setValue(100)
        self.customer_patience_timer.start(1000)
            
        self.current_order = [random.choice(unlocked) for _ in range(num)]
        
        if "Bread" in unlocked and "Bread" not in self.current_order:
            self.current_order[0] = "Bread"
            
        self.active_order_text = ", ".join(self.current_order)
        self.display_current_order()
        self.log_message(f"<i style='color: #888;'>Customer says: \"{random.choice(CUSTOMER_QUOTES)}\"</i>")

    def display_current_order(self):
        """Helper to display order, respecting scrambler hazards."""
        if not self.current_order:
            return
            
        if self.window().solar_flare_active:
            # Scramble the text
            chars = list(self.active_order_text)
            random.shuffle(chars)
            display_text = "".join(chars)
            self.log_message(f"<span style='color: #ffca28;'><b>ORDER:</b> <span style='background: #fff; color: #000;'>{display_text}</span> [SIGNAL LOST]</span>")
        else:
            self.log_message(f"<span style='color: #ffca28;'><b>ORDER:</b> Wants {self.active_order_text}</span>")

    def setup_ingredients(self):
        for i in reversed(range(self.ingredients_panel.count())): 
            w = self.ingredients_panel.itemAt(i).widget()
            if w:
                w.setParent(None)
            
        for ing in self.session.get('unlocked', []):
            base_cost = INGREDIENTS[ing]['cost']
            # Apply market event
            market_mult = 1.0
            if self.current_market_event.get('ingredient') == ing:
                market_mult = self.current_market_event.get('cost_mult', 1.0)
            
            effective_cost = base_cost * market_mult * self.ingredient_discount
            
            # Hazard: Sandstorm hides info
            if self.sandwich_visual.sandstorm_active:
                btn_text = "??? ($ ???)"
            else:
                btn_text = f"{ing} (${int(effective_cost)})"
                
            btn = JuicyButton(btn_text)
            btn.setFixedHeight(50)
            btn.clicked.connect(lambda _, x=ing: self.add_ingredient(x))
            
            if market_mult != 1.0:
                btn.setStyleSheet(btn.styleSheet() + "background-color: #ef5350;")

            self.ingredients_panel.addWidget(btn)

    def add_ingredient(self, name):
        base_cost = INGREDIENTS[name]['cost']
        market_mult = 1.0
        if self.current_market_event.get('ingredient') == name:
            market_mult = self.current_market_event.get('cost_mult', 1.0)
        
        cost = base_cost * market_mult * self.ingredient_discount
        
        if self.session['money'] >= cost:
            self.session['money'] -= cost
            self.current_sandwich.append(name)
            self.sandwich_visual.add_ingredient(name)
            try:
                self.window().play_ui_sfx("ingredients", ingredient_name=name)
            except:
                pass
            self.log_message(f"Added <b>{name}</b> (-{format_currency(cost)})")
            
            # Track ingredient usage
            counts = self.session.get('ingredient_counts', {})
            counts[name] = counts.get(name, 0) + 1
            self.session['ingredient_counts'] = counts
            
            self.refresh_stats()
            if name == "Martian Pepper":
                spice_amt = 10 if "spice_resist" in self.session.get('upgrades', []) else 20
                self.spiciness += spice_amt
        else:
            self.log_message(f"<span style='color: red;'>Too broke for {name}!</span>")

    def clear_sandwich(self):
        if not self.current_sandwich:
            return
        waste_mult = 1.0 if self.session.get('difficulty') == "OVER-SCOPED" else 0.5
        waste_fee = sum(INGREDIENTS[i]['cost'] for i in self.current_sandwich) * waste_mult
        self.session['money'] = max(0, self.session['money'] - waste_fee)
        self.day_waste += waste_fee
        self.log_message(f"<span style='color: #ff5252;'>Sandwich trashed. Bio-Waste Fee: -{format_currency(waste_fee)}</span>")
        self.current_sandwich = []
        self.sandwich_visual.clear()
        self.refresh_stats()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QHBoxLayout()
        self.game_label = QLabel("SANDWICH EMPIRE")
        self.game_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffffff;")
        
        exit_btn = JuicyButton("X")
        exit_btn.setFixedSize(60, 60)
        exit_btn.clicked.connect(self.exit_to_menu)
        
        header.addWidget(self.game_label, 1)
        header.addWidget(exit_btn)
        layout.addLayout(header)

        self.stats_label = QLabel("")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_label.setStyleSheet("font-size: 20px; color: #3e2723; background: #ffca28; padding: 10px; border-radius: 10px;")
        layout.addWidget(self.stats_label)

        # Gameplay Area
        gameplay_layout = QHBoxLayout()
        
        # Left: Narrative Log + Tabs
        left_panel = QVBoxLayout()
        
        self.left_tabs = QTabWidget()
        self.left_tabs.setStyleSheet("""
            QTabWidget::pane { background: rgba(0,0,0,200); border-radius: 10px; border: none; }
            QTabBar::tab { background: rgba(50,50,50,180); color: #aaa; padding: 8px 12px; font-weight: bold; border: none; border-top-left-radius: 8px; border-top-right-radius: 8px; }
            QTabBar::tab:selected { background: rgba(255,202,40,200); color: #3e2723; }
        """)
        
        # Log tab
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        log_layout.setContentsMargins(0, 0, 0, 0)
        self.story_log = QTextEdit()
        self.story_log.setReadOnly(True)
        self.story_log.setStyleSheet("background: rgba(0, 0, 0, 50); color: #e0e0e0; border: none; font-family: 'Consolas'; font-size: 14px;")
        log_layout.addWidget(self.story_log)
        self.left_tabs.addTab(log_widget, "LOG")
        
        # Lore tab
        lore_widget = QWidget()
        lore_layout = QVBoxLayout(lore_widget)
        lore_layout.setContentsMargins(0, 0, 0, 0)
        self.lore_log = QTextEdit()
        self.lore_log.setReadOnly(True)
        self.lore_log.setStyleSheet("background: rgba(0, 0, 0, 50); color: #e0e0e0; border: none; font-family: 'Consolas'; font-size: 14px;")
        lore_layout.addWidget(self.lore_log)
        self.left_tabs.addTab(lore_widget, "LORE")
        
        # Achievements tab
        achiev_widget = QWidget()
        achiev_layout = QVBoxLayout(achiev_widget)
        achiev_layout.setContentsMargins(0, 0, 0, 0)
        self.achievements_log = QTextEdit()
        self.achievements_log.setReadOnly(True)
        self.achievements_log.setStyleSheet("background: rgba(0, 0, 0, 50); color: #e0e0e0; border: none; font-family: 'Consolas'; font-size: 14px;")
        achiev_layout.addWidget(self.achievements_log)
        self.left_tabs.addTab(achiev_widget, "ACHIEVEMENTS")
        
        # Collectibles tab
        collect_widget = QWidget()
        collect_layout = QVBoxLayout(collect_widget)
        collect_layout.setContentsMargins(0, 0, 0, 0)
        self.collectibles_log = QTextEdit()
        self.collectibles_log.setReadOnly(True)
        self.collectibles_log.setStyleSheet("background: rgba(0, 0, 0, 50); color: #e0e0e0; border: none; font-family: 'Consolas'; font-size: 14px;")
        collect_layout.addWidget(self.collectibles_log)
        self.left_tabs.addTab(collect_widget, "COLLECTION")
        
        # Sandwich History tab
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.setContentsMargins(0, 0, 0, 0)
        self.history_log = QTextEdit()
        self.history_log.setReadOnly(True)
        self.history_log.setStyleSheet("background: rgba(0, 0, 0, 50); color: #e0e0e0; border: none; font-family: 'Consolas'; font-size: 14px;")
        history_layout.addWidget(self.history_log)
        self.left_tabs.addTab(history_widget, "HISTORY")
        
        self.left_tabs.setFixedWidth(350)
        left_panel.addWidget(self.left_tabs)
        
        # Middle: Prep Table
        self.prep_table = QVBoxLayout()
        
        self.patience_bar = QProgressBar()
        self.patience_bar.setRange(0, 100)
        self.patience_bar.setValue(100)
        self.patience_bar.setTextVisible(True)
        self.patience_bar.setFormat("Customer Patience: %v%")
        self.patience_bar.setStyleSheet("""
            QProgressBar { background: #333; border-radius: 8px; text-align: center; color: white; font-weight: bold; font-size: 13px; height: 22px; }
            QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4caf50, stop:0.7 #ffca28, stop:1 #f44336); border-radius: 8px; }
        """)
        
        self.sandwich_visual = SandwichRenderer()
        self.prep_table.addWidget(self.patience_bar)
        self.prep_table.addWidget(self.sandwich_visual)
        
        # Right: Ingredients
        self.ingredients_panel = QVBoxLayout()
        self.ingredients_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Action Bar
        actions = QHBoxLayout()
        clear_btn = JuicyButton("TRASH IT")
        clear_btn.clicked.connect(self.clear_sandwich)
        
        serve_btn = JuicyButton("SERVE SANDWICH")
        serve_btn.clicked.connect(self.serve_sandwich)
        
        next_day_btn = JuicyButton("END DAY")
        next_day_btn.clicked.connect(self.next_day)
        
        actions.addWidget(clear_btn)
        actions.addWidget(serve_btn)
        actions.addWidget(next_day_btn)
        
        gameplay_layout.addLayout(left_panel)
        gameplay_layout.addLayout(self.prep_table, 1)
        gameplay_layout.addLayout(self.ingredients_panel)
        
        layout.addLayout(gameplay_layout, 1)
        layout.addLayout(actions)

        self.setLayout(layout)

    def exit_to_menu(self):
        # Stop all timers
        self.decay_timer.stop()
        self.customer_patience_timer.stop()
        self.order_timer.stop()
        self.hazard_timer.stop()
        if self.save_callback:
            self.save_callback()
        self.switch_callback(Screen.MAIN_MENU)

    def serve_sandwich(self):
        if not self.current_sandwich or not self.current_order:
            return
        
        self.customer_patience_timer.stop()
        self.order_timer.stop()
        
        # Order Matching
        matched = sorted(self.current_sandwich) == sorted(self.current_order)
        loc_mult = self.current_location.get('profit_mult', 1)
        diff = self.session.get('difficulty', 'NORMAL')

        if matched:
            multiplier = 3.0
            # Secret Recipe Bonus
            secret_bonus = 1.0
            recipe_name_found = None
            current_sandwich_tuple = tuple(sorted(self.current_sandwich))
            for recipe_name, recipe_data in SECRET_RECIPES.items():
                if current_sandwich_tuple == tuple(sorted(recipe_data["ingredients"])):
                    secret_bonus = recipe_data["bonus_mult"]
                    recipe_name_found = recipe_name
                    # Recipe boost upgrade doubles it
                    if "recipe_boost" in self.session.get('upgrades', []):
                        secret_bonus *= 2
                    
                    # Track discovered recipes
                    discovered = self.session.get('discovered_recipes', [])
                    if recipe_name not in discovered:
                        discovered.append(recipe_name)
                        self.session['discovered_recipes'] = discovered
                        self.log_message(f"<span style='color: #9c27b0;'>NEW SECRET RECIPE DISCOVERED: {recipe_name}! x{int(secret_bonus)} Bonus!</span>")
                        self.add_lore_entry(f"Discovered the secret recipe: '{recipe_name}'!")
                    else:
                        self.log_message(f"<span style='color: #9c27b0;'>Secret Recipe: {recipe_name}! x{int(secret_bonus)} Bonus!</span>")
                    break

            # Spiciness Bonus
            spice_bonus = 1.0 + (self.spiciness / 100.0)

            # Achievement Permanent Multipliers
            ach_mult = 1.0
            unlocked_achs = self.session.get('achievements_unlocked', [])
            for name, ach in ACHIEVEMENTS.items():
                if name in unlocked_achs and ach['reward'].startswith("money_mult_"):
                    ach_mult *= float(ach['reward'].replace("money_mult_", ""))

            # Market event value changes
            market_value_mult = self.current_market_event.get('value_mult', 1.0)
            # Value boost upgrade
            value_boost = 1.25 if "value_boost" in self.session.get('upgrades', []) else 1.0
            
            total_value = (sum(INGREDIENTS[i]['value'] for i in self.current_sandwich) * 
                           multiplier * loc_mult * spice_bonus * (1 + self.hype) * 
                           secret_bonus * market_value_mult * value_boost * ach_mult)
        else:
            # Mismatch logic based on difficulty
            raw_cost = sum(INGREDIENTS[i]['cost'] for i in self.current_sandwich)
            raw_value = sum(INGREDIENTS[i]['value'] for i in self.current_sandwich)
            
            if diff == "EASY":
                # Get raw value, but no order bonus or other multipliers
                total_value = raw_value * loc_mult
            elif diff == "NORMAL":
                # Exactly what you paid (refunding costs)
                total_value = raw_cost * loc_mult
            else: # OVER-SCOPED
                # Lose money proportional to what you spent
                total_value = -0.5 * raw_cost * loc_mult

        # Location Inflation
        # loc_mult = self.current_location.get('profit_mult', 1) # Moved up
        # Market event value changes
        # market_value_mult = self.current_market_event.get('value_mult', 1.0) # Used only in matched
        # Value boost upgrade
        # value_boost = 1.25 if "value_boost" in self.session.get('upgrades', []) else 1.0 # Used only in matched
        
        self.session['money'] += total_value
        self.day_gross += total_value
        self.day_served += 1
        
        # Track total served
        self.session['total_served'] = self.session.get('total_served', 0) + 1
        
        # Generate sandwich name
        sand_name = generate_sandwich_name(self.current_sandwich)
        
        # Add to sandwich history (collectibles)
        history = self.session.get('sandwich_history', [])
        history_entry = {
            "name": sand_name,
            "ingredients": list(self.current_sandwich),
            "value": total_value,
            "day": self.session['day'],
            "location": self.current_location['name']
        }
        history.append(history_entry)
        if len(history) > 100:  # Keep last 100
            history = history[-100:]
        self.session['sandwich_history'] = history
        
        # Also add to global collectibles
        global_collectibles = load_collectibles()
        global_history = global_collectibles.get('sandwich_history', [])
        global_history.append(history_entry)
        if len(global_history) > 500:
            global_history = global_history[-500:]
        global_collectibles['sandwich_history'] = global_history
        save_collectibles(global_collectibles)
        
        try:
            self.window().play_ui_sfx("serve_sandwich")
        except:
            pass
        
        if matched:
            self.log_message(f"<span style='color: #4caf50;'>PERFECT MATCH! '{sand_name}' earned {format_currency(total_value)}</span>")
            feedback = random.choice(CUSTOMER_FEEDBACK_POSITIVE)
            self.log_message(f"<i style='color: #81c784;'>'{feedback}'</i>")
            self.hype = min(2.0, self.hype + 0.05)
            self.session['hype'] = self.hype
            self.session['perfect_streak'] = self.session.get('perfect_streak', 0) + 1
            
            # Tip based on hype
            if random.random() < 0.3 + self.hype * 0.1:
                tip = total_value * 0.15 * (1 + self.hype)
                self.session['money'] += tip
                self.log_message(f"<span style='color: #ffca28;'>TIP: +{format_currency(tip)}! Hype UP!</span>")
        

            self.add_lore_entry(f"Customer was delighted by your '{sand_name}'!")
        else:
            self.log_message(f"Served '{sand_name}' for {format_currency(total_value)} (Order mismatch).")
            self.session['perfect_streak'] = 0
        
        # Check for collectibles
        self.check_collectible_drop()
        
        # Check achievements
        self.check_achievements()
            
        self.current_sandwich = []
        self.current_order = []
        self.sandwich_visual.clear()
        self.spiciness = 0
        self.refresh_stats()
        self.update_tabs()
        self.generate_order()

    def check_collectible_drop(self):
        """Check if a collectible drops after serving."""
        loc_id = self.session.get('location_id', 1)
        available_collectibles = COLLECTIBLE_ITEMS.get(loc_id, [])
        global_data = load_collectibles()
        collected = global_data.get('collected', [])
        
        for item in available_collectibles:
            if item['id'] not in collected and random.random() < item['chance']:
                collected.append(item['id'])
                global_data['collected'] = collected
                save_collectibles(global_data)
                self.log_message(f"<span style='color: #ffd700;'>COLLECTIBLE FOUND: {item['name']}!</span>")
                self.log_message(f"<i style='color: #ffecb3;'>{item['desc']}</i>")
                self.add_lore_entry(f"Found collectible: {item['name']} - {item['desc']}")
                break

    def check_achievements(self):
        """Check and unlock achievements."""
        unlocked = self.session.get('achievements_unlocked', [])
        for name, ach in ACHIEVEMENTS.items():
            if name not in unlocked and ach['check'](self.session):
                unlocked.append(name)
                self.session['achievements_unlocked'] = unlocked
                self.log_message(f"<span style='color: #ffd700;'>ACHIEVEMENT UNLOCKED: {name}!</span>")
                self.log_message(f"<i style='color: #fff9c4;'>{ach['desc']}</i>")
                
                try:
                    if self.sfx_achievement_player.source() != QUrl():
                        self.sfx_achievement_player.play()
                except:
                    pass

                self.add_lore_entry(f"Achievement unlocked: {name} - {ach['desc']}")
                
                # Apply reward
                reward = ach['reward']
                if reward.startswith("money_mult_"):
                    # Permanent multiplier stored as upgrade
                    mult_val = reward.replace("money_mult_", "")
                    self.log_message(f"<span style='color: #4caf50;'>Reward: Permanent {mult_val}x profit multiplier!</span>")
                elif reward.startswith("money_"):
                    amount = float(reward.replace("money_", ""))
                    self.session['money'] += amount
                    self.log_message(f"<span style='color: #4caf50;'>Reward: +{format_currency(amount)}!</span>")
                elif reward.startswith("hype_"):
                    amount = float(reward.replace("hype_", ""))
                    self.hype = min(2.0, self.hype + amount)
                    self.session['hype'] = self.hype
                    self.log_message(f"<span style='color: #4caf50;'>Reward: +{int(amount*100)}% Hype!</span>")

    def add_lore_entry(self, text):
        """Add an entry to the lore log."""
        day = self.session.get('day', 1)
        loc = self.current_location['name']
        self.lore_log.append(f"<p style='color: #ffca28;'><b>[Day {day} - {loc}]</b></p>")
        self.lore_log.append(f"<p style='color: #e0e0e0;'>{text}</p><br>")

    def update_tabs(self):
        """Refresh achievement, collectible, and history tabs."""
        # Achievements
        self.achievements_log.clear()
        unlocked = self.session.get('achievements_unlocked', [])
        for name, ach in ACHIEVEMENTS.items():
            if name in unlocked:
                self.achievements_log.append(f"<p style='color: #4caf50;'><b>[DONE] {name}</b> - {ach['desc']}</p>")
            else:
                self.achievements_log.append(f"<p style='color: #666;'><b>[   ] {name}</b> - {ach['desc']}</p>")
        
        # Collectibles
        self.collectibles_log.clear()
        global_data = load_collectibles()
        collected = global_data.get('collected', [])
        
        for loc_id in sorted(COLLECTIBLE_ITEMS.keys()):
            loc_name = LOCATIONS[loc_id]['name']
            self.collectibles_log.append(f"<p style='color: #ffca28;'><b>== {loc_name} ==</b></p>")
            for item in COLLECTIBLE_ITEMS[loc_id]:
                if item['id'] in collected:
                    self.collectibles_log.append(f"<p style='color: #4caf50;'><b>{item['name']}</b> - {item['desc']}</p>")
                else:
                    self.collectibles_log.append(f"<p style='color: #555;'>??? - Undiscovered</p>")
        
        # Sandwich History
        self.history_log.clear()
        history = self.session.get('sandwich_history', [])
        for entry in reversed(history[-50:]):
            ings = ", ".join(entry.get('ingredients', []))
            self.history_log.append(
                f"<p style='color: #ffca28;'><b>{entry['name']}</b></p>"
                f"<p style='color: #bbb;'>{ings} | {format_currency(entry.get('value', 0))} | Day {entry.get('day', '?')} @ {entry.get('location', '?')}</p><br>"
            )

    def trigger_victory(self, is_win=True):
        # Mark game as completed
        self.session['game_completed'] = True
        if self.save_callback:
            self.save_callback()
        
        if is_win:
            title = "THE 6 QUINTILLION DOLLAR DREAM"
            msg = "You finally have it. The 6 Quintillion credits needed for ATG 6.\n\nYou rush to the Chockster Gumes HQ to buy the game, but the windows are boarded up.\n\nBREAKING NEWS: Chockster Gumes has run out of money. ATG 6 is canceled indefinitely.\n\nYour fortune is worthless in a world without the game."
            end_msg = "You stare into Ton-216's darkness, feeling yourself unravel.\nYou jump into the black hole.\n\n'The Universe Tasted Well.' (At least you tied Ending)"
        else:
            title = "FAILED INVESTMENT"
            msg = f"It is Day 40. You have {format_currency(self.session['money'])}, but ATG 6 costs 6.00Q.\n\nChockster Gumes ignores your calls. You are just another failed entrepreneur in a cold, sandwich-less universe."
            end_msg = "The crushing weight of failure is heavier than the black hole's gravity.\nYou jump into Ton-216.\n\n'Everything was Soggy.' (Bad Ending)"

        self.show_story_popup(title, msg, 
            lambda: self.show_story_popup("THE END", end_msg, 
                lambda: self.switch_callback(Screen.MAIN_MENU)))

    def next_day(self):
        # Stop timers
        self.decay_timer.stop()
        self.customer_patience_timer.stop()
        self.order_timer.stop()
        self.hazard_timer.stop()

        rent = self.effective_rent
        self.session['money'] -= rent
        
        # Loan interest
        loan_interest = 0
        if self.session.get('loan_amount', 0) > 0:
            loan_interest = self.session['loan_amount'] * self.session.get('loan_interest_rate', 0.1)
            self.session['money'] -= loan_interest

        # End-of-Day Analytics
        net = self.day_gross - self.day_waste - rent - loan_interest
        rent_name = self.current_location.get('rent_name', 'Rent')
        satisfaction = max(0, 100 - self.day_customers_lost * 20 + self.day_served * 5)
        satisfaction = min(100, satisfaction)
        
        summary = (
            f"<b>DAY {self.session['day']} ANALYTICS:</b>\n\n"
            f"Sandwiches Served: {self.day_served}\n"
            f"Customers Lost: {self.day_customers_lost}\n"
            f"Gross Profit: {format_currency(self.day_gross)}\n"
            f"Bio-Waste Fees: -{format_currency(self.day_waste)}\n"
            f"{rent_name}: -{format_currency(rent)}\n"
        )
        if loan_interest > 0:
            summary += f"Loan Interest: -{format_currency(loan_interest)}\n"
        summary += (
            f"\nNet Profit: {format_currency(net)}\n"
            f"Customer Satisfaction: {satisfaction}%\n"
            f"Hype Level: {int(self.hype * 100)}%"
        )
        
        self.session['day'] += 1
        self.session['lore_log_content'] = self.story_log.toHtml()
        
        # Add daily lore
        self.add_lore_entry(f"Day {self.session['day'] - 1} summary: Served {self.day_served} sandwiches, earned {format_currency(self.day_gross)}.")
        
        # Check location transition
        loc_data = self.current_location
        if self.session['day'] > loc_data['days']:
            if self.session['location_id'] == 6:
                self.trigger_victory(is_win=(self.session['money'] >= loc_data['req']))
                return

            if self.session['money'] >= loc_data['req']:
                success_text = loc_data['success_msg']
                def transition():
                    # Show upgrade shop before transitioning
                    self.session['location_id'] += 1
                    new_loc = LOCATIONS[self.session['location_id']]
                    self.session['rank'] = new_loc['rank']
                    for name, info in INGREDIENTS.items():
                        if info['loc'] == self.session['location_id'] and name not in self.session['unlocked']:
                            self.session['unlocked'].append(name)
                    
                    self.add_lore_entry(f"Moved to {new_loc['name']}! Rank: {new_loc['rank']}")
                    
                    # Show upgrade shop
                    main_window = self.window()
                    main_window.upgrade_shop.setup_shop(self.session, self.finish_transition)
                    main_window.stack.setCurrentIndex(Screen.UPGRADE_SHOP)
                
                self.show_story_popup("LOCATION COMPLETE", f"{summary}\n\n{success_text}", transition)
            else:
                self.show_story_popup("BANKRUPTCY", f"{summary}\n\n{loc_data['fail']}", 
                    lambda: self.switch_callback(Screen.MAIN_MENU))
        elif self.session['money'] < 0:
            self.show_story_popup("DEBT SINGULARITY", 
                f"{summary}\n\nYou owe the intergalactic bank too much. You are now a permanent part of the supply chain.", 
                lambda: self.switch_callback(Screen.MAIN_MENU))
        else:
            # Branching narrative event (30% chance)
            if random.random() < 0.3 and self.session['day'] > 2:
                self.trigger_branching_event(summary)
            else:
                self.show_story_popup("DAY OVER", summary, self.start_next_day_mechanics)

        # Reset daily counters
        self.day_gross = 0
        self.day_waste = 0
        self.day_served = 0
        self.day_customers_lost = 0
        self.ingredient_discount = 1.0  # Reset ingredient discount
        self.refresh_stats()
        
        if self.save_callback:
            self.save_callback()
            
        self.log_message(f"<b>Day {self.session['day']} begins.</b>")
        
        # New market event for the day
        self.current_market_event = random.choice(list(MARKET_EVENTS.values()))
        self.setup_ingredients()
        self.update_tabs()

    def finish_transition(self):
        """Called after upgrade shop to resume game at new location."""
        main_window = self.window()
        main_window.update_music(self.session['location_id'])
        main_window.update_background_image(self.session['location_id'])
        self.update_game_data(self.session)
        main_window.stack.setCurrentIndex(Screen.GAME)

    def trigger_branching_event(self, day_summary):
        """Trigger a branching narrative event."""
        event = random.choice(BRANCHING_EVENTS)
        
        full_text = f"{day_summary}\n\n--- EVENT ---\n{event['text']}"
        
        def on_choice(choice):
            if choice == "a":
                effects = event.get('effect_a', {})
                self.log_message(f"<span style='color: #ffca28;'>You chose: {event['option_a']}</span>")
            else:
                effects = event.get('effect_b', {})
                self.log_message(f"<span style='color: #ffca28;'>You chose: {event['option_b']}</span>")
            
            # Apply effects
            if 'hype' in effects:
                self.hype = max(0, min(2.0, self.hype + effects['hype']))
                self.session['hype'] = self.hype
                if effects['hype'] > 0:
                    self.log_message(f"<span style='color: #4caf50;'>Hype +{int(effects['hype']*100)}%!</span>")
                elif effects['hype'] < 0:
                    self.log_message(f"<span style='color: #ff5252;'>Hype {int(effects['hype']*100)}%!</span>")
            
            if 'money_mult' in effects:
                if effects['money_mult'] > 0:
                    bonus = self.session['money'] * (effects['money_mult'] - 1)
                    self.session['money'] += bonus
                    self.log_message(f"<span style='color: #4caf50;'>Money bonus: +{format_currency(bonus)}!</span>")
                elif effects['money_mult'] < 0:
                    penalty = abs(self.session['money'] * effects['money_mult'])
                    self.session['money'] = max(0, self.session['money'] - penalty)
                    self.log_message(f"<span style='color: #ff5252;'>Money penalty: -{format_currency(penalty)}!</span>")
            
            if 'ingredient_discount' in effects:
                self.ingredient_discount = effects['ingredient_discount']
                self.log_message(f"<span style='color: #4caf50;'>Ingredient discount: {int(effects['ingredient_discount']*100)}% tomorrow!</span>")
            
            if effects.get('competition'):
                if random.random() < 0.5:
                    prize = self.session['money'] * 0.5
                    self.session['money'] += prize
                    self.hype = min(2.0, self.hype + 0.2)
                    self.session['hype'] = self.hype
                    self.log_message(f"<span style='color: #4caf50;'>You WON the competition! +{format_currency(prize)} and Hype UP!</span>")
                else:
                    self.hype = max(0, self.hype - 0.15)
                    self.session['hype'] = self.hype
                    self.log_message(f"<span style='color: #ff5252;'>You LOST the competition! Hype down.</span>")
            
            self.add_lore_entry(f"Event: {event['title']} - Choice: {'A' if choice == 'a' else 'B'}")
            self.refresh_stats()
            self.start_next_day_mechanics()
        
        self.show_story_popup(event['title'], full_text, None,
            option_a=event['option_a'], option_b=event['option_b'],
            choice_callback=on_choice)

    def start_next_day_mechanics(self):
        """Restart timers after day summary popup is closed."""
        self.decay_timer.start(100)
        self.customer_patience_timer.start(1000)
        if self.session.get('location_id') in [3, 4, 5]:
            self.hazard_timer.start(5000)
        else:
            self.hazard_timer.stop()
            self.window().solar_flare_active = False
            self.sandwich_visual.sandstorm_active = False
        self.generate_order()

    def trigger_environmental_hazard(self):
        loc_id = self.session.get('location_id')
        if loc_id == 3:  # Moon: Solar Flare
            if random.random() < 0.2:
                self.log_message("<span style='color: #ff9800;'>WARNING: Solar Flare detected! Expect visual interference.</span>")
                self.window().solar_flare_active = True
                self.display_current_order() # Scramble existing log
                QTimer.singleShot(random.randint(3000, 8000), self.clear_environmental_hazard)
        elif loc_id == 4:  # Mars: Sandstorm
            if random.random() < 0.2:
                self.log_message("<span style='color: #bf360c;'>WARNING: Martian Sandstorm approaching! Visibility reduced.</span>")
                self.sandwich_visual.sandstorm_active = True
                self.setup_ingredients() # Hide ingredient names
                QTimer.singleShot(random.randint(3000, 8000), self.clear_environmental_hazard)
        elif loc_id == 5:  # Jupiter: Gravity Surge
            if random.random() < 0.2:
                self.log_message("<span style='color: #4a148c;'>WARNING: Gravitational Surge! Controls malfunctioning.</span>")
                self.gravity_surge_active = True
                QTimer.singleShot(random.randint(4000, 7000), self.clear_environmental_hazard)

    def clear_environmental_hazard(self):
        loc_id = self.session.get('location_id')
        if loc_id == 3:
            self.window().solar_flare_active = False
            self.log_message("<span style='color: #4caf50;'>Solar Flare subsided.</span>")
            self.display_current_order() # Restore order text
        elif loc_id == 4:
            self.sandwich_visual.sandstorm_active = False
            self.log_message("<span style='color: #4caf50;'>Sandstorm passed.</span>")
            self.setup_ingredients() # Restore ingredient names
        elif loc_id == 5:
            self.gravity_surge_active = False
            self.log_message("<span style='color: #4caf50;'>Gravity stabilized.</span>")
        if self.session.get('location_id') in [3, 4, 5]:
            self.hazard_timer.start(random.randint(10000, 20000))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Over-Scoped Sandwich Simulator")

        # Audio Setup
        self.current_bg_pixmap = None
        self.current_bg_id = 0 # 0 for menu
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)

        # Try default music
        self.current_music_file = MUSIC_FILE
        if MUSIC_FILE.exists():
            self.player.setSource(QUrl.fromLocalFile(str(MUSIC_FILE.resolve())))
        elif LOCATIONS[1]["music_file"].exists():
            self.current_music_file = LOCATIONS[1]["music_file"]
            self.player.setSource(QUrl.fromLocalFile(str(self.current_music_file.resolve())))
        self.audio_output.setVolume(0.5)
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.player.play()

        # Background Animation
        self.time_counter = 0
        self.particles = []
        self.shake_intensity = 0
        self.solar_flare_active = False
        
        self.bg_timer = QTimer(self)
        self.bg_timer.timeout.connect(self.update_bg)
        self.bg_timer.start(30)

        # Main Stack
        self.stack = QStackedWidget()
        
        def navigate(index, data=None):
            if index == Screen.MAIN_MENU:
                self.update_background_image(0)
            if index == Screen.GAME and data:
                self.update_music(data['location_id'])
                self.update_background_image(data['location_id'])
                self.game_screen.update_game_data(data)
            self.stack.setCurrentIndex(index)

        self.main_menu = MainMenu(self.audio_output, navigate)
        self.save_menu = SaveSlotMenu(navigate)
        self.game_screen = GameScreen(navigate, self.save_menu.save_to_file)
        self.upgrade_shop = UpgradeShopScreen(navigate)

        self.main_menu.player = self.player

        self.stack.addWidget(self.main_menu)     # 0
        self.stack.addWidget(self.save_menu)     # 1
        self.stack.addWidget(self.game_screen)   # 2
        self.stack.addWidget(self.upgrade_shop)  # 3
        
        self.setCentralWidget(self.stack)
        self.update_background_image(0) # Start with menu background

        # Borderless Fullscreen
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

    def update_background_image(self, location_id):
        """Caches the background image for the current location."""
        self.current_bg_id = location_id
        path = None
        if location_id == 0:
            path = IMAGES_DIR / "bg_menu.png"
        else:
            path = LOCATIONS.get(location_id, {}).get("bg_file")

        if path and path.exists():
            self.current_bg_pixmap = QPixmap(str(path.resolve()))
        else:
            self.current_bg_pixmap = None

        # Initialize particles for the new environment
        self.particles = []
        count = 40
        for _ in range(count):
            self.particles.append({
                'pos': QPoint(random.randint(0, 1920), random.randint(0, 1080)),
                'speed': random.uniform(0.5, 2.0),
                'size': random.randint(2, 6),
                'alpha': random.randint(50, 150),
                'phase': random.uniform(0, 6.28)
            })

    def play_ui_sfx(self, sfx_key, ingredient_name=None):
        """Global helper to play UI sounds."""
        path = None
        if ingredient_name:
            path = SFX_FILES.get("ingredients", {}).get(ingredient_name)
        elif sfx_key in SFX_FILES:
            path = SFX_FILES[sfx_key]
            
        if path and path.exists():
            # Create a one-shot player that cleans up after itself
            player = QMediaPlayer(self)
            output = QAudioOutput(player)
            player.setAudioOutput(output)
            output.setVolume(self.audio_output.volume())
            # Use resolve() to handle absolute paths with spaces on Windows
            player.setSource(QUrl.fromLocalFile(str(path.resolve())))
            player.play()

    def update_music(self, location_id):
        new_music_file = LOCATIONS.get(location_id, LOCATIONS[1]).get("music_file", MUSIC_FILE)
        if new_music_file.exists() and new_music_file != self.current_music_file:
            # Stop before changing source to ensure FFmpeg releases the file handle
            self.player.stop()
            self.player.setSource(QUrl.fromLocalFile(str(new_music_file.resolve())))
            self.player.play()
            self.current_music_file = new_music_file

    def update_bg(self):
        self.time_counter += 0.01
        
        # Update atmospheric particles
        loc_id = self.current_bg_id
        for p in self.particles:
            if loc_id == 4: # Mars: Horizontal sand drift
                p['pos'].setX(int(p['pos'].x() - (p['speed'] * 5)))
                if p['pos'].x() < -50: p['pos'].setX(self.width() + 50)
            elif loc_id == 5: # Jupiter: Fast chaotic movement
                p['pos'].setY(int(p['pos'].y() + (p['speed'] * 8)))
                p['pos'].setX(int(p['pos'].x() + math.sin(self.time_counter + p['phase']) * 5))
                if p['pos'].y() > self.height() + 50: p['pos'].setY(-50)
            else: # Default: Gentle float
                p['pos'].setY(int(p['pos'].y() - p['speed']))
                p['pos'].setX(int(p['pos'].x() + math.sin(self.time_counter + p['phase'])))
                if p['pos'].y() < -50: p['pos'].setY(self.height() + 50)
        self.update()

    def paintEvent(self, event):
        loc_id = self.current_bg_id
        loc_data = LOCATIONS.get(loc_id, LOCATIONS[1])
        sky_colors = loc_data.get('sky', [COLORS["sky_top"], COLORS["sky_bottom"]])

        # 0. Parallax Math
        px = math.sin(self.time_counter * 0.5) * 15
        py = math.cos(self.time_counter * 0.3) * 10

        # Screen Shake
        sx, sy = 0, 0
        if self.shake_intensity > 0 or loc_id == 5:
            base_shake = self.shake_intensity + (2 if loc_id == 5 else 0)
            sx = random.randint(-base_shake, base_shake)
            sy = random.randint(-base_shake, base_shake)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.solar_flare_active:
            painter.setOpacity(0.3 + random.random() * 0.4)
            painter.setBrush(QColor(255, random.randint(100, 200), 0, random.randint(50, 150)))
            painter.drawRect(self.rect())
            painter.setOpacity(1.0)

        # 1. Background with Parallax
        painter.save()
        painter.translate(sx + px, sy + py)
        if self.current_bg_pixmap:
            # Scale up slightly to avoid seeing edges during parallax/shake
            painter.drawPixmap(self.rect().adjusted(-40, -40, 40, 40), self.current_bg_pixmap)
        else:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0.0, QColor(sky_colors[0]))
            gradient.setColorAt(1.0, QColor(sky_colors[1]))
            painter.fillRect(self.rect().adjusted(-10, -10, 10, 10), gradient)
        painter.restore()

        # 2. Black Hole Distortion (Applied to overlays)
        if loc_id == 6:
            warp_x = math.sin(self.time_counter * 2) * 8
            warp_y = math.cos(self.time_counter * 1.5) * 8
            painter.translate(warp_x, warp_y)
            painter.scale(1.0 + math.sin(self.time_counter) * 0.01, 1.0 + math.cos(self.time_counter) * 0.01)

        # 3. Atmospheric Particles
        painter.setPen(Qt.PenStyle.NoPen)
        for p in self.particles:
            p_color = QColor(255, 255, 255, p['alpha']) # Default white
            
            if loc_id == 1: p_color = QColor(150, 255, 150, p['alpha']) # Garden: Pollen/Leaves
            elif loc_id == 2: p_color = QColor(255, 200, 100, p['alpha'] // 2) # Shop: Warm Dust
            elif loc_id == 4: p_color = QColor(255, 100, 50, p['alpha']) # Mars: Red Sand
            elif loc_id == 5: p_color = QColor(200, 230, 255, p['alpha']) # Jupiter: Blue Sparks
            elif loc_id == 6: p_color = QColor(180, 100, 255, p['alpha']) # Void: Purple Essence
            
            painter.setBrush(p_color)
            painter.drawEllipse(p['pos'], p['size'], p['size'])

        # 4. Vignette Overlay (Gives depth and focuses center)
        vignette = QRadialGradient(self.width()//2, self.height()//2, self.width()//1.5)
        vignette.setColorAt(0, QColor(0, 0, 0, 0))
        vignette.setColorAt(1, QColor(0, 0, 0, 150))
        painter.fillRect(self.rect(), vignette)

        # 5. Stars (Static Overlays)
        if loc_id in [3, 6]:
            # Draw stars on Moon/Void
            painter.setPen(Qt.PenStyle.NoPen)
            random.seed(42)  # Fixed seed for consistent star positions
            for _ in range(50):
                x = random.randint(0, self.width())
                y = random.randint(0, self.height() // 2)
                brightness = random.randint(150, 255)
                size = random.randint(1, 3)
                # Twinkle effect
                twinkle = abs(math.sin(self.time_counter + x * 0.01)) * 100
                painter.setBrush(QColor(255, 255, 255, int(brightness * 0.5 + twinkle * 0.5)))
                painter.drawEllipse(x, y, size, size)
            random.seed()  # Reset seed
            return

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.quit()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
