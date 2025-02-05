set CHEMIN=%~dp0
set CHEMIN=%CHEMIN:~0,-1%
cd %CHEMIN%
%CHEMIN%\.venv\Scripts\python.exe app.py --workdir "%CHEMIN%" --params_folder parameters --metaparams_json metaparams.json --params_time_json params_time.json --params_variables_json params_variables.json