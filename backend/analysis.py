"""Executes the trading strategies and analyzes the results.
"""

import math
from datetime import datetime

import pandas
from talib import abstract


class StrategyAnalyzer():
    """Contains all the methods required for analyzing strategies.
    """

    def __init__(self):
        """Initializes StrategyAnalyzer class
        """
        pass

    def __convert_to_dataframe(self, historical_data):
        """Converts historical data matrix to a pandas dataframe.

        Args:
            historical_data (list): A matrix of historical OHCLV data.

        Returns:
            pandas.DataFrame: Contains the historical data in a pandas dataframe.
        """

        dataframe = pandas.DataFrame(historical_data)
        dataframe.transpose()

        dataframe = pandas.DataFrame(historical_data)
        dataframe.transpose()
        dataframe.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        dataframe['datetime'] = dataframe.timestamp.apply(
            lambda x: pandas.to_datetime(datetime.fromtimestamp(x / 1000).strftime('%c'))
        )

        dataframe.set_index('datetime', inplace=True, drop=True)
        dataframe.drop('timestamp', axis=1, inplace=True)

        return dataframe

    def analyze_macd(self, historial_data, hot_thresh=None, cold_thresh=None, all_data=False):
        """Performs a macd analysis on the historical data

        Args:
            historial_data (list): A matrix of historical OHCLV data.
            hot_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to purchase.
            cold_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to sell.
            all_data (bool, optional): Defaults to False. If True, we return the MACD associated
                with each data point in our historical dataset. Otherwise just return the last one.

        Returns:
            dict: A dictionary containing a tuple of indicator values and booleans for buy / sell
                indication.
        """

        dataframe = self.__convert_to_dataframe(historial_data)
        macd_values = abstract.MACD(dataframe).iloc[:, 0]

        macd_result_data = []
        for macd_value in macd_values:
            if math.isnan(macd_value):
                continue

            is_hot = False
            if hot_thresh is not None:
                is_hot = macd_value > hot_thresh

            is_cold = False
            if cold_thresh is not None:
                is_cold = macd_value < cold_thresh

            data_point_result = {
                'values': (macd_value,),
                'is_cold': is_cold,
                'is_hot': is_hot
            }

            macd_result_data.append(data_point_result)

        if all_data:
            return macd_result_data
        else:
            if macd_result_data:
                return macd_result_data[-1]
            else:
                return macd_result_data

    def analyze_rsi(self, historial_data, period_count=14,
                    hot_thresh=None, cold_thresh=None, all_data=False):
        """Performs an RSI analysis on the historical data

        Args:
            historial_data (list): A matrix of historical OHCLV data.
            period_count (int, optional): Defaults to 14. The number of data points to consider for
                our simple moving average.
            hot_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to purchase.
            cold_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to sell.
            all_data (bool, optional): Defaults to False. If True, we return the RSI associated
                with each data point in our historical dataset. Otherwise just return the last one.

        Returns:
            dict: A dictionary containing a tuple of indicator values and booleans for buy / sell
                indication.
        """

        dataframe = self.__convert_to_dataframe(historial_data)
        rsi_values = abstract.RSI(dataframe, period_count)

        rsi_result_data = []
        for rsi_value in rsi_values:
            if math.isnan(rsi_value):
                continue

            is_hot = False
            if hot_thresh is not None:
                is_hot = rsi_value < hot_thresh

            is_cold = False
            if cold_thresh is not None:
                is_cold = rsi_value > cold_thresh

            data_point_result = {
                'values': (rsi_value,),
                'is_cold': is_cold,
                'is_hot': is_hot
            }

            rsi_result_data.append(data_point_result)

        if all_data:
            return rsi_result_data
        else:
            if rsi_result_data:
                return rsi_result_data[-1]
            else:
                return rsi_result_data

    def analyze_sma(self, historial_data, period_count=15,
                    hot_thresh=None, cold_thresh=None, all_data=False):
        """Performs a SMA analysis on the historical data

        Args:
            historial_data (list): A matrix of historical OHCLV data.
            period_count (int, optional): Defaults to 15. The number of data points to consider for
                our simple moving average.
            hot_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to purchase.
            cold_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to sell.
            all_data (bool, optional): Defaults to False. If True, we return the SMA associated
                with each data point in our historical dataset. Otherwise just return the last one.

        Returns:
            dict: A dictionary containing a tuple of indicator values and booleans for buy / sell
                indication.
        """

        dataframe = self.__convert_to_dataframe(historial_data)
        sma_values = abstract.SMA(dataframe, period_count)
        combined_data = pandas.concat([dataframe, sma_values], axis=1)
        combined_data.rename(columns={0: 'sma_value'}, inplace=True)

        sma_result_data = []
        for sma_row in combined_data.iterrows():
            if math.isnan(sma_row[1]['sma_value']):
                continue

            is_hot = False
            if hot_thresh is not None:
                threshold = sma_row[1]['sma_value'] * hot_thresh
                is_hot = sma_row[1]['close'] > threshold

            is_cold = False
            if cold_thresh is not None:
                threshold = sma_row[1]['sma_value'] * cold_thresh
                is_cold = sma_row[1]['close'] < sma_row[1]['sma_value']

            data_point_result = {
                'values': (sma_row[1]['sma_value'],),
                'is_cold': is_cold,
                'is_hot': is_hot
            }

            sma_result_data.append(data_point_result)

        if all_data:
            return sma_result_data
        else:
            if sma_result_data:
                return sma_result_data[-1]
            else:
                return sma_result_data

    def analyze_ema(self, historial_data, period_count=15,
                    hot_thresh=None, cold_thresh=None, all_data=False):
        """Performs an EMA analysis on the historical data

        Args:
            historial_data (list): A matrix of historical OHCLV data.
            period_count (int, optional): Defaults to 15. The number of data points to consider for
                our exponential moving average.
            hot_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to purchase.
            cold_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to sell.
            all_data (bool, optional): Defaults to False. If True, we return the EMA associated
                with each data point in our historical dataset. Otherwise just return the last one.

        Returns:
            dict: A dictionary containing a tuple of indicator values and booleans for buy / sell
                indication.
        """

        dataframe = self.__convert_to_dataframe(historial_data)
        ema_values = abstract.EMA(dataframe, period_count)
        combined_data = pandas.concat([dataframe, ema_values], axis=1)
        combined_data.rename(columns={0: 'ema_value'}, inplace=True)

        ema_result_data = []
        for ema_row in combined_data.iterrows():
            if math.isnan(ema_row[1]['ema_value']):
                continue

            is_hot = False
            if hot_thresh is not None:
                threshold = ema_row[1]['ema_value'] * hot_thresh
                is_hot = ema_row[1]['close'] > threshold

            is_cold = False
            if cold_thresh is not None:
                threshold = ema_row[1]['ema_value'] * cold_thresh
                is_cold = ema_row[1]['close'] < ema_row[1]['ema_value']

            data_point_result = {
                'values': (ema_row[1]['ema_value'],),
                'is_cold': is_cold,
                'is_hot': is_hot
            }

            ema_result_data.append(data_point_result)

        if all_data:
            return ema_result_data
        else:
            if ema_result_data:
                return ema_result_data[-1]
            else:
                return ema_result_data

    def analyze_bollinger_bands(self, historial_data, all_data=False):
        """Performs a bollinger band analysis on the historical data

        Args:
            historial_data (list): A matrix of historical OHCLV data.
            all_data (bool, optional): Defaults to False. If True, we return the BB's associated
                with each data point in our historical dataset. Otherwise just return the last one.

        Returns:
            dict: A dictionary containing a tuple of indicator values and booleans for buy / sell
                indication.
        """

        dataframe = self.__convert_to_dataframe(historial_data)
        bollinger_data = abstract.BBANDS(dataframe, 21)

        bb_result_data = []
        for bb_row in bollinger_data.iterrows():
            if math.isnan(bb_row[1]['upperband']) or\
                math.isnan(bb_row[1]['middleband']) or\
                math.isnan(bb_row[1]['lowerband']):
                continue

            data_point_result = {
                'values': (
                    bb_row[1]['upperband'],
                    bb_row[1]['middleband'],
                    bb_row[1]['lowerband']
                ),
                'is_hot': False,
                'is_cold': False
            }

            bb_result_data.append(data_point_result)

        if all_data:
            return bb_result_data
        else:
            if bb_result_data:
                return bb_result_data[-1]
            else:
                return bb_result_data
