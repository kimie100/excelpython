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
    "A385": "ffdaeef3",
    "A386": "ffb7dee8",
    "A387": "ff92cddc",
    "A606": "ff4bacc6",
    "A802": "ff31869b",
    "A803": "fffde9d9",
    "A805": "fffcd5b4",
    "A806": "fffabf8f",
    "A807": "fff7964a",
    "A808": "ffe26b0a",
    "A810": "ffe4dfec",
    "A812": "ffccc0da",
    "A813": "ffb1a0c7",
    "A815": "ffb17ac7",
    "A816": "ff8064a2",
    "A817": "ffebf1de",
    "A819": "ffd8e4bc",
    "A820": "ffc4d79b",
    "A821": "ff9bbb59",
    "A822": "ff76933c",
    "A823": "fff2dcdb",
    "A825": "ffe6b8b7",
    "A826": "ffda9694",
    "B01": "ffc86f6f",
    "B02": "ffc0504d",
    "B03": "ffeeeae1",
    "B05": "ffddd9c4",
    "B06": "ffc4bd97",
    "B07": "ffb1a66f",
    "B08": "ff857a4d",
    "B09": "ffdce6f1",
    "B11": "ffb8cce4",
    "B18": "ff95b3d7",
    "B19": "ff5885c7",
    "B20": "ff37649b",
    "B80": "fff2f2f2",
    "B81": "ffd9d9d9",
    "B82": "ffbfbfbf",
    "B88": "ffa6a6a6",
    "B361": "ff808080",
    "B362": "fffffcc8",
    "B363": "ffffff9b",
    "B365": "ffffff64",
    "B366": "ffffff00",
    "B371": "ffe9e900",
    "B372": "ffdeffbc",
    "B373": "ffc8ff9b",
    "B375": "ffbcff6f",
    "B376": "ff9bff42",
    "B377": "ff7af400",
    "B378": "ffc5d9f1",
    "B379": "ff90bcde",
    "B380": "ff649bd3",
    "B381": "ff427ac8",
    "B382": "ff2c6fbc",
    "B383": "ffdaeef3",
    "B388": "ffb7dee8",
    "B391": "ff92cddc",
    "B392": "ff4bacc6",
    "B393": "ff31869b",
    "K01": "fffde9d9",
    "K02": "fffcd5b4",
    "K03": "fffabf8f",
    "K05": "fff7964a",
    "N181": "ffe26b0a",
    "N182": "ffe4dfec",
    "N185": "ffccc0da",
    "N186": "ffb1a0c7",
    "N187": "ffb17ac7",
    "N188": "ff8064a2",
    "N201": "ffebf1de",
    "N202": "ffd8e4bc",
    "N203": "ffc4d79b",
    "N231": "ff9bbb59",
    "N701": "ff76933c",
    "P01": "fff2dcdb",
    "P02": "ffe6b8b7",
    "P03": "ffda9694",
    "P05": "ffc86f6f",
    "S109": "ffc0504d",
    "S130": "ffeeeae1",
    "S131": "ffddd9c4",
    "S133": "ffc4bd97",
    "S135": "ffb1a66f",
    "S136": "ff857a4d",
    "S138": "ffe1e1f0",
    "S139": "ffc7c7de",
    "S152": "ff9b9bbc",
    "S152T": "ff8585b1",
    "S155": "ff71719b",
    "S156": "ffc5d9f1",
    "S157": "ff8db4e2",
    "S601": "ff538dd5",
    "S603": "ffff5050",
    "S703": "ffff7c80",
    "S705": "ffff9999",
    "A500": "ffffcccc",
    "A502": "ffffe5e5",
    "A503": "fff2e2e6",
    "A506": "ffd5e1d6",
    "A507": "ffc5d5c6",
    "A508": "ffa7c1a7",
    "A509": "ff91b193",
    "A510": "ff769e79",
    "A511": "ff49674b",
    "A512": "ffccecff",
    "A513": "ff99ccff",
    "A515": "ff6699ff",
    "A516": "ff3366ff",
    "A519": "ff6666ff",
    "A520": "ff9999ff",
    "B501": "ffccccff",
    "B505": "ffffccff",
    "B517": "ffff99ff",
    "B518": "ffff65ff",
    "G": "ffffe5f2",
    "H": "ffffbdde",
    "Y": "ffff85c2",
    "T": "ffff5dae",
    "R": "ffff3399",
    "OFFICE": "ffdaeef3"
}