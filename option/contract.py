# -*- coding: utf-8 -*-

call = 'CALL'
put = 'PUT'


class OptionSh50:
    """

    """
    def __init__(self, option_code):
        self.asset = {}
        self.types = [call, put]
        self.amount_unit = 10000
        self.price_unit = 0.0001
        self.due_months = []

    @staticmethod
    def get_spread(price):
        if price <= 3:
            return 0.05
        elif price <= 5:
            return 0.1
        elif price <= 10:
            return 0.25
        elif price <= 20:
            return 0.5
        elif price <= 50:
            return 1
        elif price <= 100:
            return 2.5
        else:
            return 5

    @staticmethod
    def get_call_max_up(asset_pre_close, strike_price):
        return max(asset_pre_close * 0.005, min(2 * asset_pre_close - strike_price, asset_pre_close) * 0.1)

    @staticmethod
    def get_call_max_down(asset_pre_close):
        return asset_pre_close * 0.1

    @staticmethod
    def get_put_max_up(asset_pre_close, strike_price):
        return max(strike_price * 0.005, min(2 * strike_price - asset_pre_close, asset_pre_close) * 0.1)

    @staticmethod
    def get_put_max_down(asset_pre_close):
        return asset_pre_close * 0.1


