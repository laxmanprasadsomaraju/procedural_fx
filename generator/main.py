import json
import os
import shapes

OUTPUT_DIR = "output"

def save_mesh(mesh, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(mesh.to_dict(), f) # Minified is fine
    print(f"Saved {filepath}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("Generating PRO assets...")
    
    # Generate Crystal
    print("Generating Crystal...")
    crystal = shapes.generate_crystal_cluster(seed=42)
    save_mesh(crystal, "crystal.json")
    
    # Generate Pro Tree
    print("Generating Tree...")
    tree = shapes.generate_pro_tree(seed=123)
    save_mesh(tree, "tree.json") # Overwrites old tree
    
    print("Done!")

if __name__ == "__main__":
    main()
