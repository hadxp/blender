import os
import bpy
import time
import subprocess


def exec(filepath):
    """
    Called when the operator is executed
    """
    return import_pac_file(filepath)


def import_pac_file(filepath):
    """
    Converts an .pac file into an DAE file, importable by blender.
    """
    
    # Access the selected file's full filepath and filename
    full_pac_path = filepath
    pac_filename = bpy.path.display_name_from_filepath(full_pac_path)

    # Check if the full_pac_path variable doesn't end in ".pac"
    if not full_pac_path.endswith('.pac'):
        # Append ".pac" to the variable
        full_pac_path += '.pac'

    # Get the first three letters of the pac-file-name
    class_abbreviation = pac_filename[:3]

    # get the directory of the pacfile
    pac_dir_path = os.path.dirname(full_pac_path)
    
    # path and name of the mesh0_lod0 dae file
    full_path_to_dae = os.path.join(pac_dir_path, f"{pac_filename}_mesh00_lod0.dae")
    
    # check if the mesh0_lod0 dae file already exists, and if the pactool needs to execute
    if not os.path.exists(full_path_to_dae):
        # execute the pactool
        full_path_to_dae = run_pactool(full_pac_path, full_path_to_dae, class_abbreviation)
    
    # only import the dae, if it was set
    if full_path_to_dae is not None and full_path_to_dae != '':
        print(f'Importing collada: {full_path_to_dae}')
        # Run the Collada import operator with the full path to the DAE file
        bpy.ops.wm.collada_import(filepath=full_path_to_dae, filter_blender=False)
        return {'FINISHED'}
    
    return {'CANCELLED'}


def run_pactool(full_pac_path, full_path_to_dae, class_abbreviation):
    """
    Executes the pactool in conversion mode to convert an PAC to a DAE file
    """
    
    # Get the directory of the Python script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Specify the path to the pactool file (assuming it's in the same directory)
    pactool_exe = os.path.join(script_directory, 'PACtool.exe')
    
    # Specify the path to the bones directory
    bones_directory = os.path.join(script_directory, 'bones')
    
    # Specify the command as a string
    command = f"{pactool_exe} -c -refAllBones {full_pac_path} {bones_directory}\{class_abbreviation}_01.pab"
    
    # print out the command string
    print(f'Executing pactool: {command}')
    
    # Run the pactool command
    return_code = subprocess.call(command, shell=True)
    
    # Get the current time
    start_time = time.time()
    
    # create a while loop which waits 5 seconds for the pactool to finish executing
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        if os.path.exists(full_path_to_dae):
                # return when the file exists (this will break the while loop)
                return full_path_to_dae
        
        if elapsed_time >= 5:
            print(f'ERROR: The file {full_path_to_dae} did not exist, '
            'the PACtool did not complete within time')
            break
    
    return ''
    
