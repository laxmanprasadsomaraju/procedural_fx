import math
import random

class Mesh:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.colors = [] # RGB per vertex
    
    def to_dict(self):
        return {
            "vertices": self.vertices,
            "faces": self.faces,
            "colors": self.colors
        }
    
    def add_mesh(self, other_mesh, offset=[0,0,0], scale=1.0, color_override=None):
        start_idx = len(self.vertices)
        for v in other_mesh.vertices:
            self.vertices.append([
                v[0]*scale + offset[0],
                v[1]*scale + offset[1],
                v[2]*scale + offset[2]
            ])
            
        for c in other_mesh.colors:
            if color_override:
                self.colors.append(color_override)
            else:
                self.colors.append(c)
        
        # If other mesh uses faces, shift indices
        for f in other_mesh.faces:
            self.faces.append([x + start_idx for x in f])

def generate_box(width=1, height=1, depth=1, color=[1,1,1]):
    mesh = Mesh()
    w, h, d = width/2, height/2, depth/2
    
    # 8 vertices
    mesh.vertices = [
        [-w, -h, -d], [w, -h, -d], [w, h, -d], [-w, h, -d],
        [-w, -h, d], [w, -h, d], [w, h, d], [-w, h, d]
    ]
    
    for _ in range(8):
        mesh.colors.append(color)
        
    # 12 triangles (6 quads)
    faces = [
        [4, 5, 6], [4, 6, 7], # Front
        [1, 0, 3], [1, 3, 2], # Back
        [3, 2, 6], [3, 6, 7], # Top
        [4, 5, 1], [4, 1, 0], # Bottom
        [1, 5, 6], [1, 6, 2], # Right
        [4, 0, 3], [4, 3, 7]  # Left
    ]
    mesh.faces.extend(faces)
    return mesh

def generate_crystal_cluster(seed=None):
    if seed: random.seed(seed)
    mesh = Mesh()
    
    num_crystals = random.randint(5, 12)
    base_color = [0.2, 0.8, 1.0] # Cyan
    
    for _ in range(num_crystals):
        # Randomize crystal shape
        height = random.uniform(1.5, 4.0)
        width = random.uniform(0.3, 0.8)
        
        # Create a simple "shard" - represented as a tapered hexagon
        shard = Mesh()
        segments = 6
        
        # Base ring
        for i in range(segments):
            angle = (i/segments)*math.pi*2
            shard.vertices.append([math.cos(angle)*width, 0, math.sin(angle)*width])
            shard.colors.append(base_color)
            
        # Tip point
        shard.vertices.append([0, height, 0])
        shard.colors.append([1, 1, 1]) # White tip
        
        tip_idx = segments
        
        # Faces connecting base to tip
        for i in range(segments):
            next_i = (i+1)%segments
            shard.faces.append([i, next_i, tip_idx])
            
        # Faces closing bottom (fan)
        # Center bottom point could be added but let's just fan it
        shard.vertices.append([0, 0, 0]) # Bottom center
        shard.colors.append(base_color)
        bot_idx = segments + 1
        for i in range(segments):
            next_i = (i+1)%segments
            shard.faces.append([next_i, i, bot_idx]) # Winding order flipped for bottom
            
        # Add to cluster with random rotation/offset
        import math as m
        # Random rotation logic would require matrix math, let's keep it simple: 
        # Just offset and tilt by manually perturbing vertices
        
        tilt_x = random.uniform(-0.5, 0.5)
        tilt_z = random.uniform(-0.5, 0.5)
        
        transformed_shard = Mesh()
        transformed_shard.colors = shard.colors
        transformed_shard.faces = shard.faces
        
        for v in shard.vertices:
            # Apply tilt (shear)
            y = v[1]
            tx = v[0] + y * tilt_x
            tz = v[2] + y * tilt_z
            transformed_shard.vertices.append([tx, y, tz])
            
        mesh.add_mesh(transformed_shard, offset=[random.uniform(-0.5, 0.5), 0, random.uniform(-0.5, 0.5)])
        
    return mesh

def generate_pro_tree(seed=None, levels=3):
    if seed: random.seed(seed)
    mesh = Mesh()
    
    # Recursive function
    def branch(position, direction, length, radius, level):
        if level <= 0:
            # Add leaves at tips
            leaves = generate_box(length, length, length, color=[1.0, 0.2, 0.5]) # Pink Sakura Leaves
            mesh.add_mesh(leaves, offset=position)
            return

        # Cylinder-like segment logic (simplified to a box for robustness without full rotation matrices)
        # Using a box as a branch segment
        stick = generate_box(radius*2, length, radius*2, color=[0.4, 0.2, 0.1])
        
        # Calc end position
        end_pos = [
            position[0] + direction[0]*length,
            position[1] + direction[1]*length,
            position[2] + direction[2]*length
        ]
        
        # Approximation: Simply placing the box at the midpoint
        mid_pos = [
            position[0] + direction[0]*length*0.5,
            position[1] + direction[1]*length*0.5,
            position[2] + direction[2]*length*0.5
        ]
        
        mesh.add_mesh(stick, offset=mid_pos)
        
        # Split into 2 branches
        num_branches = 2
        for i in range(num_branches):
            # Spread direction slightly
            spread = 0.5
            new_dir = [
                direction[0] + random.uniform(-spread, spread),
                direction[1] + random.uniform(0, spread), # Tend upwards
                direction[2] + random.uniform(-spread, spread)
            ]
            # Normalize
            mag = math.sqrt(sum([x*x for x in new_dir]))
            new_dir = [x/mag for x in new_dir]
            
            branch(end_pos, new_dir, length*0.7, radius*0.7, level-1)

    # Start recursion
    branch([0,0,0], [0,1,0], 3.0, 0.4, 4)
    
    return mesh

def generate_building(width=1, height=1, depth=1, floors=5):
    mesh = Mesh()
    
    # Main building body
    body = generate_box(width, height, depth, color=[0.2, 0.2, 0.25])
    mesh.add_mesh(body)
    
    # Windows (Emissive-looking via vertex color, we'll need bloom for effect)
    window_color = [1.0, 0.9, 0.4] # Warm light
    window_off = [0.1, 0.1, 0.1]
    
    # Simple grid of windows on faces
    # We'll just add small thin plates on the surface for windows to keep it simple geometry-wise
    
    w, h, d = width/2, height/2, depth/2
    
    # Front/Back windows
    rows = floors
    cols = max(2, int(width * 2))
    
    window_size_w = (width / cols) * 0.6
    window_size_h = (height / rows) * 0.6
    
    for r in range(rows):
        y = -h + (height/rows) * (r + 0.5)
        for c in range(cols):
            x = -w + (width/cols) * (c + 0.5)
            
            is_on = random.random() > 0.3
            color = window_color if is_on else window_off
            
            # Front
            win = generate_box(window_size_w, window_size_h, 0.05, color=color)
            mesh.add_mesh(win, offset=[x, y, d + 0.02])
            
            # Back
            win_back = generate_box(window_size_w, window_size_h, 0.05, color=color)
            mesh.add_mesh(win_back, offset=[-x, y, -d - 0.02])
            
    # Left/Right windows
    cols_side = max(2, int(depth * 2))
    window_size_d = (depth / cols_side) * 0.6
    
    for r in range(rows):
        y = -h + (height/rows) * (r + 0.5)
        for c in range(cols_side):
            z = -d + (depth/cols_side) * (c + 0.5)
            
            is_on = random.random() > 0.3
            color = window_color if is_on else window_off
            
            # Right
            win_r = generate_box(0.05, window_size_h, window_size_d, color=color)
            mesh.add_mesh(win_r, offset=[w + 0.02, y, z])
            
            # Left
            win_l = generate_box(0.05, window_size_h, window_size_d, color=color)
            mesh.add_mesh(win_l, offset=[-w - 0.02, y, -z])

    return mesh

# =============================================================================
# BUILDING VARIETY
# =============================================================================

def generate_house(floors=2, seed=None):
    """Small residential house with pitched roof"""
    if seed: random.seed(seed)
    mesh = Mesh()
    
    width = random.uniform(4, 6)
    depth = random.uniform(4, 6)
    floor_height = 3
    height = floors * floor_height
    
    # Wall color - warm tones
    wall_colors = [
        [0.8, 0.7, 0.6],  # Beige
        [0.6, 0.5, 0.4],  # Brown
        [0.7, 0.75, 0.8], # Light gray-blue
        [0.9, 0.85, 0.75] # Cream
    ]
    wall_color = random.choice(wall_colors)
    
    # Main body
    body = generate_box(width, height, depth, color=wall_color)
    mesh.add_mesh(body, offset=[0, height/2, 0])
    
    # Pitched roof (simplified as a box for now)
    roof_height = 2
    roof_color = [0.4, 0.2, 0.15]  # Dark brown
    roof = generate_box(width + 0.5, roof_height, depth + 0.5, color=roof_color)
    mesh.add_mesh(roof, offset=[0, height + roof_height/2, 0])
    
    # Door
    door_color = [0.3, 0.2, 0.1]
    door = generate_box(1, 2.5, 0.1, color=door_color)
    mesh.add_mesh(door, offset=[0, 1.25, depth/2 + 0.05])
    
    # Windows
    window_color = [0.6, 0.8, 1.0]  # Light blue glass
    for f in range(floors):
        y = f * floor_height + floor_height/2 + 0.5
        # Front windows
        win1 = generate_box(1, 1.2, 0.05, color=window_color)
        mesh.add_mesh(win1, offset=[-width/4, y, depth/2 + 0.05])
        win2 = generate_box(1, 1.2, 0.05, color=window_color)
        mesh.add_mesh(win2, offset=[width/4, y, depth/2 + 0.05])
    
    return mesh

def generate_shop(width=8, seed=None):
    """Wide 1-floor commercial building with storefront"""
    if seed: random.seed(seed)
    mesh = Mesh()
    
    depth = random.uniform(6, 10)
    height = 4
    
    # Wall colors - commercial
    wall_color = [0.85, 0.85, 0.8]  # Off-white
    
    # Main body
    body = generate_box(width, height, depth, color=wall_color)
    mesh.add_mesh(body, offset=[0, height/2, 0])
    
    # Large storefront window
    glass_color = [0.4, 0.6, 0.8]
    storefront = generate_box(width * 0.7, height * 0.6, 0.05, color=glass_color)
    mesh.add_mesh(storefront, offset=[0, height * 0.4, depth/2 + 0.05])
    
    # Awning
    awning_colors = [
        [1.0, 0.3, 0.3],  # Red
        [0.3, 0.6, 1.0],  # Blue
        [0.3, 0.8, 0.3],  # Green
        [1.0, 0.8, 0.2]   # Yellow
    ]
    awning_color = random.choice(awning_colors)
    awning = generate_box(width * 0.8, 0.3, 1.5, color=awning_color)
    mesh.add_mesh(awning, offset=[0, height * 0.75, depth/2 + 0.75])
    
    # Sign
    sign_color = [1.0, 1.0, 0.8]  # Bright for bloom
    sign = generate_box(width * 0.5, 0.8, 0.1, color=sign_color)
    mesh.add_mesh(sign, offset=[0, height - 0.5, depth/2 + 0.1])
    
    return mesh

def generate_skyscraper(floors=20, seed=None):
    """Tall modern skyscraper with glass facade"""
    if seed: random.seed(seed)
    mesh = Mesh()
    
    width = random.uniform(8, 15)
    depth = random.uniform(8, 15)
    floor_height = 3.5
    height = floors * floor_height
    
    # Glass facade color
    glass_color = [0.3, 0.4, 0.5]
    
    # Main tower
    body = generate_box(width, height, depth, color=glass_color)
    mesh.add_mesh(body, offset=[0, height/2, 0])
    
    # Window grid (emissive)
    window_on = [1.0, 0.95, 0.7]
    window_off = [0.1, 0.12, 0.15]
    
    rows = min(floors, 25)  # Cap for performance
    cols = max(3, int(width / 2))
    
    w, h, d = width/2, height/2, depth/2
    win_w = (width / cols) * 0.6
    win_h = (height / rows) * 0.5
    
    for r in range(rows):
        y = -h + (height/rows) * (r + 0.5)
        for c in range(cols):
            x = -w + (width/cols) * (c + 0.5)
            is_on = random.random() > 0.4
            color = window_on if is_on else window_off
            
            win = generate_box(win_w, win_h, 0.05, color=color)
            mesh.add_mesh(win, offset=[x, y + height/2, d + 0.02])
    
    # Rooftop antenna
    antenna_color = [0.5, 0.5, 0.5]
    antenna = generate_box(0.5, 8, 0.5, color=antenna_color)
    mesh.add_mesh(antenna, offset=[0, height + 4, 0])
    
    # Red light on top
    light_color = [1.0, 0.2, 0.2]
    light = generate_box(0.8, 0.8, 0.8, color=light_color)
    mesh.add_mesh(light, offset=[0, height + 8, 0])
    
    return mesh

# =============================================================================
# ENVIRONMENT OBJECTS
# =============================================================================

def generate_streetlight(height=6):
    """Street lamp with glowing bulb"""
    mesh = Mesh()
    
    pole_color = [0.3, 0.3, 0.35]
    
    # Pole
    pole = generate_box(0.3, height, 0.3, color=pole_color)
    mesh.add_mesh(pole, offset=[0, height/2, 0])
    
    # Arm
    arm = generate_box(1.5, 0.2, 0.2, color=pole_color)
    mesh.add_mesh(arm, offset=[0.75, height - 0.3, 0])
    
    # Light bulb (emissive)
    bulb_color = [1.0, 0.95, 0.7]
    bulb = generate_box(0.6, 0.4, 0.6, color=bulb_color)
    mesh.add_mesh(bulb, offset=[1.5, height - 0.5, 0])
    
    return mesh

def generate_bench():
    """Park bench"""
    mesh = Mesh()
    
    wood_color = [0.5, 0.35, 0.2]
    metal_color = [0.25, 0.25, 0.3]
    
    # Seat
    seat = generate_box(2, 0.15, 0.6, color=wood_color)
    mesh.add_mesh(seat, offset=[0, 0.5, 0])
    
    # Back
    back = generate_box(2, 0.6, 0.1, color=wood_color)
    mesh.add_mesh(back, offset=[0, 0.9, -0.25])
    
    # Legs
    for x in [-0.8, 0.8]:
        leg = generate_box(0.1, 0.5, 0.5, color=metal_color)
        mesh.add_mesh(leg, offset=[x, 0.25, 0])
    
    return mesh

def generate_road_segment(length=10, width=8):
    """Road segment with lane markings"""
    mesh = Mesh()
    
    # Asphalt
    road_color = [0.15, 0.15, 0.18]
    road = generate_box(width, 0.1, length, color=road_color)
    mesh.add_mesh(road, offset=[0, 0.05, 0])
    
    # Center line (yellow)
    line_color = [0.9, 0.8, 0.2]
    for i in range(int(length / 2)):
        z = -length/2 + i * 2 + 0.5
        line = generate_box(0.15, 0.02, 0.8, color=line_color)
        mesh.add_mesh(line, offset=[0, 0.11, z])
    
    return mesh

# =============================================================================
# HUMANOID FIGURES
# =============================================================================

def generate_humanoid(seed=None):
    """Simple capsule-based human figure"""
    if seed: random.seed(seed)
    mesh = Mesh()
    
    # Random clothing colors
    shirt_colors = [
        [0.8, 0.2, 0.2],  # Red
        [0.2, 0.5, 0.8],  # Blue
        [0.2, 0.7, 0.3],  # Green
        [0.9, 0.9, 0.2],  # Yellow
        [0.6, 0.3, 0.7],  # Purple
        [0.1, 0.1, 0.1],  # Black
        [0.95, 0.95, 0.95] # White
    ]
    pants_colors = [
        [0.2, 0.2, 0.3],  # Dark blue
        [0.1, 0.1, 0.1],  # Black
        [0.4, 0.35, 0.3], # Khaki
        [0.3, 0.3, 0.35]  # Gray
    ]
    skin_color = [0.9, 0.75, 0.65]
    
    shirt_color = random.choice(shirt_colors)
    pants_color = random.choice(pants_colors)
    
    # Head
    head = generate_box(0.4, 0.45, 0.35, color=skin_color)
    mesh.add_mesh(head, offset=[0, 1.65, 0])
    
    # Torso
    torso = generate_box(0.6, 0.7, 0.35, color=shirt_color)
    mesh.add_mesh(torso, offset=[0, 1.15, 0])
    
    # Arms
    for side in [-1, 1]:
        arm = generate_box(0.2, 0.6, 0.2, color=shirt_color)
        mesh.add_mesh(arm, offset=[side * 0.4, 1.1, 0])
        # Hand
        hand = generate_box(0.15, 0.2, 0.15, color=skin_color)
        mesh.add_mesh(hand, offset=[side * 0.4, 0.7, 0])
    
    # Legs
    for side in [-1, 1]:
        leg = generate_box(0.25, 0.8, 0.25, color=pants_color)
        mesh.add_mesh(leg, offset=[side * 0.18, 0.4, 0])
    
    # Feet/Shoes
    shoe_color = [0.15, 0.1, 0.1]
    for side in [-1, 1]:
        shoe = generate_box(0.25, 0.15, 0.35, color=shoe_color)
        mesh.add_mesh(shoe, offset=[side * 0.18, 0.075, 0.05])
    
    return mesh

