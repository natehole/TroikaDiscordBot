# Data Directory

This is where you can put compendiums and load them from the bot. Note that by
default only the troika.yml file is loaded, since that represents the base
rules. But you can add other background files and it can use them instead of the
main backgrounds potentially. Since those backgrounds may have been produced by
outside creators, do NOT add them to the Github repo.

The idea is to represent Troika things as a YAML file that can be auto-loaded by the bot.

## Basic Structure of a Compendium File

Compendium files are written in YAML with the following basic structure and detailed sub-fields

``` yaml
name: The Name of this Template
key: An optional short key that can be used to refer to items only in this template (useful for name conflicts)
url: Url to find the source
author: The author of this compendium
backgrounds: optional, see below
weapons: optional, see below
spells: optional, see below
creatures: optional, see below
tables: optional, see below
```

### Background Table

An example background can look like this:



