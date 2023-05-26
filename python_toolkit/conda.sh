conda activate/deactivate ENV_NAME
conda env create -f environment.yml
conda create --name myenv
conda create -n py39 python=3.9 anaconda
conda env export > environment.yml
conda env remove -n ENV_NAME
conda env list
conda list # list of packages
conda env update --file environment.yml --prune # update current environment from file; remove pruned dependencies


# If env solving is taking too long, try setting channel priority in .condarc so that conda-forge is lower priority than defaults",
