import json
import os
import random
import math
import shapes

OUTPUT_DIR = "output"

# =============================================================================
# CONFIGURATION - Adjust these to change city generation
# =============================================================================
CONFIG = {
    "city_size": 80,           # Total city area
    "num_houses": 15,          # Small residential buildings
    "num_shops": 8,            # Commercial buildings
    "num_skyscrapers": 6,      # Tall office buildings
    "num_medium_buildings": 10,# Medium height (original style)
    "num_trees": 40,           # Trees in outskirts
    "num_streetlights": 25,    # Lamp posts
    "num_benches": 10,         # Park benches
    "num_humans": 20,          # Humanoid figures
    "num_crystals": 5,         # Decorative crystals
}

def save_mesh(mesh, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(mesh.to_dict(), f)
    print(f"Saved {filepath}")

def generate_world(config=None):
    if config is None:
        config = CONFIG
    
    world = shapes.Mesh()
    stats = {}
    
    # 1. Ground
    ground_size = 200
    ground = shapes.generate_box(ground_size, 1, ground_size, color=[0.08, 0.08, 0.12])
    world.add_mesh(ground, offset=[0, -0.5, 0])
    
    # 2. Roads (Grid pattern)
    print("Laying Roads...")
    road_positions = []
    for i in range(-3, 4):
        # Horizontal roads
        road = shapes.generate_road_segment(length=config["city_size"], width=6)
        world.add_mesh(road, offset=[0, 0, i * 12])
        road_positions.append(i * 12)
    
    # 3. SKYSCRAPERS (Downtown core)
    print("Building Skyscrapers...")
    stats["skyscrapers"] = 0
    for i in range(config["num_skyscrapers"]):
        gx = random.choice([-1, 0, 1]) * 12
        gz = random.choice([-1, 0, 1]) * 12
        x = gx + random.uniform(-3, 3)
        z = gz + random.uniform(-3, 3)
        
        if abs(x) < 6 and abs(z) < 6: continue
        
        floors = random.randint(15, 30)
        building = shapes.generate_skyscraper(floors=floors, seed=i)
        world.add_mesh(building, offset=[x, 0, z])
        stats["skyscrapers"] += 1
    
    # 4. MEDIUM BUILDINGS (Original style - surrounding downtown)
    print("Building Medium Buildings...")
    stats["medium_buildings"] = 0
    for i in range(config["num_medium_buildings"]):
        gx = random.randint(-3, 3) * 12
        gz = random.randint(-3, 3) * 12
        x = gx + random.uniform(-4, 4)
        z = gz + random.uniform(-4, 4)
        
        if abs(x) < 10 and abs(z) < 10: continue
        
        width = random.uniform(4, 8)
        depth = random.uniform(4, 8)
        height = random.uniform(10, 20)
        floors = int(height / 3) + 1
        
        building = shapes.generate_building(width, height, depth, floors)
        world.add_mesh(building, offset=[x, height/2, z])
        stats["medium_buildings"] += 1
    
    # 5. SHOPS (Commercial district edges)
    print("Building Shops...")
    stats["shops"] = 0
    for i in range(config["num_shops"]):
        x = random.uniform(-40, 40)
        z = random.choice([-36, -24, 24, 36]) + random.uniform(-2, 2)
        
        shop = shapes.generate_shop(width=random.uniform(6, 10), seed=i)
        world.add_mesh(shop, offset=[x, 0, z])
        stats["shops"] += 1
    
    # 6. HOUSES (Residential outskirts)
    print("Building Houses...")
    stats["houses"] = 0
    for i in range(config["num_houses"]):
        angle = random.uniform(0, math.pi * 2)
        dist = random.uniform(45, 70)
        x = math.cos(angle) * dist
        z = math.sin(angle) * dist
        
        floors = random.choice([1, 2, 2, 3])
        house = shapes.generate_house(floors=floors, seed=i)
        world.add_mesh(house, offset=[x, 0, z])
        stats["houses"] += 1
    
    # 7. STREETLIGHTS (Along roads)
    print("Placing Streetlights...")
    stats["streetlights"] = 0
    for i in range(config["num_streetlights"]):
        x = random.uniform(-40, 40)
        z = random.choice(road_positions) + random.choice([-4, 4])
        
        light = shapes.generate_streetlight(height=random.uniform(5, 7))
        world.add_mesh(light, offset=[x, 0, z])
        stats["streetlights"] += 1
    
    # 8. BENCHES (Near roads)
    print("Placing Benches...")
    stats["benches"] = 0
    for i in range(config["num_benches"]):
        x = random.uniform(-35, 35)
        z = random.choice(road_positions) + random.choice([-5, 5])
        
        bench = shapes.generate_bench()
        world.add_mesh(bench, offset=[x, 0, z])
        stats["benches"] += 1
    
    # 9. HUMANS (Walking around)
    print("Spawning Humans...")
    stats["humans"] = 0
    for i in range(config["num_humans"]):
        x = random.uniform(-50, 50)
        z = random.uniform(-50, 50)
        
        # Avoid spawning inside buildings (roughly)
        if abs(x) < 5 and abs(z) < 5: continue
        
        human = shapes.generate_humanoid(seed=i)
        world.add_mesh(human, offset=[x, 0, z])
        stats["humans"] += 1
    
    # 10. TREES (Parks and outskirts)
    print("Planting Trees...")
    stats["trees"] = 0
    for i in range(config["num_trees"]):
        angle = random.uniform(0, math.pi * 2)
        dist = random.uniform(50, 95)
        x = math.cos(angle) * dist
        z = math.sin(angle) * dist
        
        scale = random.uniform(0.6, 1.2)
        tree = shapes.generate_pro_tree(seed=i, levels=3)
        world.add_mesh(tree, offset=[x, 0, z], scale=scale)
        stats["trees"] += 1
    
    # 11. CRYSTALS (Decorative)
    print("Placing Crystals...")
    stats["crystals"] = 0
    for i in range(config["num_crystals"]):
        angle = random.uniform(0, math.pi * 2)
        dist = random.uniform(60, 90)
        x = math.cos(angle) * dist
        z = math.sin(angle) * dist
        
        scale = random.uniform(1.5, 3.0)
        crystal = shapes.generate_crystal_cluster(seed=i + 200)
        world.add_mesh(crystal, offset=[x, 0, z], scale=scale)
        stats["crystals"] += 1
    
    # Print stats
    print("\n--- CITY STATISTICS ---")
    total = 0
    for key, val in stats.items():
        print(f"  {key}: {val}")
        total += val
    print(f"  TOTAL OBJECTS: {total}")
    print(f"  VERTICES: {len(world.vertices)}")
    print(f"  TRIANGLES: {len(world.faces)}")
    
    return world

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("=" * 50)
    print("PROCEDURAL CITY GENERATOR")
    print("=" * 50)
    world = generate_world()
    save_mesh(world, "world.json")
    print("\n✓ Done! Open viewer to see your city.")

if __name__ == "__main__":
    main()
