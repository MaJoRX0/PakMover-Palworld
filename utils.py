import os
import shutil
import subprocess
import utils
def read_exe_hex_at_address(file_path, address, length):
    if not os.path.exists(file_path):
        print(f"The system cannot find the path specified: {file_path}")
        return
    try:
        # Open the file in binary mode
        with open(file_path, 'rb') as f:
            # Seek to the specified address
            f.seek(address)

            # Read the specified length of data from the address
            binary_data = f.read(length)

            # Convert binary data to hexadecimal representation
            hex_data = binary_data.hex()

            # Convert hexadecimal string to bytes and then decode to string
            string_data = bytes.fromhex(hex_data).decode("utf8", errors="replace")
            filtered_data = "".join(c for c in string_data if c.isalpha() or c in "/\\")
            # Print the string representation
            return extract_keyword(filtered_data)

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)


def extract_keyword(data):
    """
    Extracts the keyword between "Mods/" and "Actor" (or before the next "/").

    Args:
        data: The string containing the keyword.

    Returns:
        The extracted keyword or None if not found.
    """
    start_index = data.find("Mods/")
    if start_index != -1:
        end_index = data.find("Actor")
        if end_index != -1:
            return data[start_index + len("Mods/"):end_index]  # Extract between Mods/ and Actor
        else:
            # If "Actor" not found, extract up to the next "/"
            end_index = data.find("/", start_index + len("Mods/"))
            if end_index != -1:
                return data[start_index + len("Mods/"):end_index]
            else:
                # No delimiter found after "Mods/"
                return data[start_index + len("Mods/"):]  # Return everything after Mods/
    else:
        # "Mods/" not found
        return None


def read_and_extract_keywords_from_pak_files(directory_path):
  """
  Reads all .pak files in a given directory and extracts keywords.

  Args:
      directory_path: The path to the directory containing .pak files.

  Returns:
      A list of tuples, where each tuple contains (file_path, keyword).
  """
  results = []
  if not os.path.exists(directory_path):
      print(f"The system cannot find the path specified: {directory_path}")
      return
  for filename in os.listdir(directory_path):
    if filename.endswith(".pak"):
      file_path = os.path.join(directory_path, filename)
      try:
        # Read the hexadecimal string from the file
        data = read_exe_hex_at_address(file_path, 0x60, 70)  # Adjust addresses and lengths as needed
        # Extract the keyword
        if data:
          results.append((file_path, data))
      except FileNotFoundError:
        print(f"File not found: {file_path}")
      except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
  return results

def copy_and_rename_pak_files(results, destination_directory):
    """
    Copies .pak files based on results from read_and_extract_keywords_from_pak_files,
    renaming them with extracted keywords.

    Args:
        results: A list of tuples containing (file_path, keyword).
        destination_directory: The path to the destination directory.
    """
    if not os.path.exists(destination_directory):
        print(f"The system cannot find the path specified: {destination_directory}")
        return
    for file_path, keyword in results:
        if keyword:
            # Construct new filename with extracted keyword
            new_filename = f"{keyword}.pak"

            # Construct destination file path
            destination_path = os.path.join(destination_directory, new_filename)

            try:
                # Check if the file exists before copying
                if os.path.exists(file_path):
                    shutil.copy2(file_path, destination_path, follow_symlinks=True)
                    print(f"Copied {keyword} to /LogicMods (renamed to {new_filename})")
                else:
                    print(f"File not found: {file_path}")
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"An error occurred while processing {file_path}: {e}")

def launch_program(program_path):
    """
    Launches the specified program.

    Args:
        program_path: The path to the program executable.
    """
    try:
        subprocess.Popen(program_path)
        print(f"Launched program: {program_path}")
    except Exception as e:
        print(f"Failed to launch program: {e}")


def find_logic_mods_folder(game_path):
    """
    Finds the 'Pal\Content\Paks\LogicMods' folder within the provided game path.

    Args:
        game_path (str): The path to the game directory.

    Returns:
        str: The full path to the 'Pal\Content\Paks\LogicMods' folder if found, else None.
    """
    # Define the folder to find within the game path
    target_folder = 'Pal\\Content\\Paks\\LogicMods'

    # Check if the provided game path exists
    if os.path.exists(game_path):
        # Construct the full path to the LogicMods folder
        logic_mods_path = os.path.join(game_path, target_folder)
        # Check if the LogicMods folder exists
        if os.path.exists(logic_mods_path):
            return logic_mods_path
        else:
            print(f"LogicMods folder not found within: {game_path}")
            return None
    else:
        print(f"Game path not found: {game_path}")
        return None