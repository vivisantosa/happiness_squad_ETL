{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "import pprint\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "#1 The first step is to look for relevant table. In this case it is actually faster to paste the URL to chrome and do search function.\n",
    "#URL is 'https://www150.statcan.gc.ca/t1/wds/rest/getAllCubesListLite'\n",
    "\n",
    "#2. We found that the table we want is \"Average satisfaction with life and with selected domains of life by age group and sex\"\n",
    "#3. What's important is the productId, which is be used for downloading the CSV.\n",
    "#4. Product id is 13100106\n",
    "#5. The next thing to do is to call the download method.\n",
    "#https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{product_id}/en"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'status': 'SUCCESS', 'object': 'https://www150.statcan.gc.ca/n1/tbl/csv/13100106-eng.zip'}\n"
     ]
    }
   ],
   "source": [
    "#Apply the GetFullTable Method\n",
    "product_id = 13100106\n",
    "download_path = f\"https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{product_id}/en\"\n",
    "response = requests.get(download_path)\n",
    "table = response.json()\n",
    "print(table)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "https://www150.statcan.gc.ca/n1/tbl/csv/13100106-eng.zip\n"
     ]
    }
   ],
   "source": [
    "#get download path\n",
    "download_url = table[\"object\"]\n",
    "print(download_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'13100106-eng.zip'"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Capture the file name with regex\n",
    "import re\n",
    "\n",
    "split= download_url.split(\"/csv/\")\n",
    "file_name = split[1]\n",
    "\n",
    "file_name"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "42335"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Create request to download...\n",
    "r = requests.get(download_url, allow_redirects=True)\n",
    "\n",
    "open(file_name, 'wb').write(r.content)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "#because the data is in zip format, use python to unzip it\n",
    "from zipfile import ZipFile\n",
    "\n",
    "with ZipFile(file_name, 'r') as zipObj:\n",
    "   # Extract all the contents of zip file in current directory\n",
    "   zipObj.extractall()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "# clean the data, get the columns we want\n",
    "import pandas as pd\n",
    "df = pd.read_csv(\"13100106.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Extract the columns we want\n",
    "\n",
    "df = df[[\"REF_DATE\",\"GEO\",\"Age group\",\"Sex\",\"Satisfaction with life and with selected domains of life\",\"VALUE\"]]\n",
    "df.drop_duplicates(keep = \"first\", inplace = True)\n",
    "df.dropna(inplace= True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.to_csv(\"Statcan_CSV.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
