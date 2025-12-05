# # pip install -r requirements.txt
# # pip install botbuilder-core==4.14.0 botbuilder-schema==4.14.0 botbuilder-dialogs==4.14.0 aiohttp --no-deps


# #!/usr/bin/env bash
# set -o errexit

# echo "Installing dependencies..."
# pip install -r requirements.txt

# echo "Installing Bot Framework packages..."
# pip install botbuilder-core==4.14.0 \
#            botbuilder-schema==4.14.0 \
#            botbuilder-dialogs==4.14.0 \
#            aiohttp \
#            msrest --no-deps

# echo "Build completed!"


echo "Using Python 3.10"

# Install python-build (Render uses herokuish)
if ! command -v pyenv 2>/dev/null; then
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
fi

# Install Python 3.10.12 if not available
pyenv install -s 3.10.12
pyenv global 3.10.12

python3 --version
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install botbuilder-core==4.14.0 botbuilder-dialogs==4.14.0 botbuilder-schema==4.14.0 aiohttp --no-deps
