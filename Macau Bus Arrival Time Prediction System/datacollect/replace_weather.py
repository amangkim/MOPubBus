import pandas as pd
import os
import glob

def map_weather_conditions(input_folder):
    """
    Batch map the weather column of all CSV files in a folder, directly overwrite the original files
    
    Parameters:
    input_folder: Input folder path
    """
    
    # Read mapping relationship
    try:
        mapping_df = pd.read_csv('D:/School/MPU_Master/BusData/2025busdata/weather_types.csv')
        # Create mapping dictionary
        weather_mapping = dict(zip(mapping_df['weather conditions'], mapping_df['numerical value']))
        print("Successfully read weather type mapping:")
        for condition, value in weather_mapping.items():
            print(f"  {condition} -> {value}")
    except FileNotFoundError:
        print("Error: Could not find weather_types.csv file")
        return
    except Exception as e:
        print(f"Error reading mapping file: {e}")
        return
    
    # Get all CSV files
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))
    
    # Filter out the mapping file itself
    csv_files = [f for f in csv_files if not f.endswith('weather_types.csv')]
    
    if not csv_files:
        print(f"No CSV files found in folder {input_folder}")
        return
    
    print(f"\nFound {len(csv_files)} CSV files to process")
    print("Note: Original files will be overwritten directly!")
    
    processed_count = 0
    error_files = []
    
    for file_path in csv_files:
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Check if weather column exists
            if 'weather' not in df.columns:
                print(f"Warning: File {os.path.basename(file_path)} does not have a 'weather' column, skipping")
                continue
            
            # Record original values for statistics
            original_values = df['weather'].value_counts()
            
            # Standardize weather column (strip spaces, capitalize first letter)
            df['weather'] = df['weather'].str.strip().str.title()
            
            # Perform mapping
            df['weather'] = df['weather'].map(weather_mapping)
            
            # Handle values not found in mapping, set to 0 (Other)
            missing_mask = df['weather'].isna()
            if missing_mask.any():
                missing_values = df.loc[missing_mask, 'weather'].index
                df.loc[missing_mask, 'weather'] = 0  # Map to Other
                print(f"  Warning: Found unmapped values in file {os.path.basename(file_path)}, set to 0 (Other)")
            
            # Overwrite original file directly
            df.to_csv(file_path, index=False)
            
            # Statistics
            mapped_values = df['weather'].value_counts().sort_index()
            print(f"✓ Processed: {os.path.basename(file_path)}")
            print(f"  Mapping statistics: {dict(mapped_values)}")
            
            processed_count += 1
            
        except Exception as e:
            print(f"✗ Error processing file {os.path.basename(file_path)}: {e}")
            error_files.append(os.path.basename(file_path))
    
    # Output summary
    print(f"\nProcessing complete!")
    print(f"Successfully processed: {processed_count}/{len(csv_files)} files")
    if error_files:
        print(f"Failed files: {error_files}")

# Use default path directly, no interactive input
if __name__ == "__main__":
    # Default input folder path
    input_folder = "D:/School/MPU_Master/2025Busdata/data/grandprix"
    
    print("=== CSV File Weather Column Batch Mapping Tool ===")
    print(f"Starting processing of folder: {input_folder}")
    
    if not os.path.exists(input_folder):
        print(f"Error: The specified folder {input_folder} does not exist")
    else:
        map_weather_conditions(input_folder)
    
    print("\nProgram finished, press any key to exit...")
    input()