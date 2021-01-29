from datetime import datetime
from repository.SQLRepo import SQLRepo
from typing import Dict, Any
import Constants
import logging
from error_handler import MessageException
import pymysql


class PostConsumer:

    def __init__(self):
        self.message_repo = SQLRepo()

    def consume(self, post):
        """
        Function to get message request and store into database

        :param post: Dict[str,Any]: request with message number and transmission time
        :return:
        """
        date_format = Constants.DATE_FORMAT
        if post[Constants.MESSAGE_NUMBER] and post[Constants.TRANSMISSION_TIME]:
            message_no = post[Constants.MESSAGE_NUMBER]

            try:
                # just for validation purpose
                datetime.strptime(post[Constants.TRANSMISSION_TIME], date_format)
                transmission_time = post[Constants.TRANSMISSION_TIME]

            except ValueError:
                logging.error("This is the incorrect date string format. It should be YYYY-MM-DD hh:mm:ss:fff")
                raise MessageException(
                    f"Time format for transmission time is not valid: {post[Constants.TRANSMISSION_TIME]}",
                    status_code=400)
            # calculate arrival time
            now = datetime.now()
            arrival_time = now.strftime(Constants.DATE_FORMAT)
            try:
                self.message_repo.add_message_request(message_no, arrival_time, transmission_time)
            except pymysql.Error:
                raise MessageException(f"Something wrong on the server.", status_code=500)
        else:
            raise MessageException(f"Necessary Parameters are missing.", status_code=400)
        return message_no

    def get_stats(self, seconds: int = 10):
        """
        Function to get statistics

        :param seconds: int: number of seconds for getting average time
        :return: Dict[str,Any]: response containing maximum message number and average time
        """
        if seconds is None:
            seconds = Constants.DEFAULT_SECONDS
        # get maximum message number
        try:
            max_message_no: int = self.message_repo.get_max_message_number()
            # get average time in last few seconds defined b seconds param
            average_time: float = self.message_repo.avg_time(seconds)

            stats: Dict[str, Any] = {Constants.MAX_MESSAGE_NUMBER: max_message_no,
                                     Constants.AVERAGE_TIME: average_time}
            return stats
        except pymysql.Error:
            raise MessageException(f"Something wrong on the server.", status_code=500)
