#!/bin/bash

# Exécuter add_gestion_user
python manage.py add_gestion_user
if [ $? -ne 0 ]; then
    echo "Failed to execute add_gestion_user"
    exit 1
fi

# Exécuter add_biens
python manage.py add_biens
if [ $? -ne 0 ]; then
    echo "Failed to execute add_biens"
    exit 1
fi

# Exécuter add_units
python manage.py add_units
if [ $? -ne 0 ]; then
    echo "Failed to execute add_units"
    exit 1
fi

# Exécuter add_tenants
python manage.py add_tenants
if [ $? -ne 0 ]; then
    echo "Failed to execute add_tenants"
    exit 1
fi

echo "All commands executed successfully"
#chmod +x run_management_commands.sh il faut faire ca pour rendre le fichier executable
#./run_management_commands.sh pour executer le fichier