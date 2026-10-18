from database import engine, SessionLocal, Base
from models import (
    Character, Weapon, ArtifactSet, Build, BuildWeapon, 
    BuildArtifactSet, Team, TeamMember,
    ElementEnum, WeaponTypeEnum, WeaponPriorityEnum, 
    ArtifactSetTypeEnum, TeamRoleEnum
)

CHARACTERS_DATA = [
    # Mondstadt
    {"name": "Albedo", "element": ElementEnum.GEO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Mondstadt", "description": "Chief Alchemist and Captain of the Investigation Team of the Knights of Favonius."},
    {"name": "Amber", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 4, "region": "Mondstadt", "description": "The only remaining Outrider of the Knights of Favonius."},
    {"name": "Barbara", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 4, "region": "Mondstadt", "description": "The Deaconess of the Church of Favonius and a shining idol."},
    {"name": "Bennett", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 4, "region": "Mondstadt", "description": "An adventurous young man known for his tremendous luck-defying support."},
    {"name": "Diluc", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 5, "region": "Mondstadt", "description": "The tycoon of a winery empire in Mondstadt and the Darknight Hero."},
    {"name": "Diona", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 4, "region": "Mondstadt", "description": "A young feline bartender who crafts incredible cocktails and shields."},
    {"name": "Eula", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 5, "region": "Mondstadt", "description": "The Spindrift Knight and captain of the Reconnaissance Company."},
    {"name": "Fischl", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 4, "region": "Mondstadt", "description": "The Prinzessin der Verurteilung who travels with the night raven Oz."},
    {"name": "Jean", "element": ElementEnum.ANEMO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Mondstadt", "description": "The Acting Grand Master of the Knights of Favonius."},
    {"name": "Kaeya", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 4, "region": "Mondstadt", "description": "The charming Cavalry Captain of the Knights of Favonius."},
    {"name": "Klee", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 5, "region": "Mondstadt", "description": "The Spark Knight whose explosive antics bring fiery chaos."},
    {"name": "Lisa", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 4, "region": "Mondstadt", "description": "The clever and languid Librarian of the Knights of Favonius."},
    {"name": "Mika", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 4, "region": "Mondstadt", "description": "A young surveyor of the Knights of Favonius Reconnaissance Company."},
    {"name": "Mona", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 5, "region": "Mondstadt", "description": "An erudite astrologer with supreme mastery over Hydro divinations."},
    {"name": "Noelle", "element": ElementEnum.GEO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 4, "region": "Mondstadt", "description": "A chivalrous maid of the Knights of Favonius providing unbreakable shields."},
    {"name": "Razor", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 4, "region": "Mondstadt", "description": "A boy raised by the wolves of Wolvendom."},
    {"name": "Rosaria", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 4, "region": "Mondstadt", "description": "A shadowy sister of the Church of Favonius who works from the darkness."},
    {"name": "Sucrose", "element": ElementEnum.ANEMO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 4, "region": "Mondstadt", "description": "An alchemist obsessed with bio-alchemy and elemental grouping."},
    {"name": "Venti", "element": ElementEnum.ANEMO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 5, "region": "Mondstadt", "description": "A bard that seems to have arrived on some gentle breeze; the Anemo Archon."},

    # Liyue
    {"name": "Baizhu", "element": ElementEnum.DENDRO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 5, "region": "Liyue", "description": "The owner of Bubu Pharmacy, accompanied by the white snake Changsheng."},
    {"name": "Beidou", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 4, "region": "Liyue", "description": "Captain of the Crux fleet, unmatched in countering incoming damage."},
    {"name": "Chongyun", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 4, "region": "Liyue", "description": "A young exorcist born with excessive positive yang energy."},
    {"name": "Gaming", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 4, "region": "Liyue", "description": "A passionate Wushou dancer and secure transport guard from Yilong Wharf."},
    {"name": "Ganyu", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 5, "region": "Liyue", "description": "The half-qilin emissary and secretary for the Liyue Qixing."},
    {"name": "Hu Tao", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 5, "region": "Liyue", "description": "The 77th Director of the Wangsheng Funeral Parlor, master of Pyro burst damage."},
    {"name": "Keqing", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Liyue", "description": "The Yuheng of the Liyue Qixing, swift and precise in combat."},
    {"name": "Lan Yan", "element": ElementEnum.ANEMO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 4, "region": "Liyue", "description": "A graceful artisan from Chenyu Vale skilled in elemental swirling."},
    {"name": "Ningguang", "element": ElementEnum.GEO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 4, "region": "Liyue", "description": "The Tianquan of the Liyue Qixing, wealthy ruler of the Jade Chamber."},
    {"name": "Qiqi", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Liyue", "description": "An herb gatherer and apprentice at Bubu Pharmacy; a resurrected zombie."},
    {"name": "Shenhe", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 5, "region": "Liyue", "description": "An adeptus disciple with ferocious Cryo-buffing potential."},
    {"name": "Xiangling", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 4, "region": "Liyue", "description": "A renowned chef from Wanmin Restaurant and premier off-field Pyro dealer."},
    {"name": "Xianyun", "element": ElementEnum.ANEMO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 5, "region": "Liyue", "description": "The Cloud Retainer adeptus taking human form to boost plunge attacks."},
    {"name": "Xiao", "element": ElementEnum.ANEMO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 5, "region": "Liyue", "description": "The Vigilant Yaksha who purges demons across Liyue with soaring plunges."},
    {"name": "Xingqiu", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 4, "region": "Liyue", "description": "The second son of the Feiyun Commerce Guild, master of Rain Swords."},
    {"name": "Xinyan", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 4, "region": "Liyue", "description": "Liyue's sole rock 'n' roll pioneer, utilizing blazing physical beats."},
    {"name": "Yanfei", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 4, "region": "Liyue", "description": "A top legal adviser in Liyue Harbor with illuminated beast blood."},
    {"name": "Yaoyao", "element": ElementEnum.DENDRO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 4, "region": "Liyue", "description": "A diligent young disciple under Madame Ping with her healing rabbit Yuegui."},
    {"name": "Yelan", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 5, "region": "Liyue", "description": "A mysterious operative who claims to work for the Ministry of Civil Affairs."},
    {"name": "Yun Jin", "element": ElementEnum.GEO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 4, "region": "Liyue", "description": "A prestigious opera director who boosts normal attack damage across the party."},
    {"name": "Zhongli", "element": ElementEnum.GEO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 5, "region": "Liyue", "description": "Consultant of the Wangsheng Funeral Parlor; the Geo Archon Rex Lapis."},

    # Inazuma
    {"name": "Arataki Itto", "element": ElementEnum.GEO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 5, "region": "Inazuma", "description": "The First and Greatest Head of the Arataki Gang, powerhouse Geo DPS."},
    {"name": "Chiori", "element": ElementEnum.GEO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Inazuma / Fontaine", "description": "The boss of Chioriya Boutique, weaving dual blades with Geo automatons."},
    {"name": "Gorou", "element": ElementEnum.GEO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 4, "region": "Inazuma", "description": "The courageous general of the Watatsumi Army who empowers Geo allies."},
    {"name": "Kaedehara Kazuha", "element": ElementEnum.ANEMO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Inazuma", "description": "A wandering samurai who groups enemies and grants massive elemental buffs."},
    {"name": "Kamisato Ayaka", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Inazuma", "description": "The Shirasagi Himegimi of the Yashiro Commission, devastating in Freeze comps."},
    {"name": "Kamisato Ayato", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Inazuma", "description": "The Head of the Kamisato Clan and Yashiro Commissioner."},
    {"name": "Kirara", "element": ElementEnum.DENDRO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 4, "region": "Inazuma", "description": "A friendly nekomata courier for Komaniya Express with durable Dendro shields."},
    {"name": "Kujou Sara", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 4, "region": "Inazuma", "description": "General of the Tenryou Commission, devoted to the Raiden Shogun."},
    {"name": "Kuki Shinobu", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 4, "region": "Inazuma", "description": "The capable deputy leader of the Arataki Gang and elite Hyperbloom trigger."},
    {"name": "Raiden Shogun", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 5, "region": "Inazuma", "description": "The Electro Archon who recharges the team while unleashing slashes of Eternity."},
    {"name": "Sangonomiya Kokomi", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 5, "region": "Inazuma", "description": "The Divine Priestess of Watatsumi Island, supreme healer and Hydro enabler."},
    {"name": "Sayu", "element": ElementEnum.ANEMO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 4, "region": "Inazuma", "description": "A pint-sized ninja of the Shuumatsuban who rolls swiftly to heal."},
    {"name": "Shikanoin Heizou", "element": ElementEnum.ANEMO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 4, "region": "Inazuma", "description": "A brilliant detective who strikes down suspects with martial Anemo punches."},
    {"name": "Thoma", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 4, "region": "Inazuma", "description": "The Kamisato Clan's housekeeper, skilled in maintaining shields and Burgeon."},
    {"name": "Yae Miko", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 5, "region": "Inazuma", "description": "The Guuji of the Grand Narukami Shrine and editor-in-chief of Yae Publishing House."},
    {"name": "Yoimiya", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 5, "region": "Inazuma", "description": "The Queen of the Summer Festival and owner of Naganohara Fireworks."},

    # Sumeru
    {"name": "Alhaitham", "element": ElementEnum.DENDRO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Sumeru", "description": "The Scribe of the Sumeru Akademiya, wielding projecting mirrors of Dendro."},
    {"name": "Candace", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 4, "region": "Sumeru", "description": "The guardian of Aaru Village who shields her allies and infuses Hydro."},
    {"name": "Collei", "element": ElementEnum.DENDRO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 4, "region": "Sumeru", "description": "A Trainee Forest Ranger who patrols the Avidya Forest."},
    {"name": "Cyno", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 5, "region": "Sumeru", "description": "The General Mahamatra who dispenses righteous judgment across the sands."},
    {"name": "Dehya", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 5, "region": "Sumeru", "description": "The Flame-Mane, a brave mercenary of the Eremites who absorbs ally damage."},
    {"name": "Dori", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 4, "region": "Sumeru", "description": "An elusive merchant with an obsession for Mora and Jinni spirits."},
    {"name": "Faruzan", "element": ElementEnum.ANEMO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 4, "region": "Sumeru", "description": "A legendary scholar and the absolute cornerstone support for Anemo carries."},
    {"name": "Kaveh", "element": ElementEnum.DENDRO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 4, "region": "Sumeru", "description": "A passionate architect whose toolbox Mehrak detonates Bloom cores."},
    {"name": "Layla", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 4, "region": "Sumeru", "description": "A sleepy Rtawahist student who creates thick Cryo sleep shields."},
    {"name": "Nahida", "element": ElementEnum.DENDRO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 5, "region": "Sumeru", "description": "Lesser Lord Kusanali, the Dendro Archon, premier enabler for all Dendro reactions."},
    {"name": "Nilou", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Sumeru", "description": "A star dancer of Zubayr Theater whose bountiful blooms explode instantaneously."},
    {"name": "Sethos", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 4, "region": "Sumeru", "description": "The leader of the Temple of Silence who fires piercing Electro shadow arrows."},
    {"name": "Tighnari", "element": ElementEnum.DENDRO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 5, "region": "Sumeru", "description": "The Chief Officer of the Forest Watchers, swift at homing Dendro volleys."},
    {"name": "Wanderer", "element": ElementEnum.ANEMO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 5, "region": "Sumeru", "description": "A transient being who soars through the skies unleashing rapid Anemo blades."},

    # Fontaine
    {"name": "Arlecchino", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 5, "region": "Fontaine / Snezhnaya", "description": "The Fourth of the Fatui Harbingers. A dominant Pyro Hypercarry."},
    {"name": "Charlotte", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 4, "region": "Fontaine", "description": "An enthusiastic journalist for The Steambird who heals with flash photography."},
    {"name": "Chevreuse", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 4, "region": "Fontaine", "description": "Captain of the Special Security and Surveillance Patrol, dedicated to Overload."},
    {"name": "Clorinde", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Fontaine", "description": "Fontaine's Champion Duelist, executing rapid lunges and gunshots."},
    {"name": "Emilie", "element": ElementEnum.DENDRO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 5, "region": "Fontaine", "description": "A renowned perfumer who specializes in Burning reaction amplifiers."},
    {"name": "Freminet", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 4, "region": "Fontaine", "description": "A reserved young diver who fights alongside his mechanical penguin Pers."},
    {"name": "Furina", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Fontaine", "description": "The star performer and former Hydro Archon, providing massive party-wide damage boosts."},
    {"name": "Lynette", "element": ElementEnum.ANEMO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 4, "region": "Fontaine", "description": "A quiet and observant magician's assistant who moves with feline agility."},
    {"name": "Lyney", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 5, "region": "Fontaine", "description": "A celebrated magician who excels in Mono-Pyro charged bow combat."},
    {"name": "Navia", "element": ElementEnum.GEO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 5, "region": "Fontaine", "description": "President of Spina di Rosula who blasts enemies with her gunbrella via Crystallize."},
    {"name": "Neuvillette", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 5, "region": "Fontaine", "description": "The Iudex of Fontaine and Hydro Sovereign, firing torrential hydro beams."},
    {"name": "Sigewinne", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 5, "region": "Fontaine", "description": "The head nurse of Fortress of Meropide who supports allies with bouncing hydro bubbles."},
    {"name": "Wriothesley", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 5, "region": "Fontaine", "description": "The Duke of the Fortress of Meropide, fighting with ferocious Cryo gauntlets."},

    # Natlan
    {"name": "Chasca", "element": ElementEnum.ANEMO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 5, "region": "Natlan", "description": "A Tlalocan peacekeeper who rides a flying cannon converting elemental bullets."},
    {"name": "Citlali", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 5, "region": "Natlan", "description": "An elder of the Masters of the Night-Wind, expert in Cryo shields and totems."},
    {"name": "Iansan", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 4, "region": "Natlan", "description": "A determined warrior and coach from the Collective of Plenty."},
    {"name": "Kachina", "element": ElementEnum.GEO, "weapon_type": WeaponTypeEnum.POLEARM, "rarity": 4, "region": "Natlan", "description": "A young warrior from the Children of Echoes who rides the Turbo Twirler."},
    {"name": "Kinich", "element": ElementEnum.DENDRO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 5, "region": "Natlan", "description": "A Huitztlan dragon hunter who swings around foes with the dragon lord Ajaw."},
    {"name": "Mavuika", "element": ElementEnum.PYRO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 5, "region": "Natlan", "description": "The Pyro Archon and champion of Natlan, riding a flaming motorcycle."},
    {"name": "Mualani", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 5, "region": "Natlan", "description": "A vibrant watersports guide who surfs into enemies with Sharky Surfer."},
    {"name": "Ororon", "element": ElementEnum.ELECTRO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 4, "region": "Natlan", "description": "A contemplative young man who channels Electro spirits from the Night-Wind tribe."},
    {"name": "Xilonen", "element": ElementEnum.GEO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Natlan", "description": "A master smith of the Children of Echoes who shreds all elemental resistances on roller skates."},

    # Snezhnaya & Other Factions
    {"name": "Tartaglia", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 5, "region": "Snezhnaya", "description": "No. 11 of The Harbingers, also known as 'Childe', thriving in rapid Riptide stance switches."},
    {"name": "Columbina", "element": ElementEnum.HYDRO, "weapon_type": WeaponTypeEnum.CATALYST, "rarity": 5, "region": "Snezhnaya / Nod-Krai", "description": "The 3rd of the Fatui Harbingers, possessing enigmatic cosmic melodies."},
    {"name": "Sandrone", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.CLAYMORE, "rarity": 5, "region": "Snezhnaya", "description": "The 7th of the Fatui Harbingers, who commands mechanical automatons."},
    {"name": "Skirk", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.SWORD, "rarity": 5, "region": "Teyvat / Abyss", "description": "The mysterious warrior from the dark depths who trained Tartaglia."},
    {"name": "Alois", "element": ElementEnum.CRYO, "weapon_type": WeaponTypeEnum.BOW, "rarity": 5, "region": "Otherworldly", "description": "The Savior from Another World and skilled hunter of mechanical machines."}
]

def populate_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        characters_map = {}
        for char_info in CHARACTERS_DATA:
            char_obj = Character(**char_info)
            db.add(char_obj)
            characters_map[char_info["name"]] = char_obj

        db.commit()

        w_crimson = Weapon(name="Crimson Moon's Semblance", weapon_type=WeaponTypeEnum.POLEARM, rarity=5, base_attack=674, substat="CRIT Rate 22.1%", passive_desc="Grants Bond of Life and elemental DMG bonus.")
        w_tassel = Weapon(name="White Tassel", weapon_type=WeaponTypeEnum.POLEARM, rarity=3, base_attack=401, substat="CRIT Rate 23.4%", passive_desc="Boosts normal attacks.")
        w_splendor = Weapon(name="Splendor of Tranquil Waters", weapon_type=WeaponTypeEnum.SWORD, rarity=5, base_attack=542, substat="CRIT DMG 88.2%", passive_desc="Boosts skill damage.")
        w_kazuha = Weapon(name="Freedom-Sworn", weapon_type=WeaponTypeEnum.SWORD, rarity=5, base_attack=608, substat="Elemental Mastery 198", passive_desc="Increases party damage on elemental reactions.")
        db.add_all([w_crimson, w_tassel, w_splendor, w_kazuha])
        db.commit()

        art_whimsy = ArtifactSet(name="Fragment of Harmonic Whimsy", two_piece_bonus="ATK +18%", four_piece_bonus="Increases damage up to 54% via Bond of Life.")
        art_gladiator = ArtifactSet(name="Gladiator's Finale", two_piece_bonus="ATK +18%", four_piece_bonus="Increases Normal Attack DMG by 35%.")
        art_troupe = ArtifactSet(name="Golden Troupe", two_piece_bonus="Skill DMG +20%", four_piece_bonus="Skill DMG +25%, further increased when off-field.")
        art_vv = ArtifactSet(name="Viridescent Venerer", two_piece_bonus="Anemo DMG +15%", four_piece_bonus="Decreases opponent's Elemental RES by 40%.")
        db.add_all([art_whimsy, art_gladiator, art_troupe, art_vv])
        db.commit()

        if "Arlecchino" in characters_map:
            b_arl = Build(
                character_id=characters_map["Arlecchino"].id,
                role_title="Main DPS - Hypercarry",
                stats_priority="Sands: ATK% | Goblet: Pyro DMG | Circlet: CRIT Rate / CRIT DMG",
                notes="Maintain Bond of Life to maximize normal attack damage."
            )
            db.add(b_arl)
            db.commit()
            db.add_all([
                BuildWeapon(build_id=b_arl.id, weapon_id=w_crimson.id, priority=WeaponPriorityEnum.SIGNATURE, notes="Signature weapon."),
                BuildWeapon(build_id=b_arl.id, weapon_id=w_tassel.id, priority=WeaponPriorityEnum.BUDGET, notes="Budget 3-star option."),
                BuildArtifactSet(build_id=b_arl.id, artifact_set_id=art_whimsy.id, set_type=ArtifactSetTypeEnum.FOUR_PIECE, notes="Best in slot."),
                BuildArtifactSet(build_id=b_arl.id, artifact_set_id=art_gladiator.id, set_type=ArtifactSetTypeEnum.FOUR_PIECE, notes="Alternative.")
            ])

        if all(k in characters_map for k in ["Arlecchino", "Furina", "Kaedehara Kazuha", "Bennett"]):
            team_vape = Team(
                name="Arlecchino Vaporize Meta",
                team_type="Meta",
                description="High damage team utilizing Hydro vaporize reactions with Anemo shred."
            )
            db.add(team_vape)
            db.commit()
            db.add_all([
                TeamMember(team_id=team_vape.id, character_id=characters_map["Arlecchino"].id, role=TeamRoleEnum.MAIN_DPS, notes="On-field attacker."),
                TeamMember(team_id=team_vape.id, character_id=characters_map["Furina"].id, role=TeamRoleEnum.SUB_DPS, notes="Hydro application and buff."),
                TeamMember(team_id=team_vape.id, character_id=characters_map["Kaedehara Kazuha"].id, role=TeamRoleEnum.SUPPORT, notes="4pc VV shred & buff."),
                TeamMember(team_id=team_vape.id, character_id=characters_map["Bennett"].id, role=TeamRoleEnum.HEALER, notes="ATK buff and healing.")
            ])
            db.commit()

        print(f"Database successfully populated with {len(CHARACTERS_DATA)} characters!")
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()