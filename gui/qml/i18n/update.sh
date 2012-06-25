#!/bin/sh
# update l18n to reflect source code changes

# update the .ts files
lupdate ../*.qml -locations absolute -ts *.ts

# regenerate the .qml files
lrelease *.ts