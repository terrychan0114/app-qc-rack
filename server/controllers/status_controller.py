import connexion
import six
import pandas as pd
from pandas import ExcelFile
import json
from flask import Response
from loguru import logger
from datetime import datetime


from server.models.status_info import StatusInfo  # noqa: E501
from server import util

# file = "/usr/src/app/doc/test_QC incoming rack priority list.xlsx"
# file = "X:/S1-Quality Control Shared/Qc incoming rack/test_QC incoming rack priority list.xlsx"


def get_qcrack(sorting, group=None):  # noqa: E501
    """Get all status at Paterson

     # noqa: E501

    :param sorting: This is getting the suggestion status with sorting order
    :type sorting: str

    :rtype: List[StatusInfo]
    """
    df = pd.read_excel(file, sheet_name='test_qc_incoming')

    result = df.to_json(orient="records")
    df_json = json.loads(result)
    df_json_sort = []
    # logger.debug(df_json)
    for i in range(len(df_json)):
        # logger.debug(df_json[i])

        df_json[i]["sequence"] = df_json[i].pop("Seq #")
        df_json[i]["part_num"] = df_json[i].pop("Part #")
        df_json[i]["description"] = df_json[i].pop("Description")
        df_json[i]["wo_num"] = df_json[i].pop("Work Order number")
        df_json[i]["quantity"] = df_json[i].pop("Quantity")
        df_json[i]["process_step"] = df_json[i].pop("Process step")
        # df_json[i]["entry_date"] = df_json[i].pop("Entry date")
        df_json[i]["priority"] = df_json[i].pop("Priority")
        df_json[i]["inspector"] = df_json[i].pop("Inspector")
        df_json[i]["time_spent"] = df_json[i].pop("Time spend on the job")
        # df_json[i]["ts_completion"] = df_json[i].pop("Completion time")
        df_json[i]["comment"] = df_json[i].pop("Comment")
        df_json[i]["quantity_acc_rej"] = df_json[i].pop("Quantity accepted or rejected")
        df_json[i]["current_stat"] = df_json[i].pop("Current status")
        df_json[i]["final_stat"] = df_json[i].pop("Final status")
        try:
            timestamp = df_json[i]["Entry date"]/1000
            date = datetime.fromtimestamp(timestamp)
            df_json[i]["entry_date"] = date.strftime("%m/%d/%Y")
            df_json[i].pop("Entry date")
        except:
            logger.debug("Entry date is not a timestamp")
        try:
            timestamp = df_json[i]["Completion time"]/1000
            date = datetime.fromtimestamp(timestamp)
            df_json[i]["ts_completion"] = date.strftime("%m/%d/%Y")
            df_json[i].pop("Completion time")
        except:
            df_json[i].pop("Completion time")
        
        if group == '' or group == None:
            if df_json[i]['final_stat'] == "Completed":
                continue
            else:
                logger.debug("Default grouping")
                df_json_sort.append(df_json[i])
        elif group == "pending":
            if df_json[i]['final_stat'] == "Pending":
                logger.debug("pending group")
                df_json_sort.append(df_json[i])
            else:
                continue
        elif group == "completed":
            if df_json[i]['final_stat'] == "Complete":
                logger.debug("Complete group")
                df_json_sort.append(df_json[i])
            else:
                continue
        elif group == "ongoing":
            if df_json[i]['final_stat'] == "Ongoing":
                logger.debug("Ongoing group")
                df_json_sort.append(df_json[i])
            else:
                continue
        elif group == "all":
            df_json_sort.append(df_json[i])
        else:
            df_json_sort.append(df_json[i])
        
    if sorting == "sequence":
        return_json = sorted(df_json_sort,key=lambda i:i[sorting])
    else:
        return_json = sorted(df_json_sort,key=lambda i:i[sorting], reverse=True)
    # logger.debug(df_json_sort)
    return return_json
