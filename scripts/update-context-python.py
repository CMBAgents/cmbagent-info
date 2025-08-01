#!/usr/bin/env python3
import json
import os
import glob

def update_libraries_with_context_status(domain):
    """Update context status for a specific domain"""
    try:
        # Paths
        json_path = f'app/data/{domain}-libraries.json'
        context_dir = f'public/context/{domain}'
        
        if not os.path.exists(json_path):
            print(f"JSON file not found for domain: {domain}")
            return
        
        # Read the JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Get existing context files
        context_files = []
        if os.path.exists(context_dir):
            for file in os.listdir(context_dir):
                if file.endswith('.txt'):
                    context_files.append(file)
        
        print(f"Found {len(context_files)} context files for {domain}: {context_files}")
        
        # Update each library entry
        for library in json_data['libraries']:
            # Try different naming patterns
            package_name = library['name'].split('/')[-1]  # Get the package name
            patterns = [
                f"{package_name}-context.txt",
                f"{package_name}.txt",
                f"{library['name'].replace('/', '-').replace('.', '-')}-context.txt",
                f"{package_name.replace('.', '-')}-context.txt",
                # Handle cases like "python-skyfield" -> "skyfield-context.txt"
                f"{package_name.split('-')[-1]}-context.txt",
                # Handle cases like "python-skyfield" -> "skyfield.txt"
                f"{package_name.split('-')[-1]}.txt"
            ]
            
            has_context_file = False
            context_file_name = ''
            
            for pattern in patterns:
                if pattern in context_files:
                    context_file_name = pattern
                    has_context_file = True
                    break
            
            # Update the library entry
            library['hasContextFile'] = has_context_file
            if has_context_file:
                library['contextFileName'] = context_file_name
                print(f"✓ {library['name']} has context file: {context_file_name}")
            else:
                if 'contextFileName' in library:
                    del library['contextFileName']
                print(f"✗ {library['name']} has no context file")
        
        # Write back to the JSON file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nUpdated context status for {domain}: {len(json_data['libraries'])} libraries processed\n")
        
        return json_data
        
    except Exception as error:
        print(f"Error updating context status for domain {domain}: {error}")
        return None

def update_all_libraries_with_context_status():
    """Update context status for all domains"""
    domains = ['astronomy', 'finance']
    print('🔄 Updating context status for all domains...\n')
    
    for domain in domains:
        print(f"📁 Processing {domain} domain:")
        update_libraries_with_context_status(domain)
    
    print('✅ Context status update completed!')

if __name__ == "__main__":
    update_all_libraries_with_context_status() 