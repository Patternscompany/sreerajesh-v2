
import os
import shutil
import urllib.parse

# Dictionary mapping original filename (without path) to new compact filename (without path)
# Only including files where replacement is beneficial (size reduction)
# I'm going to map ALL potential large files.
mapping = {
    'Double Ka Meeta.png': 'DoubleKaMeet.jpeg',
    'Paneer Tikka.png': 'PaneerTikk.jpeg',
    'Premium Veg Thali.png': 'PremiumVegThal.jpeg',
    'Qubani Ka Meetha.png': 'QubaniKaMeeth.jpeg',
    'South Indian Breakfast Platter.png': 'SouthIndianBreakfastPlatte.jpeg',
    'Tandoori Chicken.png': 'TandooriChicke.jpeg',
    'Traditional Mutton Biryani.png': 'TraditionalMuttonBiryan.jpeg',
    'Vegetable Manchuria.png': 'VegetableManchuri.jpeg',
    'abouttestimonials.png': 'abouttestimonial.jpeg',
    'contactpic.png': 'contactpi.jpeg',
    'herobackground.png': 'herobackgroun.jpeg',
    'homeabout.png': 'homeabou.jpeg',
    'marriage.png': 'marriage.jpeg', # Checking if this exists in newcom or if I should look for a match
    'Hyderabadi Breakfast Special.png': 'HyderabadiBreakfastSpecial.jpeg', # Check if exists
    'Chicken 65 Special.png': 'Chicken65Special.jpeg', # Check if exists
}

# The user said "pics should be match". 
# Let's list newcom files to be sure about names before running.
# Wait, I'm writing the script now. I can add dynamic matching in the script.

base_dir = '/Users/apple/Downloads/new sree rajesh/sreerajesh-v2'
rajeshimedia_dir = os.path.join(base_dir, 'rajeshimedia')
newcom_dir = os.path.join(rajeshimedia_dir, 'newcom')

# Extensions to check for references
search_extensions = ['.html', '.css', '.js']

def replace_references(old_name, new_name):
    print(f"Updating references for {old_name} -> {new_name}")
    
    # Generate URL encoded versions
    old_name_encoded = urllib.parse.quote(old_name)
    new_name_encoded = urllib.parse.quote(new_name)
    
    replacements = [
        (old_name, new_name),
        (old_name_encoded, new_name_encoded)
    ]
    
    for root, dirs, files in os.walk(base_dir):
        if 'rajeshimedia' in root: 
            continue
            
        for file in files:
            if any(file.endswith(ext) for ext in search_extensions):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    modified = False
                    for old, new in replacements:
                        if old in new_content:
                            print(f"  Found '{old}' in {file}")
                            new_content = new_content.replace(old, new)
                            modified = True
                            
                    if modified:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                            print(f"  Updated {file}")
                            
                except Exception as e:
                    print(f"  Error reading/writing {file}: {e}")

def find_best_match(filename, newcom_files):
    # Strip extension and try to match
    base = os.path.splitext(filename)[0]
    # Remove spaces and common separators for loose matching
    clean_base = base.replace(' ', '').lower()
    
    for nf in newcom_files:
        nf_base = os.path.splitext(nf)[0]
        clean_nf = nf_base.replace(' ', '').lower()
        
        # Exact match of base name (ignoring case/spaces)
        if clean_base == clean_nf:
            return nf
            
        # Specific manual overrides if names are truncated
        if base == "Double Ka Meeta" and "DoubleKaMeet" in nf: return nf
        if base == "Paneer Tikka" and "PaneerTikk" in nf: return nf
        if base == "Premium Veg Thali" and "PremiumVegThal" in nf: return nf
        if base == "Qubani Ka Meetha" and "QubaniKaMeeth" in nf: return nf
        if base == "South Indian Breakfast Platter" and "SouthIndianBreakfastPlatte" in nf: return nf
        if base == "Tandoori Chicken" and "TandooriChicke" in nf: return nf
        if base == "Traditional Mutton Biryani" and "TraditionalMuttonBiryan" in nf: return nf
        if base == "Vegetable Manchuria" and "VegetableManchuri" in nf: return nf
        if base == "abouttestimonials" and "abouttestimonial" in nf: return nf
        if base == "contactpic" and "contactpi" in nf: return nf
        if base == "herobackground" and "herobackgroun" in nf: return nf
        if base == "homeabout" and "homeabou" in nf: return nf
        if base == "nonvegbrand" and "nonvegbran" in nf: return nf
        if base == "logo" and "log" in nf: return nf

    return None

def process_images():
    print("Starting image replacement...")
    
    # Get all files in rajeshimedia (large files)
    large_files = [f for f in os.listdir(rajeshimedia_dir) if os.path.isfile(os.path.join(rajeshimedia_dir, f))]
    # Get all files in newcom
    if not os.path.exists(newcom_dir):
        print("newcom directory not found!")
        return
    newcom_files = [f for f in os.listdir(newcom_dir) if os.path.isfile(os.path.join(newcom_dir, f))]

    for old_file in large_files:
        # Ignore non-image files if needed, but let's check size first
        old_path = os.path.join(rajeshimedia_dir, old_file)
        old_size = os.path.getsize(old_path)
        
        # Skip small files (e.g. < 500KB) unless explicitly targeted? 
        # Actually user said "replace pics which are in large side".
        if old_size < 500 * 1024:
            continue

        match = find_best_match(old_file, newcom_files)
        
        if match:
            new_compact_path = os.path.join(newcom_dir, match)
            # Create new filename in rajeshimedia: same base name as OLD file, but extension of NEW file
            # Wait, user said "replace pics...". Usually we want to keep the same extension if possible to avoid breaking code, 
            # BUT the user specifically said "pics in newcom are jpg or jpeg". 
            # So code MUST be updated.
            
            # Strategy:
            # 1. Copy NEW file to rajeshimedia with NEW extension (e.g. .jpeg)
            # 2. Update code to point to NEW extension
            # 3. Delete OLD file (.png)
            
            # We will rename the file to have the same basename as the old file IF clearer, 
            # but the user said "replace pics". Let's stick to the OLD filename BASE for clarity in code, 
            # but change extension.
            
            old_base = os.path.splitext(old_file)[0]
            new_ext = os.path.splitext(match)[1]
            final_name = old_base + new_ext # e.g. "Double Ka Meeta.jpeg"
            
            dest_path = os.path.join(rajeshimedia_dir, final_name)
            
            print(f"Processing {old_file} ({old_size/1024/1024:.2f} MB)...")
            print(f"  Found match: {match}")
            
            # Check size benefit
            new_size = os.path.getsize(new_compact_path)
            if new_size < old_size:
                print(f"  Replacing... (New size: {new_size/1024/1024:.2f} MB)")
                try:
                    shutil.copy2(new_compact_path, dest_path)
                    
                    # Update references
                    # Note: We need to replace the FULL old filename (including extension) with the FULL new filename
                    replace_references(old_file, final_name)
                    
                    # Delete old file
                    if old_file != final_name: # Prevent deleting if name/ext is same (unlikely here)
                        os.remove(old_path)
                        print(f"  Deleted old file {old_file}")
                    
                except Exception as e:
                    print(f"  Failed to replace {old_file}: {e}")
            else:
                print(f"  Skipping: New file is larger ({new_size} > {old_size})")
        else:
            if old_size > 1024 * 1024: # Only warn about unmatched large files > 1MB
                print(f"No match found for large file: {old_file}")

if __name__ == "__main__":
    process_images()
