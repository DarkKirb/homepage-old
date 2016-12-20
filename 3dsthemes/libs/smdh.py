import sys
import struct
#Terrible use for class.
class SMDH:
    def read_u8(self):
        return struct.unpack('B', self.fin.read(1))[0]
    def read_u16(self):
        return struct.unpack('H', self.fin.read(2))[0]
    def read_u32(self):
        return struct.unpack('I', self.fin.read(4))[0]
    def read_u64(self):
        return struct.unpack('Q', self.fin.read(8))[0]
    def read_utf16(self, length): #in bytes
        return self.fin.read(length).decode('utf-16')
    def delete_trailing_nuls(self, v):
        while (v[-1] == '\0' and len(v) > 1):
            v = v[:-1]
        if v[0] == '\0':
            return ""
        return v
    def info_struct(self, t):
        short_t = self.delete_trailing_nuls(self.read_utf16(0x80))
        long_t = self.delete_trailing_nuls(self.read_utf16(0x100))
        pub_t = self.delete_trailing_nuls(self.read_utf16(0x80))
        self.contents[t]=(short_t,long_t,pub_t)
    def get_entry_bound(self, ent, _list):
        valid = ""
        for a, b in _list.iteritems():
            if ent >= a:
                valid = b
            else:
                break
        return valid
    def convert_rating(self, _list):
        rat = self.read_u8()
        if not (rat&0x80):
            rat = "N/A"
        elif rat & 0x40:
            rat = "Pending"
        elif rat & 0x20:
            rat = "Unrestricted"
        else:
            rat = rat & (~0x80)
            rat = get_entry_bound(rat, list)
        return str(rat)
    def ratings(self):
        cero = self.convert_rating({0: "A", 12: "B", 15: "C", 17: "D", 18: "Z"})
        esrb = self.convert_rating({0: "E", 10: "E10+", 13: "T", 17: "M", 18: "AO"})
        self.fin.read(1)
        usk = self.convert_rating({0: "0", 6:"6", 12:"12", 16:"16", 18:"18"})
        pegi_g = self.convert_rating({0: "3", 7:"7", 12:"12", 16:"16", 18:"18"})
        self.fin.read(1)
        pegi_p = self.convert_rating({0: "3", 7:"7", 12:"12", 16:"16", 18:"18"})
        pegi_b = self.convert_rating({0: "3", 7:"7", 12:"12", 16:"16", 18:"18"})
        cob = self.convert_rating({0: "G", 15: "M", 18: "R18+"})
        grb = self.convert_rating({0: "ALL", 12: "12", 15: "15", 18: "18"})
        cgsrr = self.convert_rating({0: "G", 6: "P", 12: "PG12", 15: "PG15", 18: "R"})
        self.fin.read(1)
        self.fin.read(1)
        self.fin.read(1)
        self.fin.read(1)
        self.fin.read(1)
        self.contents["Age Rating"] = {"CERO":cero, "ESRB":esrb, "USK":usk, "PEGI GEN":pegi_g, "PEGI PRT":pegi_p, "PEGI BBFC":pegi_b, "COB":cob, "GRB":grb, "CGSRR":cgsrr}
    def region_lock(self):
        lock = self.read_u32()
        lockout = {}
        if (lock & 0x1):
            lockout["Japan"] = True
        else:
            lockout["Japan"] = False
        if (lock & 0x2):
            lockout["NorthAmerica"] = True
        else:
            lockout["NorthAmerica"] = False
        if (lock & 0x4):
            lockout["Europe"] = True
        else:
            lockout["Europe"] = False
        if (lock & 0x8):
            lockout["Australia"] = True
        else:
            lockout["Australia"] = False
        if (lock & 0x10):
            lockout["China"] = True
        else:
            lockout["China"] = False
        if (lock & 0x20):
            lockout["Korea"] = True
        else:
            lockout["Korea"] = False
        if (lock & 0x40):
            lockout["Taiwan"] = True
        else:
            lockout["Taiwan"] = False
        self.contents["RegionLockout"]=lockout
    def match_ids(self):
        _id = self.read_u32()
        bit_id = self.read_u64()
        self.contents["MatchID"]=str(_id)
        self.contents["MatchBITID"] = str(bit_id)
    def get_flags(self):
        flags = self.read_u32()
        flg={}
        flg["_V"] = flags & 0x1
        flg["_A"] = flags & 0x2
        flg["_3d"] = flags & 0x4
        flg["_E"] = flags & 0x8
        flg["_Q"] = flags & 0x10
        flg["_X"] = flags & 0x20
        flg["_R"] = flags & 0x40
        flg["_S"] = flags & 0x80
        flg["_U"] = flags & 0x100
        flg["_SD"] = flags & 0x200
        flg["_N"] = flags & 0x400
        self.contents["Flags"] = flg
    def get_eula(self):
        self.contents["EULAversion"] = str(self.read_u8()) + "." + str(self.read_u8())
    def read_smdh(self):
        self.contents["Version"] = str(self.read_u8()) + "." + str(self.read_u8())
        self.read_u16()
        self.info_struct("JP")
        self.info_struct("EN")
        self.info_struct("FR")
        self.info_struct("GR")
        self.info_struct("IT")
        self.info_struct("ES")
        self.info_struct("CH_S")
        self.info_struct("KO")
        self.info_struct("DE")
        self.info_struct("PR")
        self.info_struct("RU")
        self.info_struct("CH_T")
        self.info_struct("Unused1")
        self.info_struct("Unused2")
        self.info_struct("Unused3")
        self.info_struct("Unused4")
        self.ratings()
        self.region_lock()
        self.match_ids()
        self.get_flags()
        self.get_eula()
        self.read_u16()
        self.contents["BannerFrame"] = str(self.read_u16())
        self.contents["CECID"] = str(self.read_u16())
        self.read_u32()
        self.read_u32()
        return self.contents
    def __init__(self, fname):
        self.fin = open(fname, 'rb')
        if self.fin.read(4).decode("UTF-8") != "SMDH":
            self.fin.close()
            raise TypeError("Not a SMDH (missing or incorrect magic)")
        self.contents={}
