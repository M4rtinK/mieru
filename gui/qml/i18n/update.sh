#!/bin/sh
# update l18n to reflect source code changes

# NOTE: adding a language

# update the .ts files
lupdate ../*.qml -locations absolute -ts *.ts

# regenerate the .qml files
lrelease *.ts
