Overscoped Sandwich Sim — (A textbased Sandwich making simulator) Full Story with Time Progression and Failure Endings
You’re broke and dreaming of the only thing that matters: ATG 6, a game so powerful it costs 6 quintillion dollars. But instead of mining crypto or robbing banks, you stare at a half-eaten sandwich and decide… it’s sandwich time.

Location 1: Your Front Garden
Rank: Beginner Chef
New Ingredient: Fresh Tomatoes
Days Until Move: 7 Days

Story:
You begin your empire in your garden, where you craft simple tomato sandwiches that win over neighbors and random dogs. Day after day, profits climb.

On Day 7, the government arrives, declaring your operation illegal for “health and zoning violations.”

Success: You sell your house and, on Day 8, move into a small commercial shop.
Failure (Before Day 7): You fail to earn enough customers before inspectors arrive, get fined into oblivion, and your grill is seized.
Game Over: “You couldn’t ketchup to demand.”

Location 2: Small Sandwich Shop
Rank: Amateur Entrepreneur
New Ingredient: Premium Ham
Days Until Move: 12 Days

Story:
You reopen as a proud shop owner. Premium ham becomes your signature upgrade, and soon locals line up around the block.

By Day 10, you’re a local legend — but on Day 12, the Global Sandwich Ban lands. All sandwiches are declared “economically destabilizing products.”

Success: You build a secret rocket from stale bread and launch on Day 13.
Failure: You try to hide your shop but get caught selling black-market ham. Sentenced to “Eternal Sandwich Duty.”
Game Over: “You’ve been ham-handled by justice.”

Location 3: The Moon Base
Rank: Space Chef
New Ingredient: Cosmic Cheese
Days Until Move: 15 Days

Story:
By Day 3 on the Moon, business explodes. Tourists love your low-gravity sandwiches that bounce when dropped. Cosmic Cheese increases price and flavor 300%.

But on Day 15, the Lunar Authority demands your shutdown for “distorting gravitational taste properties.”

Success: Escape on Day 16 with your rocket in one piece.
Failure: Stay too long collecting more cheese and your base collapses from tidal forces.
Game Over: “Moon Melt: The sandwich was too strong.”

Location 4: Mars Diner
Rank: Interplanetary Sandwich Tycoon
New Ingredient: Martian Pepper
Days Until Move: 20 Days

Story:
Your diner thrives under crimson skies. Martian Pepper adds explosive spiciness that turns your sandwiches into interplanetary hits.

Around Day 18, customers form long queues stretching across craters. But on Day 20, chaos — a flavor riot breaks out. The Martian Senate blames you.

Success: You flee by Day 21, boosting your rocket toward Jupiter.
Failure: You stay to reason with rioters but get crowned “King of Spicy Bread” and can never leave.
Game Over: “Absorbed into the Martian cult of flavor.”

Location 5: Jupiter Floating Bar
Rank: Gas Giant Gourmet
New Ingredient: Storm Pickles
Days Until Move: 25 Days

Story:
Now surrounded by storms, your floating bar becomes a cosmic hotspot. Storm Pickles, electrified by Jupiter’s lightning, make your sandwiches literally crackle with flavor.

By Day 22, profits surge. On Day 25, gravity pressure starts crushing your shop like a soda can.

Success: You warp out of Jupiter’s skies by Day 26.
Failure: You try to tough it out but the bar implodes in a flash.
Game Over: “You became static in the sandwich industry.”

Location 6: Ton-216 — The Black Hole
Rank: Galactic Master Chef
New Ingredient: Black Magic Ingredients
Days Until Move: Final Stage (∞ Days)

Story:
At the edge of existence, you use raw void matter to craft the galaxy’s ultimate sandwiches. Each sale earns billions, bending physics and hunger alike.

By Day 40, you make your fortune — 6 quintillion dollars, enough for ATG 6. But your excitement fades instantly when the news hits:
“Chockster Gumes goes bankrupt. ATG 6 canceled indefinitely.”

You stare into Ton-216’s darkness, feeling yourself unravel.

Success (Story Ending): You jump into the black hole. The screen fades to white:
“The Universe Tasted Well.”
Failure: If you run out of ingredients before hitting 6 quintillion, the black hole consumes your store.
Game Over: “Lost to flavor singularity.”

---

## 🛠 Development To-Do List

### 1. Core Gameplay Engine
- [x] Day/Time System
- [x] Economy 2.0
- [x] Ingredient Stacking
- [x] Visual Stack Renderer
- [x] Narrative Engine: System to display story snippets and event text in a log.
- [x] Customer AI: Simple "Order" generator that requests specific ingredient combinations.
- [x] Rank Logic: Map money/reputation milestones to the ranks (Beginner -> Galactic Master).

### 2. Location & Progression System
- [x] State Controller: Manage the transition between the 6 distinct locations.
- [x] Save/Load Extension: Ensure `save_data.json` tracks the current Location ID and unlocked ingredients.
- [x] Narrative Overlays: Display the "Success/Failure" story text when moving locations.

### 3. Location-Specific Mechanics
- [x] Location 1 (Garden): Intro tutorial & "Health & Zoning" Game Over.
- [x] Location 2 (Shop): Unlock "Premium Ham" & "Global Sandwich Ban" transition.
- [x] Location 3 (Moon): Low-Gravity Physics & Unlock "Cosmic Cheese".
- [x] Location 4 (Mars): Spiciness Meter.
- [x] Location 5 (Jupiter): Crackle Effect & Screen shake effects.
- [x] Location 6 (Black Hole): Void matter visual effects & Final boss-tier customers.

### 4. UI & Visuals
- [x] Dynamic Backgrounds: Change the `MainWindow` paint logic based on the current location.
- [x] Environment Painter: Add unique assets/drawing logic for each planet's sky and ground.
- [x] Ending Sequences: "Bankruptcy" news flash & "Fading to White" final win sequence.

### 5. Audio Integration
- [x] **Dynamic Music**: Slower tracks for Earth, lo-fi for Moon, and chaotic synths for Jupiter/Black Hole.
- [x] **Juicy SFX**: Distinct sounds for different ingredients (e.g., a squish for tomatoes, a metallic clang for cosmic cheese).

### 6. Balancing & Economy Tuning
- [x] **Difficulty Tweak**: Ensure "Over-Scoped" difficulty actually makes ingredient management stressful.
- [x] Inflation Logic: Scale prices exponentially so reaching 6 quintillion is actually possible by Day 40.
- [x] **Operational Overheads**: Implement daily rent and utility costs (Oxygen tax on Moon, cooling costs on Mars) that scale per location to prevent profit stagnation.
- [x] **Reputation Multiplier**: Perfect orders increase a "Hype" meter, which multiplies tip percentage but increases customer arrival speed.
- [x] **Dynamic Market**: Randomized daily events (e.g., "Tomato Blight" or "Ham Export Ban") that fluctuate ingredient costs by 50-200%.
- [x] **Waste Penalty**: Implement a "Bio-Waste" fee for clearing a sandwich or letting an order expire, discouraging spam-clicking.
- [x] **Customer Feedback**: Random text snippets from customers (e.g., "Best sandwich ever!" or "Where's the ham?") influencing reputation.
- [x] **Daily Briefing**: A text summary at the start of each day, detailing market conditions, upcoming challenges, or local news.
- [x] **Galactic Loans**: Allow players to borrow money to hit location requirements, but with a daily interest rate that makes the next location harder to sustain.
- [x] **Branching Narrative Events**: Morning briefings that occasionally present a choice (e.g., "A critic visits: Give a free sandwich for a PR boost, or charge double?").

### 7. Advanced Gameplay Features
- [x] **Upgrade Shop**: A shop between locations to buy permanent buffs (e.g., "Heat Sink" for Mars, "Gravity Boots" for Moon stability).
- [x] **Secret Recipes**: Implement a combo system where specific (unlisted) ingredient stacks grant massive "Legendary Sandwich" bonuses.
- [x] **Flavor Text Engine**: Automatically generate descriptive names for sandwiches based on ingredients (e.g., "The Soggy Moon-Melt" or "A Spiced Martian Behemoth").
- [x] **Customer Patience**: Add a timer to orders; failure to serve in time results in a refund and reputation hit.
- [x] **Achievement Milestones**: Permanent stat boosts for reaching specific goals (e.g., "Sold 1,000 Tomatoes").
- [x] **Environmental Hazards**: UI-affecting events (e.g., Solar Flares blurring the screen on the Moon, or Sandstorms hiding ingredients on Mars).
- [x] **End-of-Day Analytics**: A summary screen showing gross profit, expenses (rent/waste), and customer satisfaction trends.

### 8. Endgame & Replayability
- [x] **Endless Mode**: Detect a "Game Completed" flag in `save_data.json` to unlock a new "Infinite Void" button on the Main Menu wich is an endless mode that plays in the black hole.
- [x] **Lore Log**: A text-based collection of all encountered customer feedback and story snippets to track the history of your empire. 
- [x] **Colectables:** A historry of every sandwich you ever made with names. Also another tab with items you can colect trough the storry. (Colectables are for all saves the same so if colected ones you cant colect it a second time.)