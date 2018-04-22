# MapleStory3DS Savegame Documentation

This is a repository about the Documentation of the MapleStory3DS format.

## Files of the Savegame
### achievement.dat
TODO
### common.dat
TODO
### globalFlag.dat
TODO
### inventory.dat

money: 0x08 - 0x0B

See [ItemIDs](https://github.com/Byebyesky/MapleStory3DS-Savegame-Documentation/blob/master/ItemIDs.txt) for available IDs

### mainQuest.dat

quest: 0x00
See [MainQuestIDs](https://github.com/Byebyesky/MapleStory3DS-Savegame-Documentation/blob/master/MainQuestIDs.txt)

### playerData.dat

level: 0x00
Ingame, changeing breaks EXPBar but grants the skills

exp: 0x04 - 0x07
EXPBar seems to normalize as soon as 1 ememy is killed

hp: 0x08 - 0x09
Current HP, max HP seems to be specified in the romfs(?)

mp: 0x0A - 0x0B
Current MP, max MP seems to be specified in the romfs(?)

### subQuest.dat

A 0x10000000 seperates running and done quests
See [SubQuestIDs](https://github.com/Byebyesky/MapleStory3DS-Savegame-Documentation/blob/master/SubQuestIDs.txt)

### summary_x.dat

name: 0x00 - 0x0E
In UTF-16

level: 0x1B
Only on the title screen

Equipped Items: 0x20 - 0x3B
0xFFFFFFFF for none
See [ItemIDs](https://github.com/Byebyesky/MapleStory3DS-Savegame-Documentation/blob/master/ItemIDs.txt) for available IDs

Visible Items:
Changing those to wrong ID or 0xFFFFFFFF crashes game!

Robe Equipped: 0x20 - 0x23

Hat Equipped: 0x24 - 0x27

Weapon Equipped: 0x28 - 0x2B

Invisible Items:
Boots Equipped: 0x2C - 0x2F

Ring Equipped: 0x30 - 0x33

Earrings Equipped: 0x34 - 0x37

Medal Equipped:	0x38 - 0x3B

Time: 0x3C - 0x7F			    
In seconds
