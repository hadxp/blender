import os
import bpy
import time
import subprocess
from . import export_dae

def exec(filepath, operator, context, **kwargs):
    
    # Access the selected file's full filepath and filename
    full_pac_path = filepath
    pac_filename = bpy.path.display_name_from_filepath(full_pac_path)
    
    # get the directory of the pacfile
    pac_dir_path = os.path.dirname(full_pac_path)
    
    # get the path of the generated DAE file
    full_path_to_dae = os.path.join(pac_dir_path, f"{pac_filename}_mesh00_lod0.dae")
    
    # execute the save dae file method
    save_dae_file(full_path_to_dae, operator, context, **kwargs)
    
    return export_pac_file(full_pac_path, pac_filename, full_path_to_dae)


def save_dae_file(full_path_to_dae, operator, context, **kwargs):
    """
    Saves a scene in blender as a DAE file, 
    using the better collada exporter
    """
    print(f'Saving DAE: {full_path_to_dae}')
    export_dae.save(operator, context, filepath=full_path_to_dae, **kwargs)

def export_pac_file(full_pac_path, pac_filename, full_path_to_dae):
    """
    Converts an scene in blender (which was previously saved by the export_dae.save() function)
    to an .pac file.
    """
    print('Exporting PAC')
    
    # Check if the full_pac_path variable doesn't end in ".pac"
    if not full_pac_path.endswith('.pac'):
        # Append ".pac" to the variable
        full_pac_path += '.pac'
    
    # Get the first three letters of the pac-file-name
    class_abbreviation = pac_filename[:3]
    
    if os.path.exists(full_path_to_dae):
        # execute the pactool
        full_path_to_dae = run_pactool(full_pac_path, full_path_to_dae, class_abbreviation)
    else:
        print(f'ERROR: The DAE file does not exist: {full_path_to_dae}')
        full_path_to_dae = ''
    
    # only export the pac, if it was set
    if full_path_to_dae is not None and full_path_to_dae != '':
        print('DONE')
        return {'FINISHED'}
    
    return {'CANCELLED'}

def run_pactool(full_pac_path, full_path_to_dae, class_abbreviation):
    """
    Executes the pactool to convert an DAE to a PAC file
    """
    
    # Get the directory of the Python script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Specify the path to the pactool file (assuming it's in the same directory)
    pactool_exe = os.path.join(script_directory, 'PACtool.exe')
    
    # Specify the path to the bones directory
    bones_directory = os.path.join(script_directory, 'bones')
    
    # Specify the command as a string
    command = f"{pactool_exe} -r -replaceAllLOD -colorCoding {full_path_to_dae} {full_pac_path} {bones_directory}\{class_abbreviation}_01.pab"
    
    # print out the command string
    print(f'Executing pactool: {command}')
    
    # Run the pactool command
    subprocess.call(command, shell=True)
    
    # sleep for 2 seconds to give the pactool some time to execute
    time.sleep(2)
    
    return full_path_to_dae

