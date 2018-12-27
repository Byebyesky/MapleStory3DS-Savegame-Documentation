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

**Money:** 0x08 - 0x0B  

See [ItemIDs](https://github.com/Byebyesky/MapleStory3DS-Savegame-Documentation/blob/master/ItemIDs.txt) for available IDs  

### mainQuest.dat

**Quest:** 0x00  
See [MainQuestIDs](https://github.com/Byebyesky/MapleStory3DS-Savegame-Documentation/blob/master/MainQuestIDs.txt)  

### playerData.dat

**Level:** 0x00  
Ingame, changeing breaks EXPBar but grants the skills

**Exp:** 0x04 - 0x07  
EXPBar seems to normalize as soon as 1 ememy is killed

**Hp:** 0x08 - 0x09  
Current HP, max HP seems to be specified in the romfs(?)  

**Mp:** 0x0A - 0x0B  
Current MP, max MP seems to be specified in the romfs(?)  

### subQuest.dat

A **0x10000000** seperates running and done quests  
See [SubQuestIDs](https://github.com/Byebyesky/MapleStory3DS-Savegame-Documentation/blob/master/SubQuestIDs.txt)  

### summary_x.dat

**Name:** 0x00 - 0x11  
In UTF-16  

**???:** 0x12 - 0x13 (1) 

**Year:** 0x14 - 0x15  
**Month:** 0x16  
**Day:** 0x17  
**Hour:** 0x18  
**Minute:** 0x19  

**Chapter:** 0x1A

**Level:** 0x1B  
Only on the title screen  

**Padding:** 0x1C - 0x1F ('\0')

**Equipped Items:** 0x20 - 0x3B  
0xFFFFFFFF for none  
See [ItemIDs](https://github.com/Byebyesky/MapleStory3DS-Savegame-Documentation/blob/master/ItemIDs.txt) for available IDs  

**Visible Items:**  
Changing those to wrong ID or 0xFFFFFFFF crashes game!

**Robe Equipped:** 0x20 - 0x23  
**Hat Equipped:** 0x24 - 0x27  
**Weapon Equipped:** 0x28 - 0x2B  

**Invisible Items:**  
**Boots Equipped:** 0x2C - 0x2F  
**Ring Equipped:** 0x30 - 0x33  
**Earrings Equipped:** 0x34 - 0x37  
**Medal Equipped:**	0x38 - 0x3B  

**Playtime:** 0x3C - 0x3F  	    
In seconds
