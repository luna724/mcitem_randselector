if exist ./.venv (
  goto :launch
) else (
  python -m venv .venv
  goto :pip
)


:pip
call .venv/scripts/activate
pip install -r requirements.txt

:launch
call .venv/scripts/activate
python launch.py
pause