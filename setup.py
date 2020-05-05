import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="PittJumper",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["pitjumpertitle.png"]}},
    executables = executables

    )