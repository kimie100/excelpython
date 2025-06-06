import os
import pytz
import logging
from sqlalchemy import create_engine
from urllib.parse import quote_plus
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(SCRIPT_DIR, "reports")
os.makedirs(REPORTS_DIR, mode=0o777, exist_ok=True)


# Database credentials production
username = "admin"
password = quote_plus("Bank@123456")  # URL encode the password
host = "178.16.138.52"
port = "3306"
database = "calculatorProduction"

# Database credentials dev
# username = "root"
# password = quote_plus("123456")  # URL encode the password
# host = "localhost"
# port = "3306"
# database = "calculatorProduction"



# Database
DATABASE_URL = f"mysql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)

# Timezone
malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')

# Report settings
#QUERY_DATE_RANGE = ('2025-02-11 00:00:00', '2025-02-11 23:59:59')

color_code_mapping = {
    "A385": "daeef3",
    "A386": "b7dee8",
    "A387": "92cddc",
    "A606": "4bacc6",
    "A802": "31869b",
    "A803": "fde9d9",
    "A805": "fcd5b4",
    "A806": "fabf8f",
    "A807": "f7964a",
    "A808": "e26b0a",
    "A810": "e4dfec",
    "A812": "ccc0da",
    "A813": "b1a0c7",
    "A815": "b17ac7",
    "A816": "8064a2",
    "A817": "ebf1de",
    "A819": "d8e4bc",
    "A820": "c4d79b",
    "A821": "9bbb59",
    "A822": "76933c",
    "A823": "f2dcdb",
    "A825": "e6b8b7",
    "A826": "da9694",
    "B01": "c86f6f",
    "B02": "c0504d",
    "B03": "eeeae1",
    "B05": "ddd9c4",
    "B06": "c4bd97",
    "B07": "b1a66f",
    "B08": "857a4d",
    "B09": "dce6f1",
    "B11": "b8cce4",
    "B18": "95b3d7",
    "B19": "5885c7",
    "B20": "37649b",
    "B80": "f2f2f2",
    "B81": "d9d9d9",
    "B82": "bfbfbf",
    "B88": "a6a6a6",
    "B361": "808080",
    "B362": "ffffc8",
    "B363": "ffff9b",
    "B365": "ffff64",
    "B366": "ffff00",
    "B371": "e9e900",
    "B372": "deffbc",
    "B373": "c8ff9b",
    "B375": "bcff6f",
    "B376": "9bff42",
    "B377": "7af400",
    "B378": "c5d9f1",
    "B379": "90bcde",
    "B380": "649bd3",
    "B381": "427ac8",
    "B382": "2c6fbc",
    "B383": "daeef3",
    "B388": "b7dee8",
    "B391": "92cddc",
    "B392": "4bacc6",
    "B393": "31869b",
    "K01": "fde9d9",
    "K02": "fcd5b4",
    "K03": "fabf8f",
    "K05": "f7964a",
    "N181": "e26b0a",
    "N182": "e4dfec",
    "N185": "ccc0da",
    "N186": "b1a0c7",
    "N187": "b17ac7",
    "N188": "8064a2",
    "N201": "ebf1de",
    "N202": "d8e4bc",
    "N203": "c4d79b",
    "N231": "9bbb59",
    "N701": "76933c",
    "P01": "f2dcdb",
    "P02": "e6b8b7",
    "P03": "da9694",
    "P05": "c86f6f",
    "S109": "c0504d",
    "S130": "eeeae1",
    "S131": "ddd9c4",
    "S133": "c4bd97",
    "S135": "b1a66f",
    "S136": "857a4d",
    "S138": "e1e1f0",
    "S139": "c7c7de",
    "S152": "9b9bbc",
    "S152T": "8585b1",
    "S155": "71719b",
    "S156": "c5d9f1",
    "S157": "8db4e2",
    "S601": "538dd5",
    "S603": "ff5050",
    "S703": "ff7c80",
    "S705": "ff9999",
    "A500": "ffcccc",
    "A502": "ffe5e5",
    "A503": "f2e2e6",
    "A506": "d5e1d6",
    "A507": "c5d5c6",
    "A508": "a7c1a7",
    "A509": "91b193",
    "A510": "769e79",
    "A511": "49674b",
    "A512": "ccecff",
    "A513": "99ccff",
    "A515": "6699ff",
    "A516": "3366ff",
    "A519": "6666ff",
    "A520": "9999ff",
    "B501": "ccccff",
    "B505": "ffccff",
    "B517": "ff99ff",
    "B518": "ff65ff",
    "G": "ffe5f2",
    "H": "ffbdde",
    "Y": "ff85c2",
    "T": "ff5dae",
    "R": "ff3399",
    "OFFICE": "daeef3"
}
