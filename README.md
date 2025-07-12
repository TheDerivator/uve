# What is uve

Use uv but

 - create environments in a central location 
 - with more conda-like syntax

Proof of concept for windows cmd.

# Install instructions:

 - git clone https://github.com/TheDerivator/uve.git
 - cd uve
 - [Optional: edit install.bat to use another location, default is C:\uve]
 - run install.bat
 - Add %UVE_DIR%/bin to your path

If you use Visual Studio Code, you can also add `"python.venvFolders": ["C:\\uve\\envs"]` to your settings.json, (or wherever your environments are).

# Testing

Verify that `where uve` gives you `%UVE_DIR%/bin/uve.bat`

Install environment:
```
uve env list
uve create -n my_env python=3.13 matplotlib pandas
uve activate my_env
uve install -n my_env plotly
```

Experimental! Many commands are not supported!

# How it works

1. Installation drops uve.bat and a python wheel in the %UVE%/bin folder
2. Calling `uve ...` will trigger the bat script.
3. If the command was activate, it will activate the environment and exit.
3. Otherwise, it passes the command to uvx
4. uvx can run the wheel directly, passing it to the uve module.
5. uve.py will examine the commands and execute `uv pip install --python %UVE_DIR%/envs/my_env ...`

This project is a POC (Proof of Concept) so for safety the script will ask you to confirm the commands.

# Why?
`uv` is great but lacks a nice interface to manage centrally maintained Python environments. Having an environment per project folder is too much for certain workflows with many notebooks and py-files scattered around.

Another project is this: https://github.com/robert-mcdermott/uve, which is a great idea but:
 - doesn't support windows cmd (probably easy to add)
 - Somehow uses Go
 - Has its own CLI which is different from both uv and conda

