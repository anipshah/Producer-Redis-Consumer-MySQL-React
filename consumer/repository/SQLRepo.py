import pymysql
import sqlalchemy.pool as pool
import Constants
import os
import logging
from error_handler import MessageException


class SQLRepo:
    def __init__(self):
        def get_conn():
            connection = pymysql.connect(user=str(os.environ['DB_USER']), password=str(os.environ['DB_PASSWORD']),
                                         db=str(os.environ['DB_NAME']), host=str(os.environ['DB_HOST']))
            return connection

        # defining connection pool
        self.mypool = pool.QueuePool(get_conn, max_overflow=Constants.MAX_OVERFLOW, pool_size=Constants.POOL_SIZE)

    def add_message_request(self, message_no: int, arrival_time: str, transmission_time: str):
        """
        Function to add message request to db

        :param message_no: int: message number
        :param arrival_time: str: arrival time of the message request
        :param transmission_time: str: transmission time of the message request from producer
        :return:
        """
        conn = self.mypool.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT IGNORE INTO consumer VALUES ({message_no},'{transmission_time}','{arrival_time}')".format(
                    message_no=int(message_no), arrival_time=arrival_time, transmission_time=transmission_time))
            conn.commit()
        except pymysql.Error as e:
            logging.error("cannot perform a query to insert data")
            logging.error(e)
            raise e
        finally:
            cursor.close()
            conn.close()
        return True

    def get_max_message_number(self):
        """
        Function to get max message number till now

        :return: int: message number
        """
        conn = self.mypool.connect()
        cursor = conn.cursor()

        try:
            max_message_query = "SELECT MAX(message_no) as max_number from consumer"
            cursor.execute(max_message_query)
            result = cursor.fetchone()

            if result:
                return result[0]
            else:
                return 0
        except pymysql.Error as e:
            logging.error("cannot perform a query pymysql")
            logging.error(e)
            raise e
        finally:
            cursor.close()
            conn.close()

    def avg_time(self, seconds: int = 10):
        """
        Function to get average time based on seconds

        :param seconds: int:
        :return: int: average time of transmission of messages in last {seconds} seconds
        """
        conn = self.mypool.connect()
        cursor = conn.cursor()

        try:
            avg_time_query = f"""SELECT AVG(arrival_time - transmission_time) as avg_time
                             FROM consumer
                             WHERE arrival_time >= (now() - interval {seconds} second)"""
            logging.info(avg_time_query)

            cursor.execute(avg_time_query)
            result = cursor.fetchone()

            if result and result[0]:
                return "{:.4f}".format(round(float(str(result[0])), 4))
            else:
                return 0
        except pymysql.Error as e:
            logging.error("cannot perform a query")
            logging.error(e)
            raise e
        finally:
            cursor.close()
            conn.close()
