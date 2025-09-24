import csv
import json
import os
from pathlib import Path

import pandas as pd

from src.variables import CSV_CONFIG_FILE, CSV_OUTPUT_FILE, JSON_OUTPUT_FILE


def mergeJsonFiles(jsonFiles: list[str]):
    mergedData = []

    for filePath in jsonFiles:
        pathObj = Path(filePath)
        with open(pathObj, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                mergedData.extend(data)
            else:
                mergedData.append(data)

    with open(JSON_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(mergedData, f)

    with open(JSON_OUTPUT_FILE, 'r', encoding='utf-8') as f:
        jsonList = json.load(f)
        formtJson = fmtSerialNumber(jsonList)
        resource = flatJsonList(formtJson)

    return resource


def flatJsonList(jsonList: list[dict]) -> list[dict]:
    def flatten(obj, parentKey='', result=None):
        if result is None:
            result = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                fullKey = f"{parentKey}.{k}" if parentKey else k
                flatten(v, fullKey, result)
        elif isinstance(obj, list) and all(
            isinstance(i, (dict, list)) for i in obj
        ):
            for idx, item in enumerate(obj):
                flatten(item, parentKey, result)
        else:
            result[parentKey] = obj
        return result

    flatList = []
    for item in jsonList:
        flat = flatten(item)
        flatList.append(flat)
    return flatList


def fmt4ascii4hex(serial: list[int]) -> str:
    asciiPart = ''.join(chr(b) for b in serial[:4])
    hexPart = ''.join(f'{b:02X}' for b in serial[4:])
    return f"{asciiPart}-{hexPart}"


def fmtSerialNumber(jsonList: list[dict]) -> list[dict]:
    fmtJson = []
    for jsonObj in jsonList:
        for test in jsonObj.get("tests", []):
            serialPath = test.get("results", {}).get(
                "data", {}).get("gpon", {})
            if isinstance(serialPath.get("ontSerialNumber"), list):
                serialNumber = serialPath["ontSerialNumber"]
                fmtSerial = fmt4ascii4hex(serialNumber)
                serialPath["ontSerialNumber"] = fmtSerial
        fmtJson.append(jsonObj)
    return fmtJson


def loadColumnOrder(csvConfig: Path) -> list[str]:
    with open(csvConfig, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row['column'] for row in sorted(
            reader,
            key=lambda r: int(r['order'])
        )]


def writeCsv(resource: list[dict]):
    columnOrder = loadColumnOrder(CSV_CONFIG_FILE)

    with open(CSV_OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columnOrder)
        writer.writeheader()

        for row in resource:
            orderedRow = {col: row.get(col, '') for col in columnOrder}
            writer.writerow(orderedRow)


def saveToExcel(outputPath: str):
    dataFrame = pd.read_csv(CSV_OUTPUT_FILE, encoding='latin-1')
    excelPath = outputPath.partition('.')[0] + '.xlsx'
    dataFrame.to_excel(excelPath, index=False)
    return excelPath


def openReport(filePath):
    os.startfile(filePath)
