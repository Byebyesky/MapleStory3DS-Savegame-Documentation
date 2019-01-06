#ifndef SAVEFILES_H
#define SAVEFILES_H

#include <vector>
#include <stdint.h>

//Title screen
struct summary {
    uint16_t name[9];

    uint16_t unk; // always 1?

    uint16_t year;
    uint8_t month;
    uint8_t day;
    uint8_t hour;
    uint8_t minute;

    uint8_t chapter;
    uint8_t level;

    uint32_t null; // \0 bytes

    uint32_t robeEquipped;
    uint32_t hatEquipped;
    uint32_t weaponEquipped;

    uint32_t bootsEquipped;
    uint32_t ringEquipped;
    uint32_t earringsEquipped;
    uint32_t medalEquipped;
    
    uint32_t playtime;
};

struct mainQuest {
    uint32_t activeMainQuest;
};

//Common variables between saves
struct common {
    uint16_t lastSave; //00 00 -> slot1, 01 00 -> slot2, else none
    uint16_t unlockedMovies; //100-109 -> movies in squence, IDs in Movie_title_JP.gmm
    
    uint8_t firstSlotUsed; //0 false or 1 true
    uint8_t secondSlotUsed;
    uint8_t firstSlotComplete;
    uint8_t secondSlotComplete;

    uint8_t creditsPicture;//0 false or 1 true, usually true if game completed
    uint8_t unk1;
    uint16_t unk2;

    uint8_t padding[24]; //rest of the file seems to do nothing
};

//Ingame data
struct playerData {
    int8_t level; //yes signed
    uint8_t padding[3];
    int32_t experience; //signed
    int16_t CurrentHp;
    int16_t CurrentMp;
    uint32_t currentMap; //IDs in Map_Name_JP.gmm

    uint8_t NPCSomething[16];

    uint8_t padding1[48];

    uint8_t companionNPCString[16]; //Only HPxxx:xx NPCs
    
    uint8_t padding2[8];

    //Skills 0x00 - 0x1C
    uint8_t LSkill;
    uint8_t YSkill;
    uint8_t XSkill;
    uint8_t RSkill;
    uint8_t UpLSkill;
    uint8_t UpYSkill;
    uint8_t UpXSkill;
    uint8_t UpRSkill;

    uint16_t learnedSkills; //Probably bit field
    uint8_t padding3[4];
    uint16_t newIndicator; // Probably bit field; Skill bit not 1 -> NEW indicator
    uint8_t padding4[4];
};

typedef struct {
    int32_t id;
    int32_t amount;
    int32_t padding;
}item;

typedef struct {
    int32_t numberOfItems; //numItems*0xC
    std::vector<item> items;
}itemlist;

struct inventory {
    int32_t quickSlot1;
    int32_t quickslot2;
    int32_t money;
    itemlist armor;
    itemlist accessory;
    itemlist weapon;
    itemlist shoes;
    int32_t something[4];
    itemlist consumables;
};

#endif