import xarray as xr
import sys
import os

def compare_nc_files(path1, path2):
    # Check if paths are files or directories
    if os.path.isdir(path1) and os.path.isdir(path2):
        # Compare files in the directories
        files1 = {f: os.path.join(path1, f) for f in os.listdir(path1) if f.endswith('.nc')}
        files2 = {f: os.path.join(path2, f) for f in os.listdir(path2) if f.endswith('.nc')}
        
        # Check if the same files exist in both directories
        if files1.keys() != files2.keys():
            raise ValueError("The directories must contain the same files.")

        # Compare each pair of files
        for filename in files1.keys():
            if not compare_single_file(files1[filename], files2[filename]):
                print(f"Files {filename} are different.")
                return False
            
        print("All files in the directories are equal.")
        return True

    elif os.path.isfile(path1) and os.path.isfile(path2):
        # If both paths are files, compare them
        return compare_single_file(path1, path2)

    else:
        raise ValueError("Both paths must point to either files or directories.")

def compare_single_file(file1, file2):
    if not (file1.endswith('.nc') and file2.endswith('.nc')):
        raise ValueError("Both paths must point to .nc files")

    try:
        dataset1 = xr.open_dataset(file1)
        dataset2 = xr.open_dataset(file2)
    except Exception as e:
        raise IOError(f"Error opening the files: {e}")

    # Compare the datasets
    return dataset1.equals(dataset2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_nc.py <path_to_file1.nc_or_directory> <path_to_file2.nc_or_directory>")
        sys.exit(1)

    path1 = sys.argv[1]
    path2 = sys.argv[2]

    # Compare the files or directories
    try:
        result = compare_nc_files(path1, path2)
        if result:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)